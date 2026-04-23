#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image

DEFAULT_MOTION_PRESETS = [
    "subtle_pan_left",
    "subtle_pan_right",
    "subtle_pan_up",
    "subtle_pan_down",
    "subtle_pushin",
    "subtle_pullback",
]


def load_queue(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Queue file must contain a top-level JSON array.")
    required = {"shot_id", "source_image", "duration_seconds", "output_name"}
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Queue item #{index} must be an object.")
        missing = required - set(item.keys())
        if missing:
            raise ValueError(f"Queue item #{index} missing fields: {sorted(missing)}")
    return data


def assign_motion_presets(queue: list[dict]) -> list[dict]:
    rng = random.SystemRandom()
    previous: str | None = None
    assigned: list[dict] = []
    for item in queue:
        preset = str(item.get("motion_preset", "auto"))
        if not preset or preset == "auto":
            candidates = [candidate for candidate in DEFAULT_MOTION_PRESETS if candidate != previous]
            preset = rng.choice(candidates)
            item = {**item, "motion_preset": preset}
        previous = preset
        assigned.append(item)
    return assigned


def frames_for(duration_seconds: float, fps: int) -> int:
    return max(1, int(round(duration_seconds * fps)))


def split_resolution(resolution: str) -> tuple[int, int]:
    width_str, height_str = resolution.lower().split("x", 1)
    return int(width_str), int(height_str)


def motion_progress_for(frame_index: int, total_frames: int, motion_curve: str) -> float:
    if total_frames <= 1:
        progress = 1.0
    else:
        progress = frame_index / (total_frames - 1)
    if motion_curve == "linear":
        return progress
    elif motion_curve == "ease_out":
        return 1 - math.pow(1 - progress, 2)
    raise ValueError(f"Unsupported motion_curve: {motion_curve}")


def frame_transform(
    preset: str,
    zoom_strength: float,
    pan_strength: float,
    progress: float,
) -> tuple[float, float, float]:
    if preset == "subtle_pullback":
        zoom = 1.0 + zoom_strength * (1.0 - progress)
        x_factor = 0.5
        y_factor = 0.5
    elif preset == "subtle_pushin":
        zoom = 1.0 + zoom_strength * progress
        x_factor = 0.5
        y_factor = 0.5
    elif preset == "subtle_pan_left":
        zoom = max(1.04, 1.0 + pan_strength * 4)
        x_factor = 0.5 * (1.0 - progress)
        y_factor = 0.5
    elif preset == "subtle_pan_right":
        zoom = max(1.04, 1.0 + pan_strength * 4)
        x_factor = 0.5 + 0.5 * progress
        y_factor = 0.5
    elif preset == "subtle_pan_up":
        zoom = max(1.04, 1.0 + pan_strength * 4)
        x_factor = 0.5
        y_factor = 0.5 * (1.0 - progress)
    elif preset == "subtle_pan_down":
        zoom = max(1.04, 1.0 + pan_strength * 4)
        x_factor = 0.5
        y_factor = 0.5 + 0.5 * progress
    else:
        raise ValueError(f"Unsupported motion_preset: {preset}")
    return zoom, x_factor, y_factor


def render_frames(item: dict, out_dir: Path, default_fps: int) -> tuple[list[str], Path]:
    source = Path(str(item["source_image"]))
    duration_seconds = float(item["duration_seconds"])
    fps = int(item.get("fps", default_fps))
    resolution = str(item.get("resolution", "1920x1080"))
    zoom_strength = float(item.get("zoom_strength", 0.10))
    pan_strength = float(item.get("pan_strength", 0.10))
    motion_curve = str(item.get("motion_curve", "linear"))
    total_frames = frames_for(duration_seconds, fps)
    width, height = split_resolution(resolution)
    output_path = out_dir / str(item["output_name"])
    frames_dir = out_dir / f"{item['shot_id']}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    source_image = Image.open(source).convert("RGB")
    src_w, src_h = source_image.size
    cover_scale = max(width / src_w, height / src_h)
    frame_pattern = frames_dir / "frame-%05d.jpg"

    for frame_index in range(total_frames):
        progress = motion_progress_for(frame_index, total_frames, motion_curve)
        zoom, x_factor, y_factor = frame_transform(str(item["motion_preset"]), zoom_strength, pan_strength, progress)
        preset = str(item["motion_preset"])
        # Push/pull shots are more prone to shimmer because every frame is resampled.
        # Render those frames on a larger internal canvas first, then scale down.
        internal_scale = 4 if preset in {"subtle_pullback", "subtle_pushin"} else 1
        internal_w = width * internal_scale
        internal_h = height * internal_scale
        internal_cover_scale = max(internal_w / src_w, internal_h / src_h)

        scaled_w = max(internal_w, int(round(src_w * internal_cover_scale * zoom)))
        scaled_h = max(internal_h, int(round(src_h * internal_cover_scale * zoom)))
        resized = source_image.resize((scaled_w, scaled_h), Image.Resampling.BICUBIC)
        overflow_x = max(0, scaled_w - internal_w)
        overflow_y = max(0, scaled_h - internal_h)
        crop_x = int(round(overflow_x * max(0.0, min(1.0, x_factor))))
        crop_y = int(round(overflow_y * max(0.0, min(1.0, y_factor))))
        crop_x = min(crop_x, overflow_x)
        crop_y = min(crop_y, overflow_y)
        frame = resized.crop((crop_x, crop_y, crop_x + internal_w, crop_y + internal_h))
        if internal_scale > 1:
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
        frame.save(frames_dir / f"frame-{frame_index + 1:05d}.jpg", quality=95, subsampling=0)

    encode_cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frame_pattern),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output_path),
    ]
    return encode_cmd, output_path


def write_concat_file(rendered: list[Path], concat_path: Path) -> None:
    lines = [f"file '{path.as_posix()}'" for path in rendered]
    concat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a keyframed edit track from still images with FFmpeg.")
    parser.add_argument("--queue-file", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--fps", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    queue = assign_motion_presets(load_queue(args.queue_file))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = shutil.which("ffmpeg")
    dry_run = args.dry_run or ffmpeg_path is None

    command_plan: list[dict] = []
    rendered_paths: list[Path] = []

    for item in queue:
        cmd, output_path = render_frames(item, args.out_dir, args.fps)
        command_plan.append(
            {
                "shot_id": item["shot_id"],
                "motion_preset": item["motion_preset"],
                "command": cmd,
                "output_path": str(output_path),
                "status": "planned" if dry_run else "pending",
            }
        )
        rendered_paths.append(output_path)

    concat_path = args.out_dir / "concat.txt"
    final_video_path = args.out_dir / "final-keyframe-track.mp4"
    write_concat_file(rendered_paths, concat_path)

    if not dry_run:
        for entry in command_plan:
            subprocess.run(entry["command"], check=True)
            entry["status"] = "rendered"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-c",
                "copy",
                str(final_video_path),
            ],
            check=True,
        )

    result = {
        "edit_mode": "ai_keyframe_edit",
        "ffmpeg_available": ffmpeg_path is not None,
        "dry_run": dry_run,
        "generation_queue": command_plan,
        "concat_plan": {
            "concat_file": str(concat_path),
            "final_video_path": str(final_video_path),
        },
    }
    (args.out_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
