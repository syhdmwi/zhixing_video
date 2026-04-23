#!/usr/bin/env python3
from __future__ import annotations

import argparse
import mimetypes
import os
import time
from pathlib import Path
from urllib.parse import quote

try:
    import tos  # type: ignore
except ImportError:  # pragma: no cover
    tos = None


def build_public_url(bucket: str, region: str, object_key: str, public_base_url: str | None = None) -> str:
    if public_base_url:
        return f"{public_base_url.rstrip('/')}/{quote(object_key)}"
    return f"https://{bucket}.tos-{region}.volces.com/{quote(object_key)}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a local asset to Volcengine TOS and print a public URL.")
    parser.add_argument("--file", required=True, help="Local file path to upload.")
    parser.add_argument("--prefix", default="ai-short-video-assets", help="TOS object key prefix.")
    parser.add_argument("--out", help="Optional text file to write the public URL.")
    parser.add_argument("--tos-bucket", help="TOS bucket name. Defaults to TOS_BUCKET.")
    parser.add_argument("--tos-region", help="TOS region, for example cn-beijing. Defaults to TOS_REGION.")
    parser.add_argument("--tos-public-base-url", help="Optional public base URL or custom domain.")
    args = parser.parse_args()

    if tos is None:
        raise RuntimeError("Official TOS SDK is not available. Install the `tos` package first.")

    path = Path(args.file).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Local file not found: {path}")

    access_key_id = (
        os.environ.get("TOS_ACCESS_KEY_ID")
        or os.environ.get("VOLCENGINE_TOS_ACCESS_KEY_ID")
        or os.environ.get("TOS_AK")
    )
    secret_access_key = (
        os.environ.get("TOS_SECRET_ACCESS_KEY")
        or os.environ.get("VOLCENGINE_TOS_SECRET_ACCESS_KEY")
        or os.environ.get("TOS_SK")
    )
    bucket = args.tos_bucket or os.environ.get("TOS_BUCKET")
    region = args.tos_region or os.environ.get("TOS_REGION")
    public_base_url = args.tos_public_base_url or os.environ.get("TOS_PUBLIC_BASE_URL")

    missing = [
        name
        for name, value in [
            ("TOS_ACCESS_KEY_ID", access_key_id),
            ("TOS_SECRET_ACCESS_KEY", secret_access_key),
            ("TOS_BUCKET", bucket),
            ("TOS_REGION", region),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(f"TOS upload requested but missing configuration: {', '.join(missing)}")

    object_key = f"{args.prefix.strip('/')}/{int(time.time())}-{path.name}"
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    client = tos.TosClientV2(
        ak=access_key_id,
        sk=secret_access_key,
        endpoint=f"tos-{region}.volces.com",
        region=region,
    )
    with path.open("rb") as file_obj:
        client.put_object(bucket, object_key, content=file_obj, content_type=content_type)

    url = build_public_url(bucket, region, object_key, public_base_url)
    if args.out:
        Path(args.out).write_text(url + "\n", encoding="utf-8")
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
