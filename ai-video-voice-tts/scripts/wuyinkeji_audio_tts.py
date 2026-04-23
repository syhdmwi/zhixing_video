#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

VENDOR_DIR = Path(__file__).resolve().parents[2] / ".vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

try:
    import tos  # type: ignore
except ImportError:
    tos = None


SUBMIT_URL = "https://api.wuyinkeji.com/api/async/audio_tts"
DETAIL_URL = "https://api.wuyinkeji.com/api/async/detail"
AUDIO_SUFFIXES = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: int = 120,
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


def fetch_binary(url: str, timeout: int = 180) -> bytes:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def submit_task(api_key: str, payload: dict) -> dict:
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


def slugify_filename(text: str) -> str:
    text = text.strip()
    if not text:
        return "tts-audio"
    compact = re.sub(r"\s+", "-", text[:24])
    safe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "", compact)
    return safe or "tts-audio"


def extract_audio_payload(payload: bytes, source_url: str) -> tuple[bytes, str, str | None]:
    suffix = Path(urllib.parse.urlparse(source_url).path).suffix.lower()
    if tarfile.is_tarfile(BytesIO(payload)):
        with tarfile.open(fileobj=BytesIO(payload), mode="r:*") as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            audio_member = next(
                (m for m in members if Path(m.name).suffix.lower() in AUDIO_SUFFIXES),
                None,
            )
            if audio_member is None:
                raise RuntimeError("TTS result tar archive does not contain a supported audio file.")
            file_obj = archive.extractfile(audio_member)
            if file_obj is None:
                raise RuntimeError("Failed to extract audio file from TTS tar archive.")
            audio_suffix = Path(audio_member.name).suffix.lower() or ".mp3"
            return file_obj.read(), audio_suffix, audio_member.name

    if suffix not in AUDIO_SUFFIXES:
        suffix = ".mp3"
    return payload, suffix, None


def build_tos_host(bucket: str, region: str) -> str:
    return f"{bucket}.tos-{region}.volces.com"


def put_object_to_tos(
    *,
    access_key_id: str,
    secret_access_key: str,
    bucket: str,
    region: str,
    object_key: str,
    payload: bytes,
    content_type: str,
    timeout: int = 180,
) -> str:
    if tos is None:
        raise RuntimeError("Official TOS SDK is not available. Install the `tos` package first.")

    client = tos.TosClientV2(
        ak=access_key_id,
        sk=secret_access_key,
        endpoint=f"tos-{region}.volces.com",
        region=region,
        request_timeout=timeout,
        socket_timeout=timeout,
    )

    try:
        client.put_object(
            bucket=bucket,
            key=object_key,
            content=payload,
            content_type=content_type,
        )
    except Exception as exc:
        raise RuntimeError(f"TOS upload via SDK failed: {exc}") from exc

    return build_public_tos_url(bucket, region, object_key)


