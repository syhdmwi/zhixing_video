#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SUBMIT_URL = "https://api.wuyinkeji.com/api/async/image_nanoBanana2"
DETAIL_URL = "https://api.wuyinkeji.com/api/async/detail"
DEFAULT_MODEL = "nanobanana-2"


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: int = 60,
) -> dict:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def submit_task(api_key: str, prompt: str, aspect_ratio: str, size: str, urls: list[str] | None) -> dict:
    payload: dict[str, object] = {
        "prompt": prompt,
        "aspectRatio": aspect_ratio,
        "size": size,
    }
    if urls:
        payload["urls"] = urls

    return http_json(
        SUBMIT_URL,
        method="POST",
        headers={"Authorization": api_key},
        body=payload,
    )


def fetch_detail(api_key: str, task_id: str) -> dict:
    query = urllib.parse.urlencode({"id": task_id})
    return http_json(
        f"{DETAIL_URL}?{query}",
        headers={"Authorization": api_key},
    )


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


def normalize_item(item: dict, default_aspect_ratio: str, default_size: str, default_model: str) -> dict:
    return {
        "shot_id": str(item["shot_id"]),
        "frame_type": item.get("frame_type", "character"),
        "model": item.get("model", default_model),
        "aspect_ratio": item.get("aspect_ratio", default_aspect_ratio),
        "size": item.get("size", default_size),
        "image_prompt": item["image_prompt"],
        "reference_urls": item.get("reference_urls", []),
        "consistency_note": item.get("consistency_note", ""),
    }


def summarize_detail(detail: dict | None) -> dict:
    data = (detail or {}).get("data") or {}
    return {
        "status": data.get("status"),
        "result": data.get("result"),
        "message": data.get("message"),
        "updated_at": data.get("updated_at"),
    }


def next_action_for_item(frame_type: str, status: int | None, retry_attempts_used: int, max_stuck_retries: int) -> str:
    if status == 2:
        return "review_generated_image"
    if status == 3:
        return "review_prompt_or_platform_error_then_retry"
    if retry_attempts_used < max_stuck_retries:
        return "retry_pending_task"
    if frame_type in {"subject_preview", "three_view", "subject_three_view"}:
        return "platform_stuck_after_retries; if repeated output is still unsatisfactory, ask user for reference image"
    return "platform_stuck_after_retries; retry later or review manually"


