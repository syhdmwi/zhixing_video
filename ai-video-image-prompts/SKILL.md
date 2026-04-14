---
name: ai-video-image-prompts
description: 当用户要把一段文案直接转换成一组可执行的生图提示词时使用这个 skill。它适用于 nanobanana-2、nanobanana-pro、seedream-5.0，并强调维持主体一致性和风格一致性。这里的主体不仅包括人，也包括重复出现的动物、吉祥物、IP 形象、产品、道具或关键物件，同时支持“文案 -> 30 个图片提示词”这类批量生成工作流。
---

# AI Video Image Prompts

## Overview

这个 skill 只负责静帧生图提示词，不负责图生视频，也不负责数字人视频轨。目标是把一段文案或镜头表，直接转换成一组可复制、可批量执行、可直接喂给生图工具的图片提示词。

默认不要一拿到文案就直接生成 30 条正式提示词。标准路径应该是：

1. 收集必要参数
2. 识别会反复出现的人和物
3. 先为这些重复主体生成预览图
4. 让用户确认预览图是否满意
5. 用户满意后，生成这些主体的三视图作为参考图
6. 再生成整批正式提示词
7. 用户确认提示词后，用这些提示词进入生图阶段

如果文案里存在会反复出现的人、动物、吉祥物、产品、关键物件，那么预览图确认和三视图参考图应视为默认步骤，而不是可选步骤。
提示词一旦确认，默认交给 `ai-video-prompt-to-images` 继续处理，不在本 skill 内重复重写提示词。

## Supported Workflow

优先适配以下模型名：

- `nanobanana-2`
- `nanobanana-pro`
- `seedream-5.0`

如果用户没有指定模型，就输出模型无关的结构化提示词。

这个 skill 支持两种入口：

- 文案直接转提示词
- 已有镜头表再转提示词

如果用户像你一样，先给大模型一段文案，再要求它生成 `30` 个图片提示词，优先按“文案直接转提示词”流程执行。

## Inputs

- 文案或镜头表
- 图片数量
- 图片比例
- 输出语言
- 用户上传的人物参考图
- 风格要求
- 画幅
- 禁用元素
- 目标提示词数量

## Core Rules

- 重复出现的人、动物、吉祥物、产品、关键物件，都应被视为“重复主体”
- 重复主体应以用户参考图、用户描述或首次锁定设定为第一锚点
- 先写全局 `Subject Consistency Block`
- 再写全局 `Style Block`
- 最后写镜头局部变化块
- 不编造模型私有语法
- 每条提示词都要对应文案里的一个具体信息点或情绪节点
- 如果用户明确要求 `30` 个提示词，优先服从数量要求
- 如果用户未指定数量，优先跟随分镜数；没有分镜数时再按时长估算
- 先确认必要参数，再直接生成整批提示词
- 默认至少三分之一提示词是纯场景画面
- 默认剩余提示词以人物画面或人物参与画面为主
- 生成的提示词必须能直接用于生图工具，不要停留在概括层
- 如果多个镜头里反复出现同一个人或同一个物，也必须保持主体一致性
- 对于会反复出现的主体，先生成预览图让用户直观看
- 不是所有重复名词都必须进入预览阶段，只有需要稳定视觉身份且会多次入镜的主体才必须先锁定
- 用户不满意预览图时，应先修改预览，不要急着进入 30 张正式图
- 如果连续多次修改预览图仍不满意，应主动询问用户是否提供参考图
- 用户满意预览图后，先生成主体三视图作为参考图
- 正式 30 张图应尽量以已确认主体图和三视图作为参考锚点
- 所有主体预览图默认使用白底
- 所有三视图参考图默认使用白底
- 正式分镜图里，只要画面包含人物，默认使用半身照或半身构图，不要生成全身照，除非用户明确要求全身

## Quantity Rules

提示词数量优先级：

1. 用户明确指定数量，例如 `30` 个
2. 已有镜头表的镜头数
3. 按总控 skill 的时长估算结果

不要一边说按时长算，一边又忽略用户给的明确数量。

## Workflow

### 1. Ask The Required Intake Questions First

拿到文案后，先确认这些信息，再继续：

- 要生成多少张图片
- 图片比例是 `16:9`、`9:16`，还是别的比例
- 输出语言是否以中文为主
- 想要的整体风格是什么

如果用户没给，必须先问；不要直接默认开始写整批提示词。

在问完这些基础参数后，如果当前任务是“新的文案继续做同系列内容”，还应优先问：

- 这次是否要使用指定的“人设与风格档案”

