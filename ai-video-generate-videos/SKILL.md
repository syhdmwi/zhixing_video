---
name: ai-video-generate-videos
description: 当用户已经有静帧图片和已确认的图生视频镜头运动模板，接下来要真实提交视频生成任务时使用这个 skill。它当前默认使用 grok 提交视频任务；seedance 暂时停用。
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

1. 判断当前可用视频 provider
2. 把图片和镜头运动模板转成 provider 可执行的任务
3. 提交任务
4. 轮询结果
5. 成功后默认直接展示视频结果或结果链接给用户确认

## Supported Providers

- `grok`
- `seedance`：暂时停用

## Provider Routing Rule

进入真实视频生成前，不再默认多问用户选择 provider。

默认按这套规则自动判断：

1. 当前默认只启用 `grok`
2. 如果 `YIJIA_API_KEY` 可用，就直接用 `grok`
3. `seedance` 当前不参与自动路由
4. `grok` 失败时，先直接报错和展示结果，不自动回退到 `seedance`

只有当后续重新启用 `seedance` 时，才恢复双 provider 路由。

如果最终路由到 `grok`，默认直接套用 `grok视频模版套用00`，不再额外追问。
这里的模板不是写死“龙虾”这类单一角色，而是要先识别当前文案里反复出现、需要保持一致的高频主体，再动态代入。

## Current Provider Status

- `grok`
  已按一加 `POST /v1/chat/completions` 流式接口接入真实执行链路。
  并已保存一个可复用模板：`grok视频模版套用00`
  该模板按“动态高频主体”方式套用，不应写死某个固定角色名。
- `seedance`
  当前接口能力和文档仍保留，但这条链路已暂时停用，不参与自动路由，也不参与回退。

## Required Inputs

- 已确认的静帧图片
- 已确认静帧图片的公网 URL；如果只有本地图片文件且已配置 TOS，先自动上传到 TOS 再提交
- 每张图对应的 `shot_id`
- 已确认的图生视频镜头运动模板
- 目标比例和尺寸
- 是否先跑测试批次

## Core Rules

- 默认使用 `grok`，再提交任务
- 默认先跑测试批次，再决定是否全量生成
- 图生视频接口需要公网图片 URL。用户如果提供本地图片文件，且已配置 TOS，默认先自动上传到 TOS，得到公网直链后再提交给视频模型
- 只有 TOS 配置缺失时，才提示用户提供公网可访问图片 URL
- 图生视频提示词默认沿用固定镜头运动模板
- 每条视频任务默认附带固定稳定性模板：`保持人物/场景/主要角色不变形，主体保持原地静止，不要行走、不要跟拍人物，只有相机缓慢平移或拉远`
- `grok` 默认优先使用英文强约束提示词，避免模型把镜头移动误解成主体走动
- 生成成功后，默认直接展示结果，不只给任务号
- 如果 provider 任务长时间卡住，应保留历史 task_id 并标记状态
- 所有轮询中的进度汇报，默认遵循总控里的统一规则：[references/polling-progress-rules.md](../ai-short-video-pipeline/references/polling-progress-rules.md)

## Workflow

### 1. Confirm Motion Batch Is Approved

只有当静帧和镜头运动模板都已经确认后，才进入本 skill。

### 2. Auto Route Provider First

先根据当前可用 key 判断 provider。

当前默认直接路由到 `grok`。

如果自动路由到 `grok`，默认直接套用 `grok视频模版套用00`。

套用 `grok视频模版套用00` 时，先识别：

- 当前镜头的主主体是谁
- 当前镜头里是否还有第二个反复出现的主要角色或关键物
- 当前镜头必须锁定的识别特征是什么

再把这些内容代入模板，不要直接复制旧镜头里的“龙虾”或其他固定对象。

如果 `grok` 提交失败，当前直接返回失败结果，不自动回退到 `seedance`。

### 3. Build Provider Queue

每条任务至少包含：

- `shot_id`
- `provider`
- `model`
- `source_image_url`
- `motion_prompt`
- `size`

如果 `source_image_url` 对应的是本地图片路径，不要直接提交给 provider；先按总控公网资源规则上传到 TOS。

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
- seedance 停用说明： [references/seedance-provider-notes.md](./references/seedance-provider-notes.md)
