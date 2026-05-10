---
name: ai-video-prompt-to-images
description: 当用户已经确认了一批图片提示词，接下来要正式进入生图阶段时使用这个 skill。它适用于 nanobanana-2、nanobanana-pro、seedream-5.0，并负责保持提示词顺序、比例、主体一致性与场景/人物分配。这里的主体既包括人，也包括重复出现的动物、吉祥物、IP 形象、产品和关键物件；本 skill 不在未经要求的情况下重写提示词内容。
---

# AI Video Prompt To Images

## Overview

这个 skill 只负责“提示词确认后 -> 正式生图”这一段。它不负责重新策划提示词，也不负责图生视频。默认职责是把已经确认的提示词批次，变成一组可以直接执行的生图队列。

本 skill 假设上游已经完成：

- 重复主体预览图确认
- 重复主体三视图参考图确认

## When To Use

- 用户已经确认提示词没问题
- 用户要开始正式生图
- 用户使用 `nanobanana-2`、`nanobanana-pro`、`seedream-5.0`

## Required Inputs

- 已确认的提示词批次
- 生图模型
- 比例
- 输出张数
- 参考图或角色锚点（如果有）
- 已确认的主体预览图和三视图参考图（如果有）
- 输出命名规则或镜头编号

## Core Rules

- 提示词一旦确认，默认不重写
- 按原有 `shot_id` 顺序执行
- 保持人物镜头和纯场景镜头比例不被打乱
- 所有重复主体都应保持一致性，不只限于人物
- 人物提示词优先继承同一角色锚点
- 重复出现的动物、吉祥物、产品、关键物件也要继承同一主体锚点
- 纯场景提示词不要强行加人物
- 如果用户提供参考图，人物镜头优先附着参考图一致性策略
- 如果用户提供的是本地参考图文件，且当前模型接口需要公网 URL，默认先自动上传到 TOS，再把公网直链写入 `reference_urls`
- 只有 TOS 配置缺失时，才提示用户提供公网可访问参考图链接
- 如果上游已经生成主体预览图和三视图参考图，正式生图应优先使用它们作为参考锚点
- 如果当前环境无法直接调用生图工具，就输出一份可执行的生图队列表
- 如果平台任务长时间停留在非终态，不要直接当失败丢掉，应单独标记为平台卡住
- 平台卡住的任务应保留全部历史 `task_id`
- 平台卡住后默认允许自动重提一次
- 如果主体预览阶段连续重提后仍不理想，再回到上游询问用户是否提供参考图
- 生图成功后，默认直接把图片展示给用户看，不只给链接
- 展示图片后，再让用户确认哪些镜头可以保留、哪些镜头需要回炉
- 所有轮询中的进度汇报，默认遵循总控里的统一规则：[references/polling-progress-rules.md](../ai-short-video-pipeline/references/polling-progress-rules.md)

## Codex Built-In Image Priority

如果当前运行环境是 `Codex`,并且用户选择的是 `GPT-Image-2`,本 skill 默认优先使用 `Codex` 自带的生图能力,而不是先走外部批处理脚本。

默认策略:

1. 只要是 `Codex` + `GPT-Image-2` -> 一律优先 `Codex` 自带生图
2. 非 `Codex` 环境 + `GPT-Image-2` -> 使用外部批处理脚本 / API
3. `nanobanana-2` -> 继续沿用现有外部脚本

如果在 `Codex` 中走内建生图,仍然必须遵守本 skill 的这些规则:

- 不重写已确认提示词
- 保持 `shot_id` 顺序
- 保持主体一致性锚点
- 生成完成后整批展示给用户确认

硬规则:

- 在 `Codex` 中,不要因为是前 10 张测试批次、审一张改一张、还是 60 张正式生图,就切换执行方式
- 在 `Codex` 中,不要因为已有 JSON 队列文件就自动改走外部脚本
- 只有当前 `Codex` 自带生图能力不可用时,才改用：

- `scripts/gpt_image2_batch.py`

## Workflow

### 1. Confirm The Batch Is Approved

只有当用户明确表示“提示词可以了”或“按这版去生图”时，才进入本 skill。

### 2. Lock The Execution Parameters

至少确认：

- 用哪个模型
- 用哪个比例
- 一共多少张
- 是否有人物参考图
- 是否已经有主体预览图和三视图参考图

### 3. Build The Generation Queue

按顺序为每条提示词生成执行队列。每条至少包含：

- `shot_id`
- `frame_type`
- `model`
- `aspect_ratio`
- `image_prompt`
- `reference_image_required`
- `consistency_note`

