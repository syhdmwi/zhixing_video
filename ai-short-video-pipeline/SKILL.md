---
name: ai-short-video-pipeline
description: 当用户想把一段文案或口播稿制作成完整的 AI 短视频流程时使用这个总控 skill。它负责判断何时调用分镜、图片提示词、图生视频、数字人轨道、剪辑整合等子 skills，并适用于 nanobanana-2、nanobanana-pro、seedream-5.0、doubao-seedance-1.0-pro-fast、即梦 OmniHuman 1.5、蝉镜数字人这类工具链。
---

# AI Short Video Pipeline

## Overview

这个 skill 是总控调度器，不负责把所有细节都自己做完，而是先把任务拆成合适的生产阶段，再决定要调用哪些子 skills。它面向“数字人口播视频”和“画面分镜视频”两条独立生产线，最后在剪辑阶段合流。

默认面向“数字人口播 + 画面分镜 + 剪辑整合”的短视频工作流，而不是只生成单张图或单段视频。

## When To Use

在以下场景优先使用这个 skill：

- 用户要从文案开始规划完整视频工作流
- 用户明确说这件事要拆成多个 skills 分工
- 用户要区分“数字人视频轨”和“画面分镜视频轨”
- 用户最终要把多个生成结果剪进一个完整成片
- 用户明确提到 `nanobanana-2`、`nanobanana-pro`、`seedream-5.0`、`doubao-seedance-1.0-pro-fast`、`即梦 OmniHuman 1.5`、`蝉镜数字人`

## Required Inputs

优先收集以下信息；如果用户没给全，可以按 [references/intake-checklist.md](./references/intake-checklist.md) 的默认值继续：

- 文案全文
- 目标平台和画幅，例如 `9:16`、`16:9`、`1:1`
- 目标时长；若未提供，则需要估算
- 主角信息：人物设定、外貌描述、服装、年龄段、身份、参考图
- 视觉风格：写实、电影感、插画、纪实、广告感等
- 使用的生图模型、图生视频模型、数字人工具、剪辑工具
- 是否有禁用元素或品牌限制

如果用户已经提供参考图、角色定妆图、品牌规范或既有成片风格，优先以这些材料为准。

## Skill Map

总控 skill 不应和子 skills 重复劳动。先判断任务落在哪个阶段，再调用对应 skill：

1. `ai-video-shot-planner`
   负责文案时长估算、镜头数估算、分镜拆分、数字人与 B-roll 的镜头分配。
2. `ai-video-image-prompts`
   负责基于用户参考图和统一风格生成生图提示词，适配 `nanobanana-2`、`nanobanana-pro`、`seedream-5.0`。
3. `ai-video-prompt-to-images`
   负责在用户确认提示词后，把提示词按顺序转成可执行的生图队列，进入实际生图阶段，并在生成成功后默认直接展示图片给用户确认。
4. `ai-video-series-archive`
   负责把用户已经满意的人设、重复物、风格参考和正式成图保存成可复用档案，或者在新文案中先读取指定档案继续生成。
5. `ai-video-motion-prompts`
   负责把已确认的静帧镜头转成适用于 `doubao-seedance-1.0-pro-fast` 的图生视频提示词，并默认先产出测试批次动作方案再进入全量执行。
6. `ai-video-generate-videos`
   负责在用户选择 `grok` 或 `seedance` 后，真实提交图生视频任务并轮询结果。
7. `ai-video-avatar-track`
   负责为 `即梦 OmniHuman 1.5`、`蝉镜数字人` 或速创 `Digital_Humans` 执行数字人生成阶段。
8. `ai-video-edit-assembly`
   负责把“数字人视频轨”和“画面视频轨”合流成最终剪辑方案。

如果用户只要求其中一段工作，不要调用整套流程。

## Workflow

### 1. Intake

先确认任务目标是“完整短视频生产包”还是只要其中一段：

- 仅分镜
- 仅图片提示词
- 仅图生视频提示词
- 仅数字人口播整合
- 全流程交付包

如果用户没有说清楚，默认交付全流程包。

在进入人物设定和风格设定前，优先先问一件事：

- 这次是否要使用指定的“人设与风格档案”

如果用户要复用已有档案，优先先调用 `ai-video-series-archive` 读取档案，再继续后续流程。

### 2. Decide The Two-Track Plan First

先把任务明确成两条生产轨道：

- `Track A`: 数字人口播视频轨
- `Track B`: 图片生成后再转视频的画面轨

这两条轨道应分别生成，不要把数字人口播和图生视频混成同一个生成步骤。最后再进入剪辑整合。

### 3. Estimate Duration And Shot Count

镜头数默认按每分钟 `11` 张图计算：

- `shot_count = ceil(duration_seconds / 60 * 11)`

时长优先级：

1. 用户明确给出的目标时长
2. 现成音频或数字人口播时长
3. 按文本估算

当只能按文本估算时，默认使用：

- 中文：`230` 字/分钟
- 英文：`150` 词/分钟

可以用 `scripts/calc_shot_plan.py` 做快速估算。

### 4. Create The Immutable Production Bible

在生成任何单镜头提示词前，先固定三块不可随意漂移的全局内容：

- 角色一致性块
- 风格一致性块
- 负面约束块

