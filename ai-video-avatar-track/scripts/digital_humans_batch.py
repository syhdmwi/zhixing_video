#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SUBMIT_URL = "https://api.wuyinkeji.com/api/async/video_digital_humans"
DETAIL_URL = "https://api.wuyinkeji.com/api/async/detail"


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


def submit_task(api_key: str, item: dict) -> dict:
    payload: dict[str, object] = {
        "videoName": item["video_name"],
    }
    if item.get("audio_url"):
        payload["audioUrl"] = item["audio_url"]
    if item.get("video_url"):
        payload["videoUrl"] = item["video_url"]
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
    normalized: list[dict] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Queue item #{index} must be a JSON object.")
        if "video_name" not in item:
            raise ValueError(f"Queue item #{index} must include 'video_name'.")
        if not item.get("audio_url"):
            raise ValueError(f"Queue item #{index} must include 'audio_url'.")
        if not item.get("video_url"):
            raise ValueError(f"Queue item #{index} must include 'video_url'.")
        normalized.append(
            {
                "segment_id": str(item.get("segment_id") or f"avatar-{index:02d}"),
                "video_name": str(item["video_name"]),
                "audio_url": str(item["audio_url"]),
                "video_url": str(item["video_url"]),
                "notes": str(item.get("notes", "")),
            }
        )
    return normalized


def summarize_detail(detail: dict | None) -> dict:
    data = (detail or {}).get("data") or {}
    return {
        "status": data.get("status"),
        "message": data.get("message"),
        "result": data.get("result"),
        "updated_at": data.get("updated_at"),
    }


def extract_render_url(result: object) -> str | None:
    if isinstance(result, str):
        return result if result.startswith("http") else None
    if isinstance(result, list):
        for item in result:
            if isinstance(item, str) and item.startswith("http"):
                return item
            if isinstance(item, dict):
                for key in ("url", "video_url", "download_url"):
                    value = item.get(key)
                    if isinstance(value, str) and value.startswith("http"):
                        return value
    if isinstance(result, dict):
        for key in ("url", "video_url", "download_url"):
            value = result.get(key)
            if isinstance(value, str) and value.startswith("http"):
                return value
    return None


def run_queue(queue: list[dict], poll_interval: float, timeout: float) -> dict:
    submitted: list[dict] = []
    for item in queue:
        try:
            response = submit_task(get_api_key(), item)
            task_id = ((response.get("data") or {}).get("id") if isinstance(response.get("data"), dict) else None)
            submitted.append(
                {
                    **item,
                    "task_id": task_id,
                    "submit_response": response,
                    "submit_error": None,
                    "detail": None,
                }
            )
            print(
                json.dumps(
                    {"event": "submitted", "segment_id": item["segment_id"], "task_id": task_id},
                    ensure_ascii=False,
                ),
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            submitted.append(
                {
                    **item,
                    "task_id": None,
                    "submit_response": None,
                    "submit_error": str(exc),
                    "detail": None,
                }
            )
            print(
                json.dumps(
                    {"event": "submit_error", "segment_id": item["segment_id"], "error": str(exc)},
                    ensure_ascii=False,
                ),
                flush=True,
            )

    deadline = time.time() + timeout
    pending = [item for item in submitted if item.get("task_id") and not item.get("submit_error")]
    api_key = get_api_key()

    while pending and time.time() < deadline:
        next_pending: list[dict] = []
        for item in pending:
            try:
                detail = fetch_detail(api_key, item["task_id"])
                item["detail"] = detail
                summary = summarize_detail(detail)
                status = summary["status"]
                print(
                    json.dumps(
                        {
                            "event": "polled",
                            "segment_id": item["segment_id"],
                            "task_id": item["task_id"],
                            "status": status,
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if status not in (2, 3):
                    next_pending.append(item)
            except Exception as exc:  # noqa: BLE001
                item["detail"] = {"poll_error": str(exc)}
        if next_pending:
            time.sleep(poll_interval)
        pending = next_pending

    results: list[dict] = []
    for item in submitted:
        detail = item.get("detail") or {}
        summary = summarize_detail(detail) if "poll_error" not in detail else {"status": None, "message": detail["poll_error"], "result": None, "updated_at": None}
        status = summary["status"]
        if item.get("submit_error"):
            status_label = "submit_error"
        elif detail.get("poll_error"):
            status_label = "poll_error"
        elif status == 2:
            status_label = "success"
        elif status == 3:
            status_label = "failed"
        else:
            status_label = "pending"
        results.append(
            {
                "segment_id": item["segment_id"],
                "video_name": item["video_name"],
                "task_id": item.get("task_id"),
                "status": status,
                "status_label": status_label,
                "render_url": extract_render_url(summary["result"]),
                "message": summary["message"],
                "updated_at": summary["updated_at"],
                "detail": detail,
            }
        )

    return {
        "generation_queue": results,
        "execution_notes": {
            "submitted_count": len(submitted),
            "success_count": sum(1 for item in results if item["status_label"] == "success"),
            "failed_count": sum(1 for item in results if item["status_label"] in {"failed", "submit_error", "poll_error"}),
            "pending_count": sum(1 for item in results if item["status_label"] == "pending"),
        },
        "rendered_videos_for_review": [
            {
                "segment_id": item["segment_id"],
                "render_url": item["render_url"],
            }
            for item in results
            if item.get("render_url")
        ],
    }


def get_api_key() -> str:
    api_key = os.environ.get("DIGITAL_HUMANS_API_KEY") or os.environ.get("WUYINKEJI_API_KEY")
    if not api_key:
        raise RuntimeError("DIGITAL_HUMANS_API_KEY or WUYINKEJI_API_KEY is not set")
    return api_key


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit and poll digital-human generation tasks.")
    parser.add_argument("--queue-file", required=True, help="Path to a JSON queue file.")
    parser.add_argument("--poll-interval", type=float, default=30.0, help="Polling interval in seconds.")
    parser.add_argument("--timeout", type=float, default=600.0, help="Total polling timeout in seconds.")
    parser.add_argument("--out", help="Optional output JSON file path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    queue = load_queue(Path(args.queue_file))
    result = run_queue(queue, args.poll_interval, args.timeout)
    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)
    if args.out:
        Path(args.out).write_text(result_json + "\n", encoding="utf-8")
    return 1 if result["execution_notes"]["failed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
