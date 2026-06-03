#!/usr/bin/env python3
"""seedream-5.0 batch image generation via 火山方舟 (Volcengine Ark)."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import socket
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# 火山方舟 OpenAI-compatible endpoint
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
IMAGES_URL = f"{BASE_URL}/images/generations"
CANONICAL_MODEL = "seedream-5.0"
ARK_MODEL_ID = "doubao-seedream-5-0-260128"


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: int = 120,
    retries: int = 3,
) -> dict:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionResetError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(min(2 * attempt, 6))
    raise RuntimeError(f"Request failed after {retries} attempts: {last_error}") from last_error


def aspect_to_size(aspect_ratio: str) -> str:
    """Convert aspect ratio to seedream resolution. seedream uses K-level resolution."""
    return "2K"


def submit_task(api_key: str, prompt: str, aspect_ratio: str, urls: list[str] | None) -> dict:
    payload: dict[str, object] = {
        "model": ARK_MODEL_ID,
        "prompt": prompt,
        "size": "2K",
        "output_format": "png",
        "watermark": False,
        "response_format": "url",
    }
    if urls:
        payload["reference_images"] = urls

    return http_json(
        IMAGES_URL,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}"},
        body=payload,
        timeout=120,
    )


def extract_urls(result: dict) -> list[str]:
    """Extract image URLs from seedream response."""
    data = result.get("data", [])
    urls = []
    for item in data:
        url = item.get("url", "")
        if url:
            urls.append(url)
    return urls


def load_queue(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Queue file must contain a top-level JSON array.")
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Queue item #{index} must be a JSON object.")
        if "shot_id" not in item or "image_prompt" not in item:
            raise ValueError(f"Queue item #{index} must include 'shot_id' and 'image_prompt'.")
    return data


def normalize_item(item: dict, default_aspect_ratio: str) -> dict:
    return {
        "shot_id": str(item["shot_id"]),
        "frame_type": item.get("frame_type", "scene"),
        "model": item.get("model", CANONICAL_MODEL),
        "aspect_ratio": item.get("aspect_ratio", default_aspect_ratio),
        "image_prompt": item["image_prompt"],
        "reference_urls": item.get("reference_urls", []),
        "consistency_note": item.get("consistency_note", ""),
    }


def process_batch(
    api_key: str,
    queue: list[dict],
    *,
    poll_interval: float = 15.0,
    timeout: float = 900.0,
    max_retries: int = 1,
) -> dict:
    results: list[dict] = []
    submit_count = 0

    for item in queue:
        attempt = 0
        success = False
        attempts_log: list[dict] = []

        while attempt <= max_retries and not success:
            attempt += 1
            try:
                print(json.dumps({"event": "submitting", "shot_id": item["shot_id"], "attempt": attempt}, ensure_ascii=False), flush=True)
                response = submit_task(
                    api_key,
                    item["image_prompt"],
                    item["aspect_ratio"],
                    item.get("reference_urls"),
                )
                urls = extract_urls(response)
                if urls:
                    success = True
                    attempts_log.append({
                        "attempt_index": attempt,
                        "status": "success",
                        "result": urls,
                        "message": "",
                    })
                    print(json.dumps({"event": "completed", "shot_id": item["shot_id"], "urls": urls}, ensure_ascii=False), flush=True)
                else:
                    attempts_log.append({
                        "attempt_index": attempt,
                        "status": "empty_result",
                        "result": [],
                        "message": "No image URLs in response",
                    })
                    print(json.dumps({"event": "empty_result", "shot_id": item["shot_id"], "response": response}, ensure_ascii=False), flush=True)
            except RuntimeError as exc:
                attempts_log.append({
                    "attempt_index": attempt,
                    "status": "error",
                    "result": [],
                    "message": str(exc),
                })
                print(json.dumps({"event": "error", "shot_id": item["shot_id"], "attempt": attempt, "error": str(exc)}, ensure_ascii=False), flush=True)
                time.sleep(5)

        submit_count += 1
        latest = attempts_log[-1] if attempts_log else {}
        results.append({
            "shot_id": item["shot_id"],
            "frame_type": item["frame_type"],
            "model": item["model"],
            "aspect_ratio": item["aspect_ratio"],
            "image_prompt": item["image_prompt"],
            "reference_urls": item.get("reference_urls", []),
            "consistency_note": item.get("consistency_note", ""),
            "status": 2 if success else 3,
            "result": latest.get("result", []),
            "message": latest.get("message", ""),
            "status_label": "success" if success else "failed",
            "retry_attempts_used": attempt - 1,
            "next_action": "review_generated_image" if success else "review_prompt_or_platform_error_then_retry",
            "attempts": attempts_log,
        })

    completed = sum(1 for r in results if r["status_label"] == "success")
    failed = sum(1 for r in results if r["status_label"] == "failed")

    return {
        "generation_queue": results,
        "execution_notes": {
            "submitted_count": submit_count,
            "completed_count": completed,
            "failed_count": failed,
            "pending_count": 0,
            "stuck_count": 0,
            "retried_count": sum(1 for r in results if r.get("retry_attempts_used", 0) > 0),
            "max_stuck_retries": max_retries,
            "had_timeout_events": False,
            "timed_out": False,
        },
        "qc_checklist": [
            "Confirm every shot_id returned a terminal status.",
            "Confirm recurring subjects kept the approved appearance.",
            "Confirm failed shots are reviewed and retried when needed.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a seedream-5.0 batch via 火山方舟.")
    parser.add_argument("--queue-file", required=True, help="Path to a JSON queue file.")
    parser.add_argument("--aspect-ratio", default="16:9", help="Default aspect ratio.")
    parser.add_argument("--poll-interval", type=float, default=15.0, help="Polling interval (unused — sync API).")
    parser.add_argument("--timeout", type=float, default=900.0, help="Timeout in seconds.")
    parser.add_argument("--max-retries", type=int, default=1, help="Retry count for failed requests.")
    parser.add_argument("--out", help="Optional output JSON file path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("VOLCENGINE_ARK_API_KEY")
    if not api_key:
        print("ARK_API_KEY or VOLCENGINE_ARK_API_KEY is not set", file=sys.stderr)
        return 2

    queue_file = Path(args.queue_file)
    queue = load_queue(queue_file)
    normalized_queue = [
        normalize_item(item, args.aspect_ratio)
        for item in queue
    ]

    result = process_batch(
        api_key,
        normalized_queue,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
        max_retries=max(0, args.max_retries),
    )

    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)

    if args.out:
        Path(args.out).write_text(result_json + "\n", encoding="utf-8")

    failed_count = result["execution_notes"]["failed_count"]
    return 1 if failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
