---
name: ai-video-avatar-track
description: 数字人生成实现模块当前停用，不对用户开放、不执行；实现保留供日后恢复。
---

> ⛔ 数字人功能当前停用，不对用户开放、不执行；实现保留供日后恢复。

# AI Video Avatar Track

## Overview

这个 skill 当前停用。以下接口、脚本和队列说明仅作为实现留档，不作为用户可用入口；任何用户侧数字人请求都应由总控回复“该功能当前暂未开放”。

## Supported Tools

- `即梦 OmniHuman 1.5`
- `蝉镜数字人`
- `速创 Digital_Humans`

## Inputs

- 音频链接
- 正面人物视频链接
- 或用户上传的本地音频文件和本地正面人物视频文件

## Core Rules

- 不主动询问用户是否需要制作数字人
- 不提示用户上传音频或正面人物视频来制作数字人
- 如果用户要求做数字人，固定回复：`该功能当前暂未开放。`
- 如果用户没有成品音频、但想用自己的声音读文案，不进入 `ai-video-voice-clone`，固定回复：`该功能当前暂未开放。`
- 如果用户没有成品音频、且只需要平台预设音色，应先进入 `ai-video-voice-tts`
- 当前速创接口要求 `audioUrl` 和 `videoUrl` 为公网可访问链接
- 以下素材上传与直链规则仅作为恢复时的实现参考，当前不对用户触发
- 恢复前不得要求用户补充 TOS 配置或公网 URL 来制作数字人
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

脚本保留但当前不执行：

- `scripts/digital_humans_batch.py`

默认轮询规则：

- 每 `30` 秒查一次
- 最多查 `10` 分钟

## Default Prompt After B-roll Videos

当前不再使用这一阶段；全部画面视频生成完成后应进入 `jianying_export_decision`，询问是否导出剪映手动交付包。


## References

- 队列模板： [references/avatar-queue-example.json](./references/avatar-queue-example.json)
- 脚本用法： [references/script-usage.md](./references/script-usage.md)
