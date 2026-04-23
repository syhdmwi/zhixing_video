#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VENDOR_DIR = Path(__file__).resolve().parents[2] / ".vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

try:
    import tos  # type: ignore
except ImportError:
    tos = None


CLONE_URL = "https://api.wuyinkeji.com/api/voice/clone"


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout: int = 120,
) -> dict:
    request_headers = {"Content-Type": "application/json;charset=utf-8"}
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


def submit_clone(api_key: str, payload: dict) -> dict:
    return http_json(
        CLONE_URL,
        method="POST",
        headers={"Authorization": api_key},
        body=payload,
    )


def slugify_filename(text: str) -> str:
    text = text.strip()
    if not text:
        return "voice-clone-audio"
    compact = re.sub(r"\s+", "-", text[:24])
    safe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "", compact)
    return safe or "voice-clone-audio"


def build_tos_host(bucket: str, region: str) -> str:
    return f"{bucket}.tos-{region}.volces.com"


def build_public_tos_url(bucket: str, region: str, object_key: str, custom_base: str | None = None) -> str:
    quoted_key = urllib.parse.quote(object_key, safe="/-_.~")
    if custom_base:
        return f"{custom_base.rstrip('/')}/{quoted_key}"
    return f"https://{build_tos_host(bucket, region)}/{quoted_key}"


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clone a voice from reference audio and render local audio.")
    parser.add_argument("--audio-url", required=True, help="Reference audio URL for voice cloning.")
    parser.add_argument("--text", required=True, help="Input text to read with the cloned voice.")
    parser.add_argument("--name", help="Optional clone display name.")
    parser.add_argument("--out-dir", required=True, help="Directory for generated audio and metadata.")
    parser.add_argument("--tos-bucket", help="Optional TOS bucket name for automatic upload.")
    parser.add_argument("--tos-region", help="Optional TOS region, for example cn-beijing.")
    parser.add_argument("--tos-prefix", default="voice-clone-audio", help="Object key prefix when uploading to TOS.")
    parser.add_argument("--tos-public-base-url", help="Optional public base URL or custom domain for direct links.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = os.environ.get("VOICE_CLONE_API_KEY") or os.environ.get("WUYINKEJI_API_KEY")
    if not api_key:
        print("VOICE_CLONE_API_KEY or WUYINKEJI_API_KEY is not set", file=sys.stderr)
        return 1

    payload = {
        "audio_url": args.audio_url,
        "text": args.text,
    }
    if args.name:
        payload["name"] = args.name

    response = submit_clone(api_key, payload)
    if int(response.get("code", 0)) != 200:
        raise RuntimeError(f"Voice clone request failed: {json.dumps(response, ensure_ascii=False)}")

    data = response.get("data") or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Voice clone response missing data object: {json.dumps(response, ensure_ascii=False)}")

    demo_audio_url = data.get("demo_audio")
    voice_id = data.get("voice_id")
    if not isinstance(demo_audio_url, str) or not demo_audio_url.startswith("http"):
        raise RuntimeError(f"Voice clone response missing demo_audio: {json.dumps(response, ensure_ascii=False)}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem_source = args.name or args.text
    stem = slugify_filename(stem_source)
    suffix = Path(urllib.parse.urlparse(demo_audio_url).path).suffix.lower() or ".mp3"
    audio_bytes = fetch_binary(demo_audio_url)
    audio_path = out_dir / f"{stem}{suffix}"
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
    tos_prefix = (args.tos_prefix or "voice-clone-audio").strip("/ ")

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
        "clone_name": args.name,
        "text": args.text,
        "reference_audio_url": args.audio_url,
        "voice_id": voice_id,
        "demo_audio_url": demo_audio_url,
        "uploaded_audio_url": uploaded_audio_url,
        "tos_bucket": tos_bucket,
        "tos_region": tos_region,
        "tos_object_key": tos_object_key,
        "raw_response": response,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "audio_file": str(audio_path),
                "metadata_file": str(metadata_path),
                "voice_id": voice_id,
                "demo_audio_url": demo_audio_url,
                "uploaded_audio_url": uploaded_audio_url,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