如果队列使用 `reference_urls`，其中的资源必须是模型可访问的公网 URL；本地路径必须先按总控公网资源规则转存。

### 4. Preserve The Prompt Structure

默认不要在这个阶段大改提示词，只做必要的执行层补全，例如：

- 统一比例
- 明确模型
- 补上镜头编号
- 标记是否需要参考图

### 5. Execution And QC

如果工具可直接调用，则按队列执行；如果工具不可直接调用，则输出可执行队列表和检查清单。

当前子 skill 已提供真实 API 脚本层：

- `scripts/nanobanana2_batch.py`

输入格式示例见：

- `references/generation-queue-example.json`

检查重点：

- 张数是否完整
- 顺序是否正确
- 纯场景是否仍保持至少三分之一
- 人物镜头是否延续同一角色
- 重复出现的动物、吉祥物、产品、关键物件是否延续同一主体
- 风格是否统一
- 是否存在平台长时间卡住但未被识别的任务

### 6. Show The Rendered Images By Default

只要当前环境支持直接展示图片，生成成功后默认动作应是：

- 按 `shot_id` 顺序展示图片
- 尽量直接渲染图片，不只贴 URL
- 同时保留图片链接，便于后续复查
- 展示完成后，再问用户哪些镜头满意，哪些镜头要改

不要在图片已经生成成功的情况下，只返回 JSON 或只返回一堆链接就结束。

### 6.5 Quality Review Loop（质量审核回环）

全部图片生成成功并展示给用户之前，先自动运行质量审核回环。

审核内容：
- 角色一致性：逐张对比 Character Block，检查脸型、发型、服装、配饰是否漂移
- 空间一致性：同一场景内环境锚点位置、光线方向是否跳变
- 风格一致性：画风、色彩倾向、质感是否突变
- 构图多样性：景别分布是否单调，人物/场景比例是否合理
- 瑕疵检测：多余手指、文字水印、肢体畸形、多余人物入镜

审核结果分三级：
- 🔴 必须修改：角色串脸、空间错乱、风格突变、肢体严重畸形
- 🟡 建议修改：服装细节微变、光线轻微偏差、构图略单调
- 🟢 轻微可忽略：色温差异、背景细节不同

如果没有 🔴 问题，直接展示审核报告 + 图片，询问用户是否满意。
如果有 🔴 问题，先展示报告，建议用户先处理必须修改的镜头。
如果 🔴 问题 ≥ 30%，建议整体重生成该批次。

用户选择自动重生成时，只重生成 🔴 级别镜头，最多重试 2 轮。

详细审核维度和输出格式见 [quality-review-loop.md](../ai-short-video-pipeline/references/quality-review-loop.md)。

### 7. Ask To Save A Reusable Template After Approval

当以下内容都已经产出且用户看过后，如果用户整体满意，默认应主动补问：

- 是否需要把这次的主讲人、风格和提示词规则保存为模板，方便下次新文案直接套用

这里的“已产出内容”通常包括：

- 主讲人正面定稿或三视图
- 风格参考图（如果有）
- 正式图片提示词规则
- 一批正式成图

推荐话术：

```text
是否要把这次的主讲人、风格和提示词规则保存为模板？

如果要保存，请输入模板名称。
如果不保存，请输入 2。
```

如果用户输入模板名称，再继续问：

```text
是否要选择本次满意的正式图作为风格样例？

如果要保存样例图，请输入图片编号，例如：1、3、8。
如果不保存样例图，请输入 2。
```

保存规则：

- 主讲人三视图默认保存
- 风格描述、提示词规则、负面约束默认保存
- 正式成图样例必须由用户选择编号后才保存
- 每篇文案临时识别出的重复主体默认不保存
- 只有用户明确要求长期复用的角色，才保存为固定角色

如果用户同意保存模板，下一步应把这些已确认资产交给 `ai-video-series-archive` 保存，而不是只停留在当前会话里。

## Output

至少输出：

- `generation_queue`
- `execution_notes`
- `qc_checklist`
- `rendered_images_for_review`

如果图片已经成功生成，`rendered_images_for_review` 应按 `shot_id` 顺序包含可直接展示给用户的图片结果。

## References

- 执行检查清单： [references/batch-execution-checklist.md](./references/batch-execution-checklist.md)
- 队列输入示例： [references/generation-queue-example.json](./references/generation-queue-example.json)
- 脚本使用说明： [references/script-usage.md](./references/script-usage.md)
