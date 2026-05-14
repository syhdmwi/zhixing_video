---
name: ai-video-generate-videos
description: 当用户已经有静帧图片和已确认的图生视频动作方案，接下来要真实提交视频生成任务时使用这个 skill。它当前默认使用 grok 提交视频任务；seedance 暂时停用。
---

# AI Video Generate Videos

## Overview

这个 skill 负责“已确认静帧 + 已确认图生视频动作方案 -> 真实提交视频生成任务”这一段。

它不负责：

- 生图
- 重写图生视频动作方案
- 数字人视频轨
- 最终剪辑

它的职责是：

1. 判断当前可用视频生成模型
2. 把图片和图生视频动作方案转成可执行任务
3. 提交任务
4. 轮询结果
5. 成功后默认直接展示视频结果或结果链接给用户确认

## Supported Providers

- `grok`
- `seedance`：暂时停用

## Provider Routing Rule

进入真实视频生成前，不要让普通用户理解 provider。用户侧只需要知道现在进入“图生视频模式”。

默认按这套规则自动判断：

1. 当前默认只启用 `grok`
2. 如果 `YIJIA_API_KEY` 可用，就直接用 `grok`
3. `seedance` 当前不参与自动路由
4. `grok` 失败时，先直接报错和展示结果，不自动回退到 `seedance`

只有当后续重新启用 `seedance` 时，才恢复双 provider 路由。

如果最终路由到 `grok`，默认直接套用 `grok视频模版套用00`，不再额外追问。
这里的模板不是写死“龙虾”这类单一角色，而是要先识别当前文案里反复出现、需要保持一致的高频主体，再动态代入。

对用户展示时，优先用这种话术：

```text
当前进度：
1. 图片已确认
2. 现在进入图生视频模式
3. 我会自动选择当前可用的视频生成模型

接下来会按已确认图片逐张生成视频，不会自动拼接总片。
```

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
- 已确认的图生视频动作方案
- 目标比例和尺寸
- 是否先跑测试批次

## Core Rules

- 默认使用 `grok`，再提交任务
- 默认先跑测试批次，再决定是否全量生成
- 图生视频接口需要公网图片 URL。用户如果提供本地图片文件，且已配置 TOS，默认先自动上传到 TOS，得到公网直链后再提交给视频模型
- 只有 TOS 配置缺失时，才提示用户提供公网可访问图片 URL
- 图生视频提示词默认沿用已确认的 `motion_type` 和 `video_prompt`
- 每条视频任务默认附带固定稳定性模板：`保持人物/场景/主要角色不变形，保持原始画风和构图，主体只做小幅自然动作，不要夸张变形、不要新增角色、不要背景漂移`
- `grok` 默认优先使用英文强约束提示词，避免模型把“小幅自然动作”误解成大幅表演或结构漂移
- 生成成功后，默认直接展示结果，不只给任务号
- 如果 provider 任务长时间卡住，应保留历史 task_id 并标记状态
- 所有轮询中的进度汇报，默认遵循总控里的统一规则：[references/polling-progress-rules.md](../ai-short-video-pipeline/references/polling-progress-rules.md)

## Workflow

### 1. Confirm Motion Batch Is Approved

只有当静帧和图生视频动作方案都已经确认后，才进入本 skill。

如果是用户刚从图片阶段进入视频阶段，优先先展示这个选择：

```text
当前进度：
1. 图片已确认
2. 现在进入视频生成

请选择：
1 图转镜头移动视频模式
2 图生视频模式
```

### 2. Auto Route Provider First

先根据当前可用 key 判断视频生成模型，但不要把这个判断过程暴露给普通用户。

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
- `narration_excerpt`
- `provider`
- `model`
- `source_image_url`
- `motion_type`
- `motion_intensity`
- `video_prompt_cn`
- `video_prompt`
- `size`

如果 `source_image_url` 对应的是本地图片路径，不要直接提交给 provider；先按总控公网资源规则上传到 TOS。

用户侧不要说“请提供公网 URL”，除非 TOS 配置缺失。默认说：

```text
如果图片是本地文件，我会自动转存后再提交视频生成。
```

### 4. Submit And Poll

当前脚本层：

- `scripts/video_generation_router.py`

### 5. Preflight Check For Image-To-Video Prompts

真正提交前，每条镜头都先检查：

- `motion_type` 是否已指定
- `motion_intensity` 是否已指定
- `video_prompt` 是否已生成
- `video_prompt` 是否同时包含：
  - 主体动作
  - 镜头运动
  - 风格保持
  - 负面约束

如果缺任何一项，先回到 `ai-video-motion-prompts` 补齐，不直接提交。

### 5.5 Video Quality Review Loop（视频质量审核回环）

全部视频生成成功、展示给用户之前，先自动运行视频质量审核。

审核内容：
- 角色一致性：人物是否在运动中变形或串脸
- 空间一致性：场景空间是否在运动中跳变
- 运动幅度：是否超出提示词约束（如要求缓慢平移却出现大幅晃动）
- 闪烁/抖动：是否出现不合理的画面闪烁或帧间跳变
- 首帧连续性：视频首帧是否与原始静帧一致

严重程度分级：
- 🔴 必须修改：人物严重变形、场景完全跳变、视频不可用
- 🟡 建议修改：轻微闪烁、运动幅度偏大但可接受
- 🟢 轻微可忽略：色温微变、边缘轻微抖动

如果没有 🔴 问题，直接展示审核报告 + 视频。
如果有 🔴 问题，先展示报告，建议用户先处理。
如果 🔴 问题 ≥ 30%，建议整体重生成该批次。

用户选择自动重生成时，只重生成 🔴 级别镜头，最多重试 2 轮。

详细审核维度和输出格式见 [quality-review-loop.md](../ai-short-video-pipeline/references/quality-review-loop.md)。

### 6. Show Generated Results

如果环境支持展示视频或返回视频链接，默认按 `shot_id` 顺序展示结果给用户确认。

展示时默认同时带上：

- `narration_excerpt`
- `video_prompt_cn`
- 视频结果

不要只展示视频文件或英文 `video_prompt`，避免用户看不懂当前镜头是根据哪句原文和哪条中文动作提示生成的。

展示完成后，固定询问：

```text
视频已生成完成，下面是全部结果。

是否满意，有无需要重新生成的视频？
如果有请输入第几段，并把修改要求一起输入；
如果不需要修改，本轮视频生成完成。
```

## Output

至少输出：

- `provider`
- `generation_queue`
- `execution_notes`
- `rendered_videos_for_review`

## References

- provider 队列模板： [references/provider-queue-example.json](./references/provider-queue-example.json)
- 图生视频提示词规则： [references/image-to-video-prompt-rules.md](./references/image-to-video-prompt-rules.md)
- 动作模板库： [references/motion-template-library.md](./references/motion-template-library.md)
- grok 接入说明： [references/grok-provider-notes.md](./references/grok-provider-notes.md)
- grok 固定模板： [references/grok-video-template-00.md](./references/grok-video-template-00.md)
- seedance 停用说明： [references/seedance-provider-notes.md](./references/seedance-provider-notes.md)
