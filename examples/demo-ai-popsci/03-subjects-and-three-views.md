# 03 Subjects And Three Views

SSOT 引用：
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)，本例使用 `style_key=cyberpunk_bright_hud_infographic`
- 模型清单：[../../MODELS.md](../../MODELS.md)，三视图静帧使用 `GPT-Image-2`，后续视频使用 `grok`
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)
- 主体一致性：[../../ai-video-image-prompts/references/subject-consistency-rules.md](../../ai-video-image-prompts/references/subject-consistency-rules.md)
- 三视图模板：[../../ai-video-image-prompts/references/three-view-template.md](../../ai-video-image-prompts/references/three-view-template.md)
- 示例模板：[../../templates/cyber-host-template.json](../../templates/cyber-host-template.json)

## 重复主体清单

| subject_id | 类型 | 是否需要三视图 | 说明 |
| --- | --- | --- | --- |
| host_cyber_female_01 | 主讲人 | 是 | 来自 `cyber-host-template.json`，全片固定身份锚点 |
| ai_agent_core_01 | 抽象主体 | 是 | AI 智能体核心，表现为发光任务中枢 |
| workflow_board_01 | 抽象主体 | 否 | 流程看板，可随镜头变化但保持同一风格 |

## 主讲人三视图提示词

```text
Subject reference sheet, one character only, white background, front view + side view + back view in one clean layout. Character: young female AI explainer host, long black hair, red floral off-shoulder dress, calm confident expression, stylized commercial tech illustration, not photorealistic. Preserve same face shape, hairstyle, dress, and identity across all three views. style_key: cyberpunk_bright_hud_infographic. No scene background, no extra characters, no text labels, no multiple outfits.
```

[占位：主讲人白底三视图图像，subject_id=host_cyber_female_01]

## AI 智能体核心三视图提示词

```text
Abstract technology asset reference sheet, one object only, white or light gray background, front view + side view + back view in one clean layout. Subject: AI agent core represented as a floating translucent hexagonal processor hub with small connected task nodes, premium commercial tech illustration, glowing cyan and violet accents, clean HUD design language. Keep the same silhouette, materials, node layout, and scale across views. style_key: cyberpunk_bright_hud_infographic. No mascot character, no chibi proportions, no hardware product photography, no text labels.
```

[占位：AI 智能体核心三视图图像，subject_id=ai_agent_core_01]

## 确认状态

- `subjects_identified`: true
- `subjects_confirmed`: true
- `three_views_generated`: true
- `three_views_confirmed`: true