如果用户要复用档案，优先先读取档案中的人物锚点、重复物锚点、风格摘要和默认参数，再继续后续流程。

### 2. Identify Recurring Subjects First

先从文案里提取会反复出现的主体，例如：

- 主讲人物
- 红色卡通龙虾
- 品牌吉祥物
- 产品外观
- 固定设备或关键物件

如果这些主体会在多个镜头里反复出现，就不能跳过主体确认。

但要先做一次筛选，不要把所有重复名词都拉进预览阶段。默认只有这类对象必须先锁定：

- 会在多个镜头里持续出现，且外观需要保持一致的人物
- 会在多个镜头里持续出现的动物、吉祥物、IP 形象
- 会在多个镜头里持续出现，且有明确造型要求的产品、道具、装置

以下内容默认不单独做主体预览，除非用户明确要求它们也要固定形象：

- 平台名、品牌名、厂商名
- 抽象概念
- 普通 UI 界面元素
- 一次性出现的工具、图标、背景信息点

### 3. Generate Subject Preview Images First

在正式 30 张图之前，先为重复主体生成预览阶段材料。至少包括：

- 人物预览图
- 重复物件或吉祥物预览图

这一步的目标是让用户“直观看见”主体长什么样，而不是只看文字设定。

预览图默认要求：

- 白色纯背景
- 单主体清晰展示
- 不做剧情场景
- 不加复杂环境元素
- 不出现任何文字、字母、水印、logo、排版元素

如果环境支持生图 API，就直接生成预览图；如果当前环境不支持直接调生图 API，就至少输出：

- 可直接用于预览生图的提示词
- 预览图用途说明
- 后续要锁定的主体清单

### 4. Let The User Approve Or Revise The Subject Previews

拿到预览图后，让用户确认：

- 人物是否满意
- 重复物件或吉祥物是否满意
- 是否需要调整配色、形状、气质、材质

如果用户不满意，先修改预览图阶段，不进入正式 30 张图。

如果同一主体连续多次预览仍不满意，不要继续盲目重试，应询问用户是否可以提供参考图或更明确的视觉参考。

### 5. Generate Three-View References After Approval

用户满意预览图后，为关键重复主体生成三视图参考图。

至少包括：

- 人物三视图
- 高频重复物件或吉祥物三视图

这些三视图的目标是给后续正式出图提供稳定参考，而不是剧情图。

三视图默认要求：

- 白色纯背景
- 单主体清晰展示
- 不加剧情环境
- 不出现任何文字、字母、水印、logo、排版元素

### 6. Generate The Final Prompt Batch

主体确认完成后，再根据文案生成整批正式提示词。提示词必须：

- 内容与文案逐段对应
- 可以直接复制到生图工具使用
- 统一整体风格
- 保持重复主体一致性
- 默认至少三分之一是纯场景画面
- 不要所有画面都有人物
- 不要所有画面都只是场景
- 有人物的画面和纯场景画面应交替或合理穿插，利于后续剪辑

这里的“重复主体一致性”包括但不限于：

- 同一个女生角色
- 同一个红色卡通龙虾
- 同一个品牌 mascot
- 同一个产品或设备外观
- 同一个固定道具

正式分镜图的人物构图默认要求：

- 有人物的正式画面，优先半身照、半身特写或胸像构图
- 不要默认生成全身站立图
- 让人物脸部、上半身、手部核心动作更容易看清
- 只有用户明确要求全身构图、走路构图、站姿全景时，才放开全身照

如果用户没有特别强调构图比例，默认使用：

- 人物/人物参与画面：约三分之二
- 纯场景画面：约三分之一

### 7. Let The User Confirm The Prompt Batch

整批提示词输出后，让用户确认：

- 提示词是否贴合文案
- 画风是否正确
- 人物与场景比例是否合适
- 是否可以直接用于生图

如果用户确认提示词没问题，下一步就是交给 `ai-video-prompt-to-images` 用这些提示词去生图。

### 8. Read The Full Script First

先完整理解文案的叙事结构，不要看到一句就立刻写一句。至少先识别：

- 开头钩子
- 问题提出
- 核心卖点或核心观点
- 案例或论证
- 转折
- 收尾 CTA

### 9. Allocate Prompt Slots Across The Script

把提示词数量分配到文案结构里，而不是平均切字数。优先保证：

- 开头钩子有独立画面
- 重要卖点有独立画面
- 数字、对比、案例、动作类句子优先独立成画面
- 结尾 CTA 有独立画面

### 10. Build One Global Prompt Bible

