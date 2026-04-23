---
name: ai-video-avatar-track
description: 当用户要单独制作数字人生成结果时使用这个 skill。它适用于即梦 OmniHuman 1.5、蝉镜数字人和速创 Digital_Humans，并负责素材校验、真实提交、轮询查询和结果展示。
---

# AI Video Avatar Track

## Overview

这个 skill 只负责数字人生成阶段，不负责 B-roll 生图、图生视频，也不负责最终剪辑。目标是在用户提供可用素材后，直接进入真实数字人生成。

## Supported Tools

- `即梦 OmniHuman 1.5`
- `蝉镜数字人`
- `Digital_Humans（速创API）`

## Inputs

- 音频链接
- 正面人物视频链接

## Core Rules

- 当全部画面视频已经生成完成后，应主动询问用户是否需要制作数字人
- 如果用户需要数字人，再提示用户上传或提供音频和正面人物视频
- 如果用户没有成品音频、但想用自己的声音读文案，应先进入 `ai-video-voice-clone`
- 如果用户没有成品音频、且只需要平台预设音色，应先进入 `ai-video-voice-tts`
- 当前速创接口要求 `audioUrl` 和 `videoUrl` 为公网可访问链接
- 当前速创接口文档写明 `videoUrl` 时长不得低于 10 秒
- 当前生成阶段不讨论“数字人出镜策略”或最终剪辑使用方式
- 提交前先校验素材链接是否为真实直链
- 校验通过后直接提交，不额外混入剪辑层参数
- 所有轮询中的进度汇报，默认遵循总控里的统一规则：[references/polling-progress-rules.md](../ai-short-video-pipeline/references/polling-progress-rules.md)

## Output

至少输出：

- `digital_human_queue`
- `generation_notes`
- `rendered_videos_for_review`

## Execution

如果用户已经给出音频和人物视频链接，当前脚本层可直接执行：

- `scripts/digital_humans_batch.py`

默认轮询规则：

- 每 `30` 秒查一次
- 最多查 `10` 分钟

## Default Prompt After B-roll Videos

当全部画面视频已经生成完成后，默认下一句要主动问：

- `是否需要继续制作数字人视频轨？如果需要，请上传音频和正面人物视频链接。`

## References

- 队列模板： [references/avatar-queue-example.json](./references/avatar-queue-example.json)
- 脚本用法： [references/script-usage.md](./references/script-usage.md)
