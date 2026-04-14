#!/usr/bin/env python3
"""
Estimate narration duration and shot count for the ai-short-video-pipeline skill.

Defaults:
- Chinese: 230 characters per minute
- English: 150 words per minute
- Shot density: 11 shots per minute
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass
class ShotPlan:
    duration_seconds: int
    duration_minutes: float
    shot_count: int
    source: str


def estimate_from_minutes(minutes: float, shot_density: float) -> ShotPlan:
    duration_seconds = math.ceil(minutes * 60)
    shot_count = math.ceil(minutes * shot_density)
    return ShotPlan(
        duration_seconds=duration_seconds,
        duration_minutes=round(duration_seconds / 60, 2),
        shot_count=shot_count,
        source="minutes",
    )


def estimate_from_chinese_chars(chars: int, chars_per_minute: float, shot_density: float) -> ShotPlan:
    minutes = chars / chars_per_minute
    plan = estimate_from_minutes(minutes, shot_density)
    plan.source = "chinese_chars"
    return plan


def estimate_from_english_words(words: int, words_per_minute: float, shot_density: float) -> ShotPlan:
    minutes = words / words_per_minute
    plan = estimate_from_minutes(minutes, shot_density)
    plan.source = "english_words"
    return plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Estimate short-video duration and shot count.")
    parser.add_argument("--minutes", type=float, help="Known narration duration in minutes.")
    parser.add_argument("--seconds", type=float, help="Known narration duration in seconds.")
    parser.add_argument("--cn-chars", type=int, help="Chinese character count.")
    parser.add_argument("--en-words", type=int, help="English word count.")
    parser.add_argument("--chars-per-minute", type=float, default=230.0, help="Chinese chars per minute.")
    parser.add_argument("--words-per-minute", type=float, default=150.0, help="English words per minute.")
    parser.add_argument("--shot-density", type=float, default=11.0, help="Shots per minute.")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    provided = [args.minutes is not None, args.seconds is not None, args.cn_chars is not None, args.en_words is not None]
    if sum(provided) != 1:
        parser.error("Provide exactly one of --minutes, --seconds, --cn-chars, or --en-words.")

    if args.minutes is not None:
        plan = estimate_from_minutes(args.minutes, args.shot_density)
    elif args.seconds is not None:
        plan = estimate_from_minutes(args.seconds / 60, args.shot_density)
        plan.source = "seconds"
    elif args.cn_chars is not None:
        plan = estimate_from_chinese_chars(args.cn_chars, args.chars_per_minute, args.shot_density)
    else:
        plan = estimate_from_english_words(args.en_words, args.words_per_minute, args.shot_density)

    if args.json:
        print(json.dumps(asdict(plan), ensure_ascii=False, indent=2))
    else:
        print(f"source: {plan.source}")
        print(f"duration_seconds: {plan.duration_seconds}")
        print(f"duration_minutes: {plan.duration_minutes}")
        print(f"shot_count: {plan.shot_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
