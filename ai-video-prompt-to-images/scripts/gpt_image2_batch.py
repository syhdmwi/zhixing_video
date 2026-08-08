#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


YIJIA_IMAGE2_URL = "https://api.yijiarj.cn/v1/chat/completions"
CANONICAL_MODEL = "GPT-Image-2"
API_MODEL_ID = "image2"
MODEL_ALIASES = {"gpt-image-2", "gpt_image_2", "image-2", "image2"}
ASPECT_RATIO_SIZES = {
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "1:1": "1024x1024",
    "21:9": "1920x822",
    "9:21": "822x1920",
}
SUPPORTED_SIZES = set(ASPECT_RATIO_SIZES.values())


def http_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: float = 900,
) -> dict:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    data = json.dumps(body or {}).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=request_headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionResetError) as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def normalize_size(value: str) -> str:
    normalized = value.strip()
    if normalized in ASPECT_RATIO_SIZES:
        return ASPECT_RATIO_SIZES[normalized]
    if normalized in SUPPORTED_SIZES:
        return normalized
    supported = ", ".join(sorted(ASPECT_RATIO_SIZES))
    raise ValueError(f"Unsupported aspect ratio or size: {value}. Use one of: {supported}.")


def normalize_model(value: str) -> str:
    if value == CANONICAL_MODEL or value.strip().lower() in MODEL_ALIASES:
        return CANONICAL_MODEL
    raise ValueError(f"Unsupported image model: {value}. Only {CANONICAL_MODEL} is enabled.")


def build_message_content(prompt: str, reference_urls: list[str]) -> str | list[dict]:
    if not reference_urls:
        return prompt

    content: list[dict] = [{"type": "text", "text": prompt}]
    content.extend(
        {
            "type": "image_url",
            "image_url": {"url": url},
        }
        for url in reference_urls
    )
    return content


def submit_task(
    api_key: str,
    prompt: str,
    size: str,
    reference_urls: list[str],
    *,
    timeout: float,
) -> dict:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": build_message_content(prompt, reference_urls),
            }
        ],
        "model": API_MODEL_ID,
        "size": size,
    }
    return http_json(
        YIJIA_IMAGE2_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        body=payload,
        timeout=timeout,
    )


def extract_image_urls(content: str) -> list[str]:
    markdown_urls = re.findall(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", content)
    if markdown_urls:
        return list(dict.fromkeys(markdown_urls))

    raw_urls = re.findall(
        r"https?://[^\s<>()\[\]]+\.(?:png|jpe?g|webp)(?:\?[^\s<>()\[\]]*)?",
        content,
        flags=re.IGNORECASE,
    )
    return list(dict.fromkeys(raw_urls))


def parse_image_response(response: dict) -> tuple[str | None, str, list[str]]:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError(f"Image-2 response missing choices: {json.dumps(response, ensure_ascii=False)}")

    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str):
        raise RuntimeError(f"Image-2 response missing message content: {json.dumps(response, ensure_ascii=False)}")

    image_urls = extract_image_urls(content)
    if not image_urls:
        raise RuntimeError(f"Image-2 response contained no image URL: {content}")
    task_id = response.get("id") if isinstance(response.get("id"), str) else None
    return task_id, content, image_urls


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


def normalize_item(item: dict, default_aspect_ratio: str, default_model: str) -> dict:
    reference_urls = item.get("reference_urls", [])
    if not isinstance(reference_urls, list) or not all(isinstance(url, str) and url for url in reference_urls):
        raise ValueError(f"Queue item {item['shot_id']} reference_urls must be a list of non-empty URLs.")

    aspect_ratio = str(item.get("aspect_ratio") or item.get("size") or default_aspect_ratio)
    return {
        "shot_id": str(item["shot_id"]),
        "frame_type": item.get("frame_type", "character"),
        "model": normalize_model(str(item.get("model") or default_model)),
        "aspect_ratio": aspect_ratio,
        "size": normalize_size(aspect_ratio),
        "image_prompt": str(item["image_prompt"]),
        "reference_urls": reference_urls,
        "consistency_note": item.get("consistency_note", ""),
    }


