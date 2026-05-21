---
name: ai-video-series-archive
description: 当用户想把已经满意的主讲人形象、主讲人三视图、画面风格、提示词规则、默认模型和负面约束保存成可复用模板，或者在新文案中套用指定模板时使用这个 skill。重复主体默认不保存，除非用户明确指定为长期固定角色。
---

# AI Video Series Archive

## Overview

这个 skill 负责两件事：

1. 在用户已经对主讲人、风格、提示词规则和正式成图满意后，询问是否保存为“可复用模板”
2. 在用户下次拿新文案来生成时，读取并套用指定模板

这个 skill 不负责直接生图，也不负责直接写整批提示词。它只负责“模板保存”和“模板复用”这层稳定资产。

模板保存的是跨文案稳定复用的内容，不是某一次文案生成出来的全部临时主体。

## When To Use

- 用户说后续还想沿用当前人物和风格
- 用户想把当前满意结果保存下来
- 用户拿新文案来，且希望沿用上一套人物与风格
- 总控 skill 判断当前任务应该先检查是否存在可复用模板
- 用户说“保存为模板”“套用上次模板”“使用某某模板”

## Default Storage Path

默认把模板保存到：

- `/Volumes/扩展盘/gpt_codex/video-series-archives/<series_slug>.json`

如果用户明确指定别的保存位置，再按用户要求保存。

## What To Save

模板至少应包含：

- `template_name`
- `template_slug`
- `template_type`
- `main_character`
- `visual_style`
- `prompt_rules`
- `defaults`
- `fixed_subjects`
- `notes_for_future_scripts`

默认保存：

- 主讲人描述
- 主讲人正面定稿
- 主讲人三视图
- 画面风格摘要（结构化 Style DNA）
- 风格参考图
- 提示词结构
- 负面约束
- 默认比例
- 默认生图模型
- 默认视频模式
- 构图偏好

默认不保存：

- 每篇文案临时识别出来的重复主体
- 用户未选择的正式成图
- 单次项目任务队列
- 不满意或勉强通过的图片

只有当用户明确说某个角色要长期固定出现时，才保存到 `fixed_subjects`。

## Style DNA（风格基因）

`visual_style` 字段从 v2.0 开始使用结构化 Style DNA 格式，包含 6 组基因：

- `color_palette`：色彩基因（主色、辅色、强调色、饱和度、对比度）
- `lighting_profile`：光影基因（光线类型、方向、色温、光比）
- `texture_profile`：质感基因（颗粒感、锐度、材质、分辨率感受）
- `composition_tendencies`：构图基因（构图倾向、景深、三分法、留白）
- `camera_language`：镜头语言基因（等效焦距、运镜风格、角度倾向）
- `mood_keywords` + `era_spatial` + `post_processing`：情绪与时空基因

完整 schema 见 [style-gene-structure.md](../ai-short-video-pipeline/references/style-gene-structure.md)。

### 继承与混合

- 子模板可通过 `inherits_from` 继承父模板的基因，只覆盖需要修改的部分
- 可通过 `mix_from` 从多个模板各取部分基因组合
- 可通过 `overrides` 做单基因微调

### 旧模板迁移

用户套用旧版扁平风格描述的模板时，自动解析为结构化 Style DNA 并展示给用户确认。旧模板保留不删除，新模板用 `_v2` 后缀区分。

## Create Workflow

只有在用户已经看过并认可以下内容后，才主动询问是否保存模板：

- 主讲人正面定稿或三视图
- 画面风格
- 正式图片提示词规则
- 至少一批正式成图

默认话术意图应是：

- 你现在这套主讲人、风格和提示词规则已经稳定了，是否要保存为模板，方便下次新文案直接套用

推荐话术：

```text
是否要把这次的主讲人、风格和提示词规则保存为模板？

如果要保存，请输入模板名称。
如果不保存，请输入 2。
```

用户输入模板名称后，再问：

```text
是否要选择本次满意的正式图作为风格样例？

如果要保存样例图，请输入图片编号，例如：1、3、8。
如果不保存样例图，请输入 2。
```

如果用户选择样例图，只把用户指定编号对应的正式成图保存到 `visual_style.approved_style_sample_urls`。

如果用户没有选择样例图，不保存正式成图样例。

## Reuse Workflow

当用户下次拿新文案来时，如果用户提到“套用模板”或指定模板名称，不要直接重新做主讲人和风格。优先先读取模板。

推荐触发表达：

- `套用赛博女主持模板`
- `使用上次模板`
- `使用知行视频skill，套用某某模板做这篇文案`

读取模板后，先展示摘要：

```text
已读取「模板名称」：
- 主讲人：[摘要]
- 风格：[摘要]
- 默认比例：[比例]
- 默认模型：[模型]

沿用这套模板请输入 1；
需要修改模板设置请输入 2。
```

如果模板使用旧版扁平风格描述，读取时自动解析为结构化 Style DNA 并展示给用户确认。

用户确认后，后续工作流应：

1. 继承模板中的主讲人锚点、风格锚点、提示词规则和默认参数
2. 根据新文案重新识别重复主体
3. 不把模板里的旧文案临时主体强行带入新文案
4. 不重新发明主讲人和风格，除非用户明确要求改

### 微调风格基因

用户可以在套用模板后对单个基因做微调，不需要重新描述整体风格：

```text
这套模板的风格整体沿用，但色调想暖一点。
```

此时只覆盖 `lighting_profile.warmth` 和 `color_palette` 中的冷暖倾向，其他基因保持不变。

```text
构图想更大气一点，多用全景和远景。
```

此时只覆盖 `composition_tendencies.framing` 和 `camera_language.lens_equivalent`。

## Output

创建档案时，至少输出：

- `archive_path`
- `template_name`
- `saved_main_character`
- `saved_style_summary`
- `saved_prompt_rules`
- `saved_style_samples`
- `saved_reference_assets`

复用档案时，至少输出：

- `archive_path`
- `template_name`
- `loaded_main_character`
- `loaded_style_summary`
- `execution_defaults`

## References

- 档案模板： [references/archive-template.json](./references/archive-template.json)
- 档案字段说明： [references/archive-fields.md](./references/archive-fields.md)
