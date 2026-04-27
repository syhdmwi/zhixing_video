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
- 画面风格摘要
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

用户确认后，后续工作流应：

1. 继承模板中的主讲人锚点、风格锚点、提示词规则和默认参数
2. 根据新文案重新识别重复主体
3. 不把模板里的旧文案临时主体强行带入新文案
4. 不重新发明主讲人和风格，除非用户明确要求改

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