def build_public_tos_url(bucket: str, region: str, object_key: str, custom_base: str | None = None) -> str:
    quoted_key = urllib.parse.quote(object_key, safe="/-_.~")
    if custom_base:
        return f"{custom_base.rstrip('/')}/{quoted_key}"
    return f"https://{build_tos_host(bucket, region)}/{quoted_key}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate local TTS audio from Wuyinkeji async audio_tts.")
    parser.add_argument("--text", required=True, help="Input text for TTS.")
    parser.add_argument("--voice-id", required=True, help="System voice_id from the TTS doc.")
    parser.add_argument("--speed", default="1")
    parser.add_argument("--vol", default="1")
    parser.add_argument("--language-boost", default="auto")
    parser.add_argument("--poll-interval", type=float, default=30.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--out-dir", required=True, help="Directory for generated audio and metadata.")
    parser.add_argument("--tos-bucket", help="Optional TOS bucket name for automatic upload.")
    parser.add_argument("--tos-region", help="Optional TOS region, for example cn-beijing.")
    parser.add_argument("--tos-prefix", default="tts-audio", help="Object key prefix when uploading to TOS.")
    parser.add_argument("--tos-public-base-url", help="Optional public base URL or custom domain for direct links.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = os.environ.get("AUDIO_TTS_API_KEY") or os.environ.get("WUYINKEJI_API_KEY")
    if not api_key:
        print("AUDIO_TTS_API_KEY or WUYINKEJI_API_KEY is not set", file=sys.stderr)
        return 1

    payload = {
        "text": args.text,
        "voice_id": args.voice_id,
        "speed": str(args.speed),
        "vol": str(args.vol),
        "language_boost": args.language_boost,
    }
    submit_response = submit_task(api_key, payload)
    task_id = ((submit_response.get("data") or {}).get("id") if isinstance(submit_response.get("data"), dict) else None)
    if not task_id:
        raise RuntimeError(f"TTS submit response missing task id: {json.dumps(submit_response, ensure_ascii=False)}")

    deadline = time.time() + args.timeout
    final_detail: dict | None = None
    while time.time() < deadline:
        detail = fetch_detail(api_key, task_id)
        final_detail = detail
        data = (detail or {}).get("data") or {}
        status = data.get("status")
        print(json.dumps({"event": "polled", "task_id": task_id, "status": status}, ensure_ascii=False), flush=True)
        if status in (2, 3):
            break
        time.sleep(args.poll_interval)

    if final_detail is None:
        raise RuntimeError("TTS polling did not return any detail response.")

    detail_data = (final_detail.get("data") or {})
    status = detail_data.get("status")
    if status != 2:
        raise RuntimeError(f"TTS task not successful: {json.dumps(final_detail, ensure_ascii=False)}")

    result = detail_data.get("result")
    if isinstance(result, list) and result:
        audio_url = result[0]
    elif isinstance(result, str):
        audio_url = result
    else:
        raise RuntimeError(f"TTS result missing audio url: {json.dumps(final_detail, ensure_ascii=False)}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify_filename(args.text)
    raw_bytes = fetch_binary(audio_url)
    audio_bytes, audio_suffix, extracted_member_name = extract_audio_payload(raw_bytes, audio_url)
    audio_path = out_dir / f"{stem}{audio_suffix}"
    metadata_path = out_dir / f"{stem}.json"
    audio_path.write_bytes(audio_bytes)

    tos_access_key_id = (
        os.environ.get("TOS_ACCESS_KEY_ID")
        or os.environ.get("VOLCENGINE_TOS_ACCESS_KEY_ID")
        or os.environ.get("TOS_AK")
    )
    tos_secret_access_key = (
        os.environ.get("TOS_SECRET_ACCESS_KEY")
        or os.environ.get("VOLCENGINE_TOS_SECRET_ACCESS_KEY")
        or os.environ.get("TOS_SK")
    )
    tos_bucket = args.tos_bucket or os.environ.get("TOS_BUCKET")
    tos_region = args.tos_region or os.environ.get("TOS_REGION")
    tos_public_base_url = args.tos_public_base_url or os.environ.get("TOS_PUBLIC_BASE_URL")
    tos_prefix = (args.tos_prefix or "tts-audio").strip("/ ")

    uploaded_audio_url = None
    tos_object_key = None
    if any([tos_access_key_id, tos_secret_access_key, tos_bucket, tos_region]):
        missing = [
            name
            for name, value in [
                ("TOS_ACCESS_KEY_ID", tos_access_key_id),
                ("TOS_SECRET_ACCESS_KEY", tos_secret_access_key),
                ("TOS_BUCKET", tos_bucket),
                ("TOS_REGION", tos_region),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(f"TOS upload requested but missing configuration: {', '.join(missing)}")

        timestamp_part = datetime.now(timezone.utc).strftime("%Y%m%d/%H%M%S")
        tos_object_key = f"{tos_prefix}/{timestamp_part}-{audio_path.name}"
        content_type = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
        put_object_to_tos(
            access_key_id=tos_access_key_id,
            secret_access_key=tos_secret_access_key,
            bucket=tos_bucket,
            region=tos_region,
            object_key=tos_object_key,
            payload=audio_bytes,
            content_type=content_type,
        )
        uploaded_audio_url = build_public_tos_url(
            tos_bucket,
            tos_region,
            tos_object_key,
            custom_base=tos_public_base_url,
        )

    metadata = {
        "audio_file": str(audio_path),
        "metadata_file": str(metadata_path),
        "task_id": task_id,
        "voice_id": args.voice_id,
        "speed": str(args.speed),
        "vol": str(args.vol),
        "language_boost": args.language_boost,
        "audio_url": audio_url,
        "downloaded_payload_suffix": audio_suffix,
        "archive_member_name": extracted_member_name,
        "status": status,
        "message": detail_data.get("message"),
        "updated_at": detail_data.get("updated_at"),
        "uploaded_audio_url": uploaded_audio_url,
        "tos_bucket": tos_bucket,
        "tos_region": tos_region,
        "tos_object_key": tos_object_key,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "audio_file": str(audio_path),
                "metadata_file": str(metadata_path),
                "task_id": task_id,
                "voice_id": args.voice_id,
                "audio_url": audio_url,
                "uploaded_audio_url": uploaded_audio_url,
                "tos_object_key": tos_object_key,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