先固定：

- `Subject Consistency Block`
- `Style Block`
- `Negative Constraints`

再为每个提示词叠加局部镜头变化。

### 11. Convert Each Beat Into An Image Prompt

每条提示词都应回答这 4 个问题：

- 这条画面对应文案哪一段？
- 画面主信息是什么？
- 主角在做什么？
- 画面如何体现当前句子的情绪或结论？

### 12. Keep The Batch Cohesive

同一批提示词中，默认不应无理由改变：

- 主要人物的身份、脸部特征、发型、服装
- 重复动物或吉祥物的颜色、造型、表情体系、材质感
- 重复产品或物件的外观、配色、结构、识别特征
- 视觉风格
- 时代和世界观

## Prompt Pattern

每条提示词推荐结构：

```text
[Character Block from user reference]
[Recurring subject consistency block]
[Style Block from user preference]
[Shot-specific action and environment]
[Composition, lens, framing, lighting]
[Negative constraints]
```

如果用户提供的是文案而不是镜头表，则在写提示词前先补一个内部字段：

```text
[Narration beat]
[Visual goal]
[Prompt body]
```

## Model Routing Guidance

- 如果用户要更高一致性，优先强调参考图锚定和低变量镜头变化
- 如果用户自己有成熟模板，直接沿用其模板结构
- 如果用户没有成熟模板，输出通用结构，不发明厂商专属参数
- 如果文案里存在重复出现的非人物主体，必须像人物一样单独锁定一致性

## LLM Meta-Prompt Mode

如果任务目标是“帮用户写一个给大模型用的母提示词”，不要直接产出 30 条图片提示词，而是优先输出：

- 一段可直接粘贴给大模型的主提示词
- 目标输出格式
- 必填参数列表
- 一份简短使用说明

模板见 [references/master-prompt-template.md](./references/master-prompt-template.md)。

如果任务目标是“帮用户跑完整工作流”，默认顺序必须是：

1. 询问图片数量、比例、语言、风格
2. 识别重复主体
3. 先生成重复主体预览图
4. 用户确认或修改预览图
5. 生成主体三视图参考图
6. 再生成整批正式提示词
7. 默认保持至少三分之一纯场景
8. 让用户确认提示词
9. 用户确认后进入生图

## Script-To-Prompt Mapping Rules

优先把文案内容映射成以下类型的画面：

- 事实信息
- 情绪冲突
- 人物动作
- 环境变化
- 抽象概念的具象化表达

避免大量重复这几类低信息密度画面：

- 连续多张只是人物站着说话
- 连续多张只是电脑界面或手机截图
- 没有动作、没有情绪、没有场景变化的空镜
- 与文案句意无关的炫技画面

详细规则见 [references/script-to-image-playbook.md](./references/script-to-image-playbook.md)。

## Output

如果直接输出图片提示词批次，每个条目至少产出：

- `shot_id`
- `narration_excerpt`
- `visual_goal`
- `frame_type`
- `model`
- `image_prompt`
- `negative_prompt_or_constraints`
- `consistency_note`

如果输出的是“给大模型的母提示词”，至少产出：

- `system_or_master_prompt`
- `input_variables`
- `expected_output_schema`
- `usage_note`

如果当前阶段是角色确认阶段，至少产出：

- `character_summary`
- `style_summary`
- `approval_questions`
- `revision_path_if_rejected`

如果当前阶段是三视图阶段，至少产出：

- `front_view_prompt`
- `side_view_prompt`
- `back_view_prompt`
- `consistency_lock_note`
- `render_notes`

- 如果当前阶段是主体预览阶段，至少产出：

- `subject_preview_list`
- `preview_prompts_or_preview_images`
- `approval_questions`
- `revision_targets`

## References

- 提示词母模板： [references/master-prompt-template.md](./references/master-prompt-template.md)
- 文案转画面规则： [references/script-to-image-playbook.md](./references/script-to-image-playbook.md)
- 你的文案例子： [references/example-openclaw-master-prompt.md](./references/example-openclaw-master-prompt.md)
- 角色确认与三视图流程： [references/character-approval-workflow.md](./references/character-approval-workflow.md)
- 角色确认输出模板： [references/character-review-template.md](./references/character-review-template.md)
- 三视图输出模板： [references/three-view-template.md](./references/three-view-template.md)
- 重复主体一致性规则： [references/subject-consistency-rules.md](./references/subject-consistency-rules.md)
- 主体预览确认流程： [references/subject-preview-workflow.md](./references/subject-preview-workflow.md)