这三块写完后，每个分镜提示词都应继承它们，再叠加镜头自己的动作、场景和构图变化。具体规则见 [references/consistency-rules.md](./references/consistency-rules.md)。

### 5. Split Script Into Shots

把文案按语义节奏拆成镜头，而不是机械按句号平均切分。默认每个镜头 `4` 到 `7` 秒，优先遵守：

- 一个镜头只表达一个清晰信息点
- 开头 3 秒优先服务钩子
- 论证段按观点变化切镜
- 转折句、数字、对比、案例适合单独成镜
- 收尾 CTA 应预留独立镜头

每个镜头至少产出：

- `shot_id`
- `time_range`
- `narration_excerpt`
- `visual_goal`
- `image_prompt`
- `image_to_video_prompt`
- `edit_note`

标准格式见 [references/output-format.md](./references/output-format.md)。

### 6. Route To The Right Subskill

按任务内容路由：

- 需要“估时 + 分镜 + 数字人/B-roll 分配”时，用 `ai-video-shot-planner`
- 需要“参考图一致性 + 生图提示词”时，用 `ai-video-image-prompts`
- 需要“提示词确认后进入生图”时，用 `ai-video-prompt-to-images`
- 需要“保存或读取系列人设与风格档案”时，用 `ai-video-series-archive`
- 需要“静帧转视频动作提示词”时，用 `ai-video-motion-prompts`
- 需要“选择视频 provider 并真实提交图生视频任务”时，用 `ai-video-generate-videos`
- 需要“数字人独立视频轨生成方案”时，用 `ai-video-avatar-track`
- 需要“两个视频轨合成最终成片方案”时，用 `ai-video-edit-assembly`

### 7. Generate Image Prompts

先写“全局稳定块”，再写“镜头可变块”。

图片提示词必须：

- 保留同一个主角身份、脸部特征、发型、服装主设定
- 保留同一视觉风格、色温、镜头语言和质感
- 只在动作、机位、场景、道具、情绪上做局部变化
- 避免同一批次中无理由更换服装、发色、年龄感、脸型、时代背景

如果用户指定 `nanobanana`、`Seedream 4.6` 等模型，但没有给出该模型的提示词偏好或长度限制，则默认输出“模型无关、结构清晰、可直接改写”的提示词，不假设厂商私有语法。

### 8. Generate Image-To-Video Prompts

图生视频提示词应建立在已确认可用的静帧上，不要跳过静帧一致性检查。每个镜头的视频提示词至少补充：

- 主体动作
- 镜头运动
- 前景或背景运动
- 节奏和情绪
- 禁止异常变形的约束

如果某个镜头对人物一致性要求特别高，优先先稳住静帧，再做低幅度运动，而不是一开始就要求复杂大动作。

### 9. Run Avatar Generation

当前这一阶段只处理数字人生成，不处理数字人视频在最终成片里的剪辑使用方式。

当全部画面视频已经生成完成后，默认要主动继续问：

- 是否需要制作数字人视频轨

如果用户需要，再进入 `ai-video-avatar-track`，要求用户提供：

- 音频
- 正面人物视频

如果当前数字人走速创 `Digital_Humans` 接口，优先使用公网可访问直链，不直接假设本地文件可被接口读取。

如果用户没有指定数字人工具，只输出整合方案，不编造某个平台专属参数。

### 10. Assemble Final Delivery Package

默认交付包含：

- 时长与镜头数估算
- 分镜表
- 角色一致性块
- 风格一致性块
- 负面约束块
- 每镜头图片提示词
- 每镜头图生视频提示词
- 剪辑与转场建议
- 字幕、BGM、SFX、封面、CTA 建议

## Current Toolchain Defaults

当前这套 skill 套件默认围绕以下工具链编排：

- 生图：`nanobanana-2`、`nanobanana-pro`、`seedream-5.0`
- 图生视频：`doubao-seedance-1.0-pro-fast`
- 数字人：`即梦 OmniHuman 1.5`、`蝉镜数字人`
- 速创数字人：`Digital_Humans`
- 发布平台：抖音、视频号、小红书
- 画幅：根据用户要求选择，不强制固定

不要为这些工具编造用户未提供的私有参数；如果用户提供了自己常用模板，优先继承。

## Output Requirements

默认按照 [references/output-format.md](./references/output-format.md) 的结构输出，除非用户明确要求 JSON、CSV、表格或更短版本。

如果用户要直接拿去批量生成素材，优先保证：

- 提示词可复制
- 角色设定稳定
- 镜头编号清晰
- 每个镜头都能独立执行

## Tool Adaptation Rules

当用户提供特定工具信息时，按以下顺序适配：

1. 用户自己的成功案例或既有模板
2. 用户提供的官方文档或截图
3. 通用提示词结构

不要假设未提供的私有参数名、权重语法或 seed 语法。

## References

- 输入补全与默认值： [references/intake-checklist.md](./references/intake-checklist.md)
- 一致性控制规则： [references/consistency-rules.md](./references/consistency-rules.md)
- 标准输出模板： [references/output-format.md](./references/output-format.md)
- 用户配置模板： [references/provider-config-template.md](./references/provider-config-template.md)
- 多 skill 协作图： [references/suite-architecture.md](./references/suite-architecture.md)

## Script

- 时长和镜头数估算： `scripts/calc_shot_plan.py`
