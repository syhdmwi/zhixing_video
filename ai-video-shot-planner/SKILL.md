---
name: ai-video-shot-planner
description: 当用户要把文案拆成镜头表时使用这个 skill。它负责估算时长、按每分钟 11 个镜头计算分镜数量、拆解 narration 节奏，并为数字人主讲镜头与 B-roll 镜头做分配。
---

# AI Video Shot Planner

## Overview

这个 skill 只负责前期策划，不负责写生图提示词或图生视频提示词。目标是把文案变成清晰的镜头表，并提前划分哪些镜头属于数字人轨，哪些镜头属于画面轨。

## When To Use

- 用户给出文案，想先拆分镜
- 用户还没开始生图，只需要镜头规划
- 用户需要判断数字人全程出镜还是部分镜头出镜

## Core Rules

- 镜头密度默认是每分钟 `11` 个镜头
- 时长优先使用用户给定时长；否则按文案估算
- 中文默认 `230` 字/分钟，英文默认 `150` 词/分钟
- 开头 3 秒优先给钩子镜头
- 一个镜头只表达一个主要信息点

## Required Output

每个镜头至少包含：

- `shot_id`
- `time_range`
- `narration_excerpt`
- `message_goal`
- `frame_type`，只能是 `avatar`、`b-roll`、`split`
- `reason`

## Avatar Allocation

如果用户没指定数字人出镜策略，默认：

- 开头镜头优先考虑数字人建立真人感
- 中段复杂说明优先允许 B-roll 覆盖
- 结尾 CTA 优先回到数字人收口

## Tools

可使用兄弟 skill 中的估算脚本：

- `../ai-short-video-pipeline/scripts/calc_shot_plan.py`
