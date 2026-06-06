#!/usr/bin/env python3
"""Build a Jianying manual-import handoff package.

The script writes only portable handoff files:
timeline.csv, subtitles.srt, and delivery-manifest.json.
It does not read or write Jianying draft directories.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TRACKS = {"avatar", "broll"}


@dataclass
class Shot:
    order: int
    shot_id: str
    start: float
    end: float
    duration: float
    narration: str
    video_file: str
    audio_file: str
    track: str
    transition: str
    bgm_note: str


def parse_time(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"Unsupported time value: {value!r}")

    text = value.strip().replace(",", ".")
    if not text:
        raise ValueError("Empty time value")

    parts = text.split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    except ValueError as exc:
        raise ValueError(f"Invalid time value: {value!r}") from exc

    raise ValueError(f"Invalid time value: {value!r}")


def parse_time_range(value: str) -> tuple[float, float]:
    pieces = re.split(r"\s*(?:-->|-|~|to)\s*", value.strip(), maxsplit=1)
    if len(pieces) != 2:
        raise ValueError(f"Invalid time_range: {value!r}")
    start = parse_time(pieces[0])
    end = parse_time(pieces[1])
    if end <= start:
        raise ValueError(f"time_range end must be after start: {value!r}")
    return start, end


def format_srt_time(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def load_payload(path: Path) -> tuple[str, list[dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if isinstance(payload, list):
        return path.stem, payload
    if isinstance(payload, dict):
        shots = payload.get("shots")
        if not isinstance(shots, list):
            raise ValueError("Input object must contain a shots array")
        return str(payload.get("project_id") or path.stem), shots
    raise ValueError("Input must be a shot array or an object with shots")


def normalize_shots(raw_shots: list[dict[str, Any]]) -> list[Shot]:
    normalized: list[Shot] = []
    cursor = 0.0

    for index, raw in enumerate(raw_shots, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"Shot #{index} must be an object")

        shot_id = str(raw.get("shot_id") or "").strip()
        if not shot_id:
            raise ValueError(f"Shot #{index} is missing shot_id")

        if raw.get("time_range"):
            start, end = parse_time_range(str(raw["time_range"]))
        else:
            start = parse_time(raw["start"]) if raw.get("start") is not None else cursor
            if raw.get("duration") is None:
                raise ValueError(f"{shot_id} needs duration when time_range is absent")
            end = start + parse_time(raw["duration"])

        duration = round(end - start, 3)
        if duration <= 0:
            raise ValueError(f"{shot_id} duration must be positive")

        track = str(raw.get("track") or "broll").strip()
        if track not in TRACKS:
            raise ValueError(f"{shot_id} track must be one of {sorted(TRACKS)}")

        normalized.append(
            Shot(
                order=index,
                shot_id=shot_id,
                start=round(start, 3),
                end=round(end, 3),
                duration=duration,
                narration=str(raw.get("narration") or "").strip(),
                video_file=str(raw.get("video_file") or "").strip(),
                audio_file=str(raw.get("audio_file") or "").strip(),
                track=track,
                transition=str(raw.get("transition") or "").strip(),
                bgm_note=str(raw.get("bgm_note") or "").strip(),
            )
        )
        cursor = end

    return normalized


def write_timeline(path: Path, shots: list[Shot]) -> None:
    fields = [
        "order",
        "shot_id",
        "start_time",
        "end_time",
        "duration_seconds",
        "track",
        "video_file",
        "audio_file",
        "narration",
        "transition",
        "bgm_note",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for shot in shots:
            writer.writerow(
                {
                    "order": shot.order,
                    "shot_id": shot.shot_id,
                    "start_time": format_srt_time(shot.start),
                    "end_time": format_srt_time(shot.end),
                    "duration_seconds": f"{shot.duration:.3f}",
                    "track": shot.track,
                    "video_file": shot.video_file,
                    "audio_file": shot.audio_file,
                    "narration": shot.narration,
                    "transition": shot.transition,
                    "bgm_note": shot.bgm_note,
                }
            )


def write_srt(path: Path, shots: list[Shot]) -> None:
    blocks: list[str] = []
    for index, shot in enumerate(shots, start=1):
        text = shot.narration or shot.shot_id
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{format_srt_time(shot.start)} --> {format_srt_time(shot.end)}",
                    text,
                ]
            )
        )
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def write_manifest(path: Path, project_id: str, input_path: Path, shots: list[Shot]) -> None:
    manifest = {
        "project_id": project_id,
        "route": "jianying_manual_import",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_file": str(input_path),
        "package_files": {
            "timeline": "timeline.csv",
            "subtitles": "subtitles.srt",
            "manifest": "delivery-manifest.json",
        },
        "shot_count": len(shots),
        "duration_seconds": round(shots[-1].end - shots[0].start, 3) if shots else 0,
        "tracks": {
            "avatar": sum(1 for shot in shots if shot.track == "avatar"),
            "broll": sum(1 for shot in shots if shot.track == "broll"),
        },
        "shots": [asdict(shot) for shot in shots],
        "import_notes": [
            "Manual import only.",
            "Place avatar shots on the speaker/avatar track and broll shots on the visual overlay track.",
            "Import subtitles.srt through Jianying's subtitle import UI.",
        ],
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(input_path: Path, output_dir: Path) -> None:
    project_id, raw_shots = load_payload(input_path)
    shots = normalize_shots(raw_shots)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_timeline(output_dir / "timeline.csv", shots)
    write_srt(output_dir / "subtitles.srt", shots)
    write_manifest(output_dir / "delivery-manifest.json", project_id, input_path, shots)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Jianying manual handoff package.")
    parser.add_argument("--input", required=True, type=Path, help="Shot list JSON file.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory.")
    args = parser.parse_args()

    try:
        build(args.input, args.out_dir)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote handoff package to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
