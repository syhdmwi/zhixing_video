#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


YIJIA_DEFAULT_BASE_URL = "https://api.yijiarj.cn"
YIJIA_US_BASE_URL = "https://apius.yijiarj.cn"
YIJIA_CREATE_PATH = "/v1/videos"
YIJIA_CHAT_COMPLETIONS_PATH = "/v1/chat/completions"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
ARK_CONTENTS_GENERATION_PATH = "/contents/generations/tasks"
GROK_DEFAULT_MODEL = "grok-imagine-1.0-video-super"


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


def http_event_stream(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: int = 900,
) -> list[str]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=request_headers, method="POST")
    events: list[str] = []
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if line:
                    events.append(line)
        return events
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def load_queue(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Queue file must contain a top-level JSON array.")
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Queue item #{index} must be a JSON object.")
        for field in ("shot_id", "source_image_url", "motion_prompt", "size"):
            if field not in item:
                raise ValueError(f"Queue item #{index} must include '{field}'.")
    return data


def provider_has_credentials(provider: str) -> bool:
    if provider == "grok":
        return bool(os.environ.get("YIJIA_API_KEY"))
    if provider == "seedance":
        return False
    return False


def default_model_for_provider(provider: str) -> str:
    if provider == "grok":
        return GROK_DEFAULT_MODEL
    if provider == "seedance":
        raise RuntimeError("seedance is temporarily disabled")
    raise RuntimeError(f"Unsupported provider: {provider}")


def choose_auto_provider(item: dict) -> tuple[str, str]:
    has_grok = provider_has_credentials("grok")

    if has_grok:
        return "grok", "seedance_disabled_use_grok"
    raise RuntimeError("No active video provider key found. Set YIJIA_API_KEY.")


def resolve_provider_and_model(item: dict) -> tuple[dict, str]:
    requested_provider = str(item.get("provider", "auto")).strip().lower() or "auto"
    if requested_provider == "auto":
        provider, decision = choose_auto_provider(item)
    else:
        provider = requested_provider
        decision = "explicit_provider"

    resolved = dict(item)
    resolved["provider"] = provider
    resolved["model"] = str(item.get("model") or default_model_for_provider(provider))
    return resolved, decision


def yijia_base_url_for_item(item: dict) -> str:
    source = str(item.get("source_image_url", ""))
    if "|" in source:
        return YIJIA_US_BASE_URL
    return item.get("base_url", YIJIA_DEFAULT_BASE_URL)


def yijia_chat_base_url_for_item(item: dict) -> str:
    return item.get("base_url", YIJIA_DEFAULT_BASE_URL)


def submit_veo(api_key: str, item: dict) -> dict:
    base_url = yijia_base_url_for_item(item)
    payload: dict[str, object] = {
        "prompt": item["motion_prompt"],
        "model": item["model"],
        "input_reference": item["source_image_url"],
        "size": item["size"],
    }
    if item.get("remix_id"):
        payload["remix_id"] = item["remix_id"]
    return http_json(
        f"{base_url}{YIJIA_CREATE_PATH}",
        method="POST",
        headers={"Authorization": f"Bearer {api_key}"},
        body=payload,
    )


def poll_veo(api_key: str, item: dict, video_id: str) -> dict:
    base_url = yijia_base_url_for_item(item)
    return http_json(
        f"{base_url}{YIJIA_CREATE_PATH}/{urllib.parse.quote(video_id)}",
        headers={"Authorization": f"Bearer {api_key}"},
    )


def build_grok_message_content(item: dict) -> list[dict]:
    content: list[dict] = []
    motion_prompt = str(item.get("motion_prompt", "")).strip()
    if motion_prompt:
        content.append({"type": "text", "text": motion_prompt})

    source_image_url = str(item.get("source_image_url", "")).strip()
    if not source_image_url:
        raise RuntimeError("Grok queue item must include source_image_url.")

    for url in [part.strip() for part in source_image_url.split("|") if part.strip()]:
        content.append({"type": "image_url", "image_url": {"url": url}})

    return content


def extract_progress_percent(text: str) -> int | None:
    match = re.search(r"当前进度\s*(\d+)%", text)
    if match:
        return int(match.group(1))
    match = re.search(r"progress\s*=\s*(\d+)%", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def extract_video_url_from_text(text: str) -> str | None:
    match = re.search(r"https?://[^\s\"']+\.mp4(?:\?[^\s\"']+)?", text)
    if match:
        return match.group(0)
    return None


def submit_grok(api_key: str, item: dict) -> dict:
    ratio = item.get("ratio") or derive_ratio_from_size(str(item.get("size", ""))) or "16:9"
    resolution_name = item.get("resolution_name") or derive_resolution_from_size(str(item.get("size", ""))) or "480p"
    video_length = str(item.get("video_length") or item.get("duration_seconds") or item.get("duration") or 5)
    preset = item.get("preset", "fun")

    payload: dict[str, object] = {
        "model": item["model"],
        "messages": [
            {
                "role": "user",
                "content": build_grok_message_content(item),
            }
        ],
        "video_config": {
            "video_length": video_length,
            "aspect_ratio": ratio,
            "preset": preset,
            "resolution_name": resolution_name,
        },
    }

    events = http_event_stream(
        f"{yijia_chat_base_url_for_item(item)}{YIJIA_CHAT_COMPLETIONS_PATH}",
        headers={"Authorization": f"Bearer {api_key}"},
        body=payload,
    )

    chunk_ids: list[str] = []
    content_parts: list[str] = []
    progress_messages: list[str] = []
    video_url: str | None = None
    finish_reason: str | None = None
    model_name: str | None = None

    for event in events:
        if not event.startswith("data:"):
            continue
        data_str = event[len("data:") :].strip()
        if not data_str or data_str == "[DONE]":
            continue
        try:
            payload_chunk = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        chunk_id = payload_chunk.get("id")
        if isinstance(chunk_id, str):
            chunk_ids.append(chunk_id)
        if isinstance(payload_chunk.get("model"), str):
            model_name = payload_chunk["model"]

        choices = payload_chunk.get("choices")
        if not isinstance(choices, list):
            continue
        for choice in choices:
            if not isinstance(choice, dict):
                continue
            if choice.get("finish_reason"):
                finish_reason = str(choice.get("finish_reason"))
            delta = choice.get("delta")
            if not isinstance(delta, dict):
                continue
            content = delta.get("content")
            if isinstance(content, str) and content:
                content_parts.append(content)
                if extract_progress_percent(content) is not None:
                    progress_messages.append(content.strip())
                maybe_video_url = extract_video_url_from_text(content)
                if maybe_video_url:
                    video_url = maybe_video_url

    if not video_url:
        raise RuntimeError("Grok stream completed but no video URL was found in the streamed content.")

    task_id = next((value for value in reversed(chunk_ids) if value), None)
    transcript = "".join(content_parts)
    return {
        "id": task_id,
        "status": "completed",
        "object": "chat.completion.stream",
        "model": model_name or item["model"],
        "video_url": video_url,
        "finish_reason": finish_reason,
        "stream_events": len(events),
        "progress_messages": progress_messages,
        "stream_transcript": transcript,
    }


def parse_size(size: str) -> tuple[int, int] | None:
    try:
        width_str, height_str = size.lower().split("x", 1)
        return int(width_str), int(height_str)
    except (TypeError, ValueError):
        return None


def derive_ratio_from_size(size: str) -> str | None:
    parsed = parse_size(size)
    if not parsed:
        return None
    width, height = parsed
    if width == 0 or height == 0:
        return None
    common_ratios = {
        (16, 9): "16:9",
        (9, 16): "9:16",
        (4, 3): "4:3",
        (3, 4): "3:4",
        (1, 1): "1:1",
        (21, 9): "21:9",
        (9, 21): "9:21",
    }
    from math import gcd

    factor = gcd(width, height)
    reduced = (width // factor, height // factor)
    return common_ratios.get(reduced, f"{reduced[0]}:{reduced[1]}")


def derive_resolution_from_size(size: str) -> str | None:
    parsed = parse_size(size)
    if not parsed:
        return None
    width, height = parsed
    max_side = max(width, height)
    if max_side >= 1920:
        return "1080p"
    if max_side >= 1280:
        return "720p"
    return "480p"


def build_seedance_content(item: dict) -> list[dict]:
    content: list[dict] = []
    motion_prompt = str(item.get("motion_prompt", "")).strip()
    if motion_prompt:
        content.append({"type": "text", "text": motion_prompt})

    source_image_url = str(item.get("source_image_url", "")).strip()
    if source_image_url:
        # The official video generation docs define a multimodal content array.
        # Here we build a conservative text + image_url payload for first-frame image-to-video.
        content.append({"type": "image_url", "image_url": {"url": source_image_url}})

    if not content:
        raise RuntimeError("Seedance queue item must include at least one text or image input.")
    return content


def submit_seedance(api_key: str, item: dict) -> dict:
    payload: dict[str, object] = {
        "model": item["model"],
        "content": build_seedance_content(item),
    }

    resolution = item.get("resolution") or derive_resolution_from_size(str(item.get("size", "")))
    ratio = item.get("ratio") or derive_ratio_from_size(str(item.get("size", "")))
    if resolution:
        payload["resolution"] = resolution
    if ratio:
        payload["ratio"] = ratio

    if "duration_seconds" in item:
        payload["duration"] = item["duration_seconds"]
    elif "duration" in item:
        payload["duration"] = item["duration"]

    if "frames" in item:
        payload["frames"] = item["frames"]
    if "seed" in item:
        payload["seed"] = item["seed"]
    if "camera_fixed" in item:
        payload["camera_fixed"] = item["camera_fixed"]
    if "watermark" in item:
        payload["watermark"] = item["watermark"]
    if "callback_url" in item:
        payload["callback_url"] = item["callback_url"]
    if "return_last_frame" in item:
        payload["return_last_frame"] = item["return_last_frame"]
    if "draft_mode" in item:
        payload["draft_mode"] = item["draft_mode"]
    if "safety_identifier" in item:
        payload["safety_identifier"] = item["safety_identifier"]

    return http_json(
        f"{ARK_BASE_URL}{ARK_CONTENTS_GENERATION_PATH}",
        method="POST",
        headers={"Authorization": f"Bearer {api_key}"},
        body=payload,
    )


def poll_seedance(api_key: str, _: dict, task_id: str) -> dict:
    return http_json(
        f"{ARK_BASE_URL}{ARK_CONTENTS_GENERATION_PATH}/{urllib.parse.quote(task_id)}",
        headers={"Authorization": f"Bearer {api_key}"},
    )


def submit_item(item: dict) -> tuple[dict, str | None]:
    provider = item["provider"]
    if provider == "grok":
        api_key = os.environ.get("YIJIA_API_KEY")
        if not api_key:
            raise RuntimeError("YIJIA_API_KEY is not set")
        response = submit_grok(api_key, item)
        task_id = response.get("id")
        return response, task_id
    if provider == "veo":
        api_key = os.environ.get("YIJIA_API_KEY")
        if not api_key:
            raise RuntimeError("YIJIA_API_KEY is not set")
        response = submit_veo(api_key, item)
        video_id = response.get("id") or ((response.get("data") or {}).get("id") if isinstance(response.get("data"), dict) else None)
        return response, video_id
    if provider == "seedance":
        raise RuntimeError("seedance is temporarily disabled")
    raise RuntimeError(f"Unsupported provider: {provider}")


def poll_item(item: dict, task_id: str) -> dict:
    provider = item["provider"]
    if provider == "grok":
        return item.get("detail") or {}
    if provider == "veo":
        api_key = os.environ.get("YIJIA_API_KEY")
        if not api_key:
            raise RuntimeError("YIJIA_API_KEY is not set")
        return poll_veo(api_key, item, task_id)
    if provider == "seedance":
        raise RuntimeError("seedance is temporarily disabled")
    raise RuntimeError(f"Unsupported provider: {provider}")


def status_is_terminal(provider: str, detail: dict) -> tuple[bool, bool]:
    if provider == "grok":
        status = str(detail.get("status", "")).lower()
        if status == "completed":
            return True, True
        if status in {"error", "failed"}:
            return True, False
        return False, False
    if provider == "veo":
        status = str(detail.get("status", "")).lower()
        if status == "completed":
            return True, True
        if status == "error":
            return True, False
        return False, False
    if provider == "seedance":
        status = str(detail.get("status", "")).lower()
        if status in {"succeeded", "failed", "expired"}:
            return True, status == "succeeded"
        return False, False
    return False, False


def extract_render_url(provider: str, detail: dict) -> str | None:
    if provider == "grok":
        return detail.get("video_url") or extract_video_url_from_text(str(detail.get("stream_transcript", "")))
    if provider == "veo":
        return detail.get("video_url") or detail.get("url")
    if provider == "seedance":
        content = detail.get("content")
        if isinstance(content, dict):
            return (
                content.get("video_url")
                or content.get("url")
                or ((content.get("video_urls") or [None])[0] if isinstance(content.get("video_urls"), list) else None)
            )
        return (
            detail.get("video_url")
            or detail.get("url")
            or ((detail.get("video_urls") or [None])[0] if isinstance(detail.get("video_urls"), list) else None)
        )
    return None


def run_queue(queue: list[dict], poll_interval: float, timeout: float) -> dict:
    submitted: list[dict] = []
    for item in queue:
        resolved_item, provider_decision = resolve_provider_and_model(item)
        try:
            submit_response, task_id = submit_item(resolved_item)
            detail = submit_response if resolved_item["provider"] == "grok" else None
            submitted.append(
                {
                    **resolved_item,
                    "task_id": task_id,
                    "submit_response": submit_response,
                    "submit_error": None,
                    "detail": detail,
                    "provider_decision": provider_decision,
                    "fallback_from": None,
                }
            )
            print(json.dumps({"event": "submitted", "shot_id": resolved_item["shot_id"], "provider": resolved_item["provider"], "task_id": task_id, "provider_decision": provider_decision}, ensure_ascii=False), flush=True)
        except Exception as exc:  # noqa: BLE001
            submitted.append(
                {
                    **resolved_item,
                    "task_id": None,
                    "submit_response": None,
                    "submit_error": str(exc),
                    "detail": None,
                    "provider_decision": provider_decision,
                    "fallback_from": None,
                }
            )
            print(json.dumps({"event": "submit_error", "shot_id": resolved_item["shot_id"], "provider": resolved_item["provider"], "error": str(exc), "provider_decision": provider_decision}, ensure_ascii=False), flush=True)

    deadline = time.time() + timeout
    pending = [
        item
        for item in submitted
        if item.get("task_id") and not item.get("submit_error") and item["provider"] != "grok"
    ]

    while pending and time.time() < deadline:
        next_pending: list[dict] = []
        for item in pending:
            try:
                detail = poll_item(item, item["task_id"])
                item["detail"] = detail
                terminal, success = status_is_terminal(item["provider"], detail)
                print(json.dumps({"event": "polled", "shot_id": item["shot_id"], "provider": item["provider"], "task_id": item["task_id"], "terminal": terminal, "success": success}, ensure_ascii=False), flush=True)
                if not terminal:
                    next_pending.append(item)
            except Exception as exc:  # noqa: BLE001
                item["detail"] = {"poll_error": str(exc)}
        if next_pending:
            time.sleep(poll_interval)
        pending = next_pending

    results: list[dict] = []
    for item in submitted:
        detail = item.get("detail") or {}
        if item.get("submit_error"):
            status_label = "submit_error"
        elif detail.get("poll_error"):
            status_label = "poll_error"
        elif item["provider"] == "grok":
            grok_status = str(detail.get("status", "")).lower()
            if grok_status == "completed":
                status_label = "success"
            elif grok_status in {"error", "failed"}:
                status_label = "failed"
            else:
                status_label = "pending"
        elif item["provider"] == "veo":
            veo_status = str(detail.get("status", "")).lower()
            if veo_status == "completed":
                status_label = "success"
            elif veo_status == "error":
                status_label = "failed"
            else:
                status_label = "pending"
        elif item["provider"] == "seedance":
            seedance_status = str(detail.get("status", "")).lower()
            if seedance_status == "succeeded":
                status_label = "success"
            elif seedance_status in {"failed", "expired"}:
                status_label = "failed"
            else:
                status_label = "pending"
        else:
            status_label = "pending"

        results.append(
            {
                "shot_id": item["shot_id"],
                "provider": item["provider"],
                "model": item["model"],
                "provider_decision": item.get("provider_decision"),
                "fallback_from": item.get("fallback_from"),
                "task_id": item.get("task_id"),
                "status_label": status_label,
                "render_url": extract_render_url(item["provider"], detail),
                "submit_error": item.get("submit_error"),
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
                "shot_id": item["shot_id"],
                "provider": item["provider"],
                "render_url": item["render_url"],
            }
            for item in results
            if item.get("render_url")
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Choose a provider and run an approved image-to-video batch.")
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
