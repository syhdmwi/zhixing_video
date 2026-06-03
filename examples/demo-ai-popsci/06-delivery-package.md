# 06 Delivery Package

SSOT 引用：
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)
- 模型清单：[../../MODELS.md](../../MODELS.md)
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)

## 交付摘要

- project_id: `demo-ai-popsci`
- title: `AI 不只是会聊天`
- duration: 约 45 秒
- aspect_ratio: `16:9`
- image_model: `GPT-Image-2`
- video_provider: `grok`
- style_key: `cyberpunk_bright_hud_infographic`
- template_ref: `../../templates/cyber-host-template.json`

## 文件清单

| 阶段 | 文件 | 状态 |
| --- | --- | --- |
| 原始文案 | [00-source-script.md](./00-source-script.md) | 已完成 |
| 分镜规划 | [01-shot-plan.md](./01-shot-plan.md) | 已完成 |
| 风格选择 | [02-style-selection.md](./02-style-selection.md) | 已完成 |
| 主体与三视图 | [03-subjects-and-three-views.md](./03-subjects-and-three-views.md) | 已完成 |
| 图片提示词 | [04-image-prompts.md](./04-image-prompts.md) | 已完成 |
| 图生视频提示词 | [05-image-to-video-prompts.md](./05-image-to-video-prompts.md) | 已完成 |
| 状态快照 | [project-state.json](./project-state.json) | 已完成 |

## 交付内容

- 7 条静帧图片提示词，shot_id 从 `shot_01` 到 `shot_07` 贯通。
- 7 条图生视频提示词，使用相同 shot_id。
- 图片和视频均为占位，不依赖真实 API。
- 主讲人、风格、模型、provider 均引用 SSOT。

## 质量自检

- `style_key` 全程一致：`cyberpunk_bright_hud_infographic`
- `image_model` 全程一致：`GPT-Image-2`
- `video_provider` 全程一致：`grok`
- `visual_carrier` 全部使用 7 值规范集合。
- `scene_only`、`concept_explainer`、`ui_closeup`、`data_compare` 等非人物镜头覆盖足够，避免连续口播疲劳。