def submit_queue(
    api_key: str,
    queue: list[dict],
    *,
    request_timeout: float,
    max_retries: int,
) -> dict:
    ordered_results: list[dict] = []
    request_count = 0

    for item in queue:
        attempts: list[dict] = []
        task_id: str | None = None
        message = ""
        image_urls: list[str] = []

        for attempt_index in range(1, max_retries + 2):
            request_count += 1
            try:
                response = submit_task(
                    api_key,
                    item["image_prompt"],
                    item["size"],
                    item["reference_urls"],
                    timeout=request_timeout,
                )
                task_id, message, image_urls = parse_image_response(response)
                attempts.append(
                    {
                        "attempt_index": attempt_index,
                        "task_id": task_id,
                        "status": 2,
                        "result": image_urls,
                        "message": message,
                        "timed_out": False,
                    }
                )
                print(
                    json.dumps(
                        {
                            "event": "completed",
                            "shot_id": item["shot_id"],
                            "task_id": task_id,
                            "attempt_index": attempt_index,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                break
            except RuntimeError as exc:
                message = str(exc)
                attempts.append(
                    {
                        "attempt_index": attempt_index,
                        "task_id": None,
                        "status": 3,
                        "result": [],
                        "message": message,
                        "timed_out": False,
                    }
                )
                print(
                    json.dumps(
                        {
                            "event": "request_error",
                            "shot_id": item["shot_id"],
                            "attempt_index": attempt_index,
                            "error": message,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if attempt_index <= max_retries:
                    time.sleep(min(2 * attempt_index, 6))

        succeeded = bool(image_urls)
        ordered_results.append(
            {
                "shot_id": item["shot_id"],
                "frame_type": item["frame_type"],
                "model": item["model"],
                "api_model": API_MODEL_ID,
                "aspect_ratio": item["aspect_ratio"],
                "size": item["size"],
                "image_prompt": item["image_prompt"],
                "reference_urls": item["reference_urls"],
                "consistency_note": item["consistency_note"],
                "task_id": task_id,
                "status": 2 if succeeded else 3,
                "result": image_urls,
                "image_urls": image_urls,
                "message": message,
                "status_label": "success" if succeeded else "failed",
                "retry_attempts_used": max(0, len(attempts) - 1),
                "next_action": "review_generated_image" if succeeded else "review_prompt_or_platform_error_then_retry",
                "attempts": attempts,
            }
        )

    completed_count = sum(1 for item in ordered_results if item["status_label"] == "success")
    failed_count = len(ordered_results) - completed_count
    return {
        "generation_queue": ordered_results,
        "execution_notes": {
            "provider": "yijia",
            "endpoint": YIJIA_IMAGE2_URL,
            "api_model": API_MODEL_ID,
            "request_count": request_count,
            "submitted_count": request_count,
            "completed_count": completed_count,
            "failed_count": failed_count,
            "pending_count": 0,
            "stuck_count": 0,
            "retried_count": sum(1 for item in ordered_results if item["retry_attempts_used"] > 0),
            "max_retries": max_retries,
            "timed_out": False,
        },
        "qc_checklist": [
            "Confirm every shot_id returned at least one image URL.",
            "Confirm recurring subjects kept the approved appearance.",
            "Confirm failed shots are reviewed and retried when needed.",
        ],
        "rendered_images_for_review": [
            {"shot_id": item["shot_id"], "image_urls": item["image_urls"]}
            for item in ordered_results
            if item["image_urls"]
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an Image-2 batch through the Yijia API.")
    parser.add_argument("--queue-file", required=True, help="Path to a JSON queue file.")
    parser.add_argument("--aspect-ratio", default="16:9", help="Default ratio or supported pixel size.")
    parser.add_argument("--model", default=CANONICAL_MODEL, help="Canonical model label for queue metadata.")
    parser.add_argument(
        "--request-timeout",
        "--timeout",
        dest="request_timeout",
        type=float,
        default=900.0,
        help="Timeout for each synchronous Image-2 request.",
    )
    parser.add_argument(
        "--max-retries",
        "--max-stuck-retries",
        dest="max_retries",
        type=int,
        default=1,
        help="Automatic retries after a failed synchronous request.",
    )
    parser.add_argument("--poll-interval", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--out", help="Optional output JSON file path.")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    api_key = os.environ.get("YIJIA_API_KEY")
    if not api_key:
        print("YIJIA_API_KEY is not set", file=sys.stderr)
        return 2

    queue = load_queue(Path(args.queue_file))
    normalized_queue = [normalize_item(item, args.aspect_ratio, args.model) for item in queue]
    result = submit_queue(
        api_key,
        normalized_queue,
        request_timeout=args.request_timeout,
        max_retries=max(0, args.max_retries),
    )

    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)
    if args.out:
        Path(args.out).write_text(result_json + "\n", encoding="utf-8")
    return 1 if result["execution_notes"]["failed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
