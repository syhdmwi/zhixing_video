---
name: ai-video-generate-videos
description: 当用户已经有静帧图片和已确认的图生视频镜头运动模板，接下来要真实提交视频生成任务时使用这个 skill。它负责先让用户选择视频平台，再把任务提交到对应 provider。当前支持 grok 和 seedance 两种 provider 入口，二者都已接入真实执行链路。
---

# AI Video Generate Videos

## Overview

这个 skill 负责“已确认静帧 + 已确认镜头运动模板 -> 真实提交视频生成任务”这一段。

它不负责：

- 生图
- 重写镜头运动模板
- 数字人视频轨
- 最终剪辑

它的职责是：

1. 先让用户选择视频 provider
2. 把图片和镜头运动模板转成 provider 可执行的任务
3. 提交任务
4. 轮询结果
5. 成功后默认直接展示视频结果或结果链接给用户确认

## Supported Providers

- `grok`
- `seedance`

## Provider Choice Rule

进入真实视频生成前，必须先问用户：

- 这次要用 `grok`，还是 `seedance`

不要替用户默认切 provider，除非用户已经明确指定。

如果用户选择 `grok`，还要继续问：

- 是否要使用 `grok视频模版套用00`

如果用户同意，就优先按该模板生成视频提示词；如果用户不要，再按当前镜头单独写。
这里的模板不是写死“龙虾”这类单一角色，而是要先识别当前文案里反复出现、需要保持一致的高频主体，再动态代入。

## Current Provider Status

- `grok`
  已按一加 `POST /v1/chat/completions` 流式接口接入真实执行链路。
  并已保存一个可复用模板：`grok视频模版套用00`
  该模板按“动态高频主体”方式套用，不应写死某个固定角色名。
- `seedance`
  已按火山方舟视频生成 API 接入真实执行链路，并已完成真实提交与查询验证。

## Required Inputs

- 已确认的静帧图片
- 每张图对应的 `shot_id`
- 已确认的图生视频镜头运动模板
- provider 选择结果
- 目标比例和尺寸
- 是否先跑测试批次

## Core Rules

- 先选 provider，再提交任务
- 默认先跑测试批次，再决定是否全量生成
- 图生视频提示词默认沿用固定镜头运动模板
- 每条视频任务默认附带固定稳定性模板：`保持人物/场景/主要角色不变形，主体保持原地静止，不要行走、不要跟拍人物，只有相机缓慢平移或拉远`
- `grok` 默认优先使用英文强约束提示词，避免模型把镜头移动误解成主体走动
- 生成成功后，默认直接展示结果，不只给任务号
- 如果 provider 任务长时间卡住，应保留历史 task_id 并标记状态

## Workflow

### 1. Confirm Motion Batch Is Approved

只有当静帧和镜头运动模板都已经确认后，才进入本 skill。

### 2. Ask Provider First

先问用户：

- 这次要用 `grok`，还是 `seedance`

如果用户选择 `grok`，继续问：

- 是否要直接套用 `grok视频模版套用00`

如果套用 `grok视频模版套用00`，先识别：

- 当前镜头的主主体是谁
- 当前镜头里是否还有第二个反复出现的主要角色或关键物
- 当前镜头必须锁定的识别特征是什么

再把这些内容代入模板，不要直接复制旧镜头里的“龙虾”或其他固定对象。

### 3. Build Provider Queue

每条任务至少包含：

- `shot_id`
- `provider`
- `model`
- `source_image_url`
- `motion_prompt`
- `size`

### 4. Submit And Poll

当前脚本层：

- `scripts/video_generation_router.py`

### 5. Show Generated Results

如果环境支持展示视频或返回视频链接，默认按 `shot_id` 顺序展示结果给用户确认。

## Output

至少输出：

- `provider`
- `generation_queue`
- `execution_notes`
- `rendered_videos_for_review`

## References

- provider 队列模板： [references/provider-queue-example.json](./references/provider-queue-example.json)
- grok 接入说明： [references/grok-provider-notes.md](./references/grok-provider-notes.md)
- grok 固定模板： [references/grok-video-template-00.md](./references/grok-video-template-00.md)
- seedance 接入说明： [references/seedance-provider-notes.md](./references/seedance-provider-notes.md)
