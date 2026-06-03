# 02 Style Selection

SSOT 引用：
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)
- 模型清单：[../../MODELS.md](../../MODELS.md)
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)
- 示例模板：[../../templates/cyber-host-template.json](../../templates/cyber-host-template.json)

## 已选参数

| 项 | 值 |
| --- | --- |
| template_id | `cyber-host-template` |
| style_key | `cyberpunk_bright_hud_infographic` |
| style_preset_ref | `ai-video-image-prompts/references/style-presets.md` |
| aspect_ratio | `16:9` |
| image_model | `GPT-Image-2` |
| video_provider | `grok` |
| language | `中文` |

## 风格摘要

使用 `style-presets.md` 中 `style_key = cyberpunk_bright_hud_infographic` 的完整 `style_block`、6 组风格基因和负面约束。本文档不复制风格基因 JSON。

## 全局约束

- 主讲人沿用 `templates/cyber-host-template.json` 的 `host_cyber_female_01`。
- 所有正式图片提示词使用同一 `style_key`。
- 画面文字只做结构提示，不承担长段叙事。
- 生图模型规范名使用 `MODELS.md` 中的 `GPT-Image-2`。
- 图生视频 provider 规范名使用 `MODELS.md` 中的 `grok`。
- 分镜分类只使用 `visual_carrier` 7 值规范集合。
