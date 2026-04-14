---
name: ai-video-series-archive
description: 当用户想把已经满意的人物形象、重复物形象、风格参考图、默认模型和负面约束保存成可复用的系列档案，或者在新文案中复用指定档案时使用这个 skill。它适用于“创建系列人设与风格档案”和“读取指定档案继续生成”的工作流。
---

# AI Video Series Archive

## Overview

这个 skill 负责两件事：

1. 在用户已经对预览图、三视图、风格参考图和正式成图满意后，询问是否创建“系列人设与风格档案”
2. 在用户下次拿新文案来生成时，先询问是否使用已有的指定档案

这个 skill 不负责直接生图，也不负责直接写整批提示词。它只负责“保存”和“复用”这层稳定资产。

## When To Use

- 用户说后续还想沿用当前人物和风格
- 用户想把当前满意结果保存下来
- 用户拿新文案来，且希望沿用上一套人物与风格
- 总控 skill 判断当前任务应该先检查是否存在可复用系列档案

## Default Storage Path

默认把档案保存到：

- `/Volumes/扩展盘/gpt_codex/video-series-archives/<series_slug>.json`

如果用户明确指定别的保存位置，再按用户要求保存。

## What To Save

一个系列档案至少应包含：

- `series_name`
- `series_slug`
- `created_from_script`
- `default_image_model`
- `default_aspect_ratio`
- `default_output_language`
- `style_summary`
- `negative_constraints`
- `subject_anchors`
- `style_reference_images`
- `approved_preview_images`
- `approved_three_view_images`
- `approved_final_images`
- `notes_for_future_scripts`

其中 `subject_anchors` 至少覆盖：

- 主角人物
- 高频重复动物 / 吉祥物 / IP
- 其他必须长期稳定的关键物件

## Create Workflow

只有在用户已经看过并认可以下内容后，才主动询问是否创建档案：

- 主体预览图
- 主体三视图
- 风格参考图
- 至少一批正式成图

默认话术意图应是：

- 你现在这套人物和风格已经稳定了，是否要帮你创建系列人设与风格档案，方便下次新文案直接复用

如果用户同意，就把当前已确认资产整理成档案并保存。

## Reuse Workflow

当用户下次拿新文案来时，不要直接重新做人物设定。优先先问：

- 这次是否要使用指定的“人设与风格档案”

如果用户说要使用某个档案，则后续工作流应：

1. 先读取档案
2. 继承档案中的人物锚点、重复物锚点、风格锚点、默认参数
3. 只根据新文案改镜头内容
4. 不重新发明人设和风格，除非用户明确要求改

## Output

创建档案时，至少输出：

- `archive_path`
- `series_name`
- `saved_subjects`
- `saved_style_summary`
- `saved_reference_assets`

复用档案时，至少输出：

- `archive_path`
- `loaded_subjects`
- `loaded_style_summary`
- `execution_defaults`

## References

- 档案模板： [references/archive-template.json](./references/archive-template.json)
- 档案字段说明： [references/archive-fields.md](./references/archive-fields.md)