def submit_queue(
    api_key: str,
    queue: list[dict],
    *,
    poll_interval: float,
    timeout: float,
    max_stuck_retries: int,
) -> dict:
    state_by_shot_id: dict[str, dict] = {
        item["shot_id"]: {
            **item,
            "attempts": [],
        }
        for item in queue
    }

    pending_items = list(queue)
    submit_count = 0
    had_timeout_events = False

    for attempt_index in range(1, max_stuck_retries + 2):
        if not pending_items:
            break

        active_tasks: dict[str, dict] = {}
        for item in pending_items:
            response = submit_task(
                api_key,
                item["image_prompt"],
                item["aspect_ratio"],
                item["size"],
                item["reference_urls"],
            )
            task_id = (((response or {}).get("data") or {}).get("id"))
            attempt_state = {
                "attempt_index": attempt_index,
                "task_id": task_id,
                "submit_response": response,
                "status": None,
                "result": None,
                "message": "",
                "timed_out": False,
                "terminal": False,
                "last_detail": None,
            }
            state_by_shot_id[item["shot_id"]]["attempts"].append(attempt_state)
            submit_count += 1
            if task_id:
                active_tasks[task_id] = {
                    "item": item,
                    "attempt_state": attempt_state,
                }
            print(
                json.dumps(
                    {
                        "event": "submitted",
                        "shot_id": item["shot_id"],
                        "task_id": task_id,
                        "attempt_index": attempt_index,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

        deadline = time.time() + timeout
        while active_tasks and time.time() < deadline:
            for task_id, task_info in list(active_tasks.items()):
                item = task_info["item"]
                attempt_state = task_info["attempt_state"]
                detail = fetch_detail(api_key, task_id)
                summary = summarize_detail(detail)
                attempt_state["last_detail"] = detail
                attempt_state["status"] = summary["status"]
                attempt_state["result"] = summary["result"]
                attempt_state["message"] = summary["message"]
                print(
                    json.dumps(
                        {
                            "event": "polled",
                            "shot_id": item["shot_id"],
                            "task_id": task_id,
                            "status": summary["status"],
                            "attempt_index": attempt_index,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if summary["status"] in (2, 3):
                    attempt_state["terminal"] = True
                    del active_tasks[task_id]
            if active_tasks:
                time.sleep(poll_interval)

        pending_next_attempt: list[dict] = []
        for task_id, task_info in active_tasks.items():
            item = task_info["item"]
            attempt_state = task_info["attempt_state"]
            attempt_state["timed_out"] = True
            pending_next_attempt.append(item)

        if pending_next_attempt:
            had_timeout_events = True
            print(
                json.dumps(
                    {
                        "event": "attempt_timed_out",
                        "attempt_index": attempt_index,
                        "pending_shot_ids": [item["shot_id"] for item in pending_next_attempt],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        pending_items = pending_next_attempt

    ordered_results: list[dict] = []
    for item in queue:
        state = state_by_shot_id[item["shot_id"]]
        attempts = state["attempts"]
        latest_attempt = attempts[-1] if attempts else {}
        latest_detail = latest_attempt.get("last_detail")
        latest_summary = summarize_detail(latest_detail)
        retry_attempts_used = max(0, len(attempts) - 1)
        ordered_results.append(
            {
                "shot_id": item["shot_id"],
                "frame_type": item["frame_type"],
                "model": item["model"],
                "aspect_ratio": item["aspect_ratio"],
                "size": item["size"],
                "image_prompt": item["image_prompt"],
                "reference_urls": item["reference_urls"],
                "consistency_note": item["consistency_note"],
                "task_id": latest_attempt.get("task_id"),
                "status": latest_summary["status"],
                "result": latest_summary["result"],
                "message": latest_summary["message"],
                "status_label": (
                    "success"
                    if latest_summary["status"] == 2
                    else "failed"
                    if latest_summary["status"] == 3
                    else "platform_stuck"
                ),
                "retry_attempts_used": retry_attempts_used,
                "next_action": next_action_for_item(
                    item["frame_type"],
                    latest_summary["status"],
                    retry_attempts_used,
                    max_stuck_retries,
                ),
                "attempts": [
                    {
                        "attempt_index": attempt["attempt_index"],
                        "task_id": attempt["task_id"],
                        "status": attempt["status"],
                        "result": attempt["result"],
                        "message": attempt["message"],
                        "timed_out": attempt["timed_out"],
                    }
                    for attempt in attempts
                ],
            }
        )

    unresolved_stuck_count = sum(1 for item in ordered_results if item.get("status_label") == "platform_stuck")
    return {
        "generation_queue": ordered_results,
        "execution_notes": {
            "submitted_count": submit_count,
            "completed_count": sum(1 for item in ordered_results if item.get("status") == 2),
            "failed_count": sum(1 for item in ordered_results if item.get("status") == 3),
            "pending_count": sum(1 for item in ordered_results if item.get("status") not in (2, 3)),
            "stuck_count": unresolved_stuck_count,
            "retried_count": sum(1 for item in ordered_results if item.get("retry_attempts_used", 0) > 0),
            "max_stuck_retries": max_stuck_retries,
            "had_timeout_events": had_timeout_events,
            "timed_out": unresolved_stuck_count > 0,
        },
        "qc_checklist": [
            "Confirm every shot_id returned a terminal status.",
            "Confirm pure-scene shots remain at least one-third of the batch.",
            "Confirm recurring subjects kept the approved appearance.",
            "Confirm failed shots are reviewed and retried when needed.",
            "Confirm platform_stuck shots use preserved task history before resubmitting.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a NanoBanana2 image-generation batch from an approved queue file.")
    parser.add_argument("--queue-file", required=True, help="Path to a JSON queue file.")
    parser.add_argument("--aspect-ratio", default="16:9", help="Default aspect ratio for items missing aspect_ratio.")
    parser.add_argument("--size", default="1K", help="Default output size for items missing size.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name label for queue metadata.")
    parser.add_argument("--poll-interval", type=float, default=15.0, help="Polling interval in seconds.")
    parser.add_argument("--timeout", type=float, default=900.0, help="Batch polling timeout in seconds.")
    parser.add_argument("--max-stuck-retries", type=int, default=1, help="Automatic resubmits for non-terminal tasks after timeout.")
    parser.add_argument("--out", help="Optional output JSON file path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = os.environ.get("NANOBANANA_API_KEY")
    if not api_key:
        print("NANOBANANA_API_KEY is not set", file=sys.stderr)
        return 2

    queue_file = Path(args.queue_file)
    queue = load_queue(queue_file)
    normalized_queue = [
        normalize_item(item, args.aspect_ratio, args.size, args.model)
        for item in queue
    ]

    result = submit_queue(
        api_key,
        normalized_queue,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
        max_stuck_retries=max(0, args.max_stuck_retries),
    )

    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)

    if args.out:
        Path(args.out).write_text(result_json + "\n", encoding="utf-8")

    timed_out = result["execution_notes"]["timed_out"]
    failed_count = result["execution_notes"]["failed_count"]
    return 1 if timed_out or failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
