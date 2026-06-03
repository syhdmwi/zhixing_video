# 05 Image To Video Prompts

SSOT 引用：
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)，沿用 `style_key=cyberpunk_bright_hud_infographic`
- 模型清单：[../../MODELS.md](../../MODELS.md)
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)
- 图生视频规则：[../../ai-video-generate-videos/references/image-to-video-prompt-rules.md](../../ai-video-generate-videos/references/image-to-video-prompt-rules.md)
- 运动模板库：[../../ai-video-generate-videos/references/motion-template-library.md](../../ai-video-generate-videos/references/motion-template-library.md)

全局取值：静帧来自 `GPT-Image-2` 占位图，图生视频 provider 为 `grok`。所有提示词从已批准静帧出发，保持主体、服装、脸、道具和构图稳定。

| shot_id | visual_carrier | video_prompt | placeholder |
| --- | --- | --- | --- |
| shot_01 | host_primary | Starting from the approved still frame, keep the host's face, dress, hair, and pose stable. Add a very slow camera push-in and subtle HUD glow pulses. No walking, no mouth movement, no hand motion, no face drift. | [占位：shot_01 视频] |
| shot_02 | host_with_visual | Starting from the approved still frame, keep the host and AI core fixed. Let the thin task lines gently light up from host to AI core while camera drifts slightly right. No character animation, no redesign. | [占位：shot_02 视频] |
| shot_03 | ui_closeup | Starting from the approved still frame, keep all UI windows in the same positions. Add a slow parallax push through the layered panels and tiny glow flickers. No new text, no window reshuffle. | [占位：shot_03 视频] |
| shot_04 | concept_explainer | Starting from the approved still frame, keep the diagram layout stable. Let the connection lines illuminate in order from goal to plan, tools, and review. Camera remains steady with minimal zoom. | [占位：shot_04 视频] |
| shot_05 | brand_symbolic | Starting from the approved still frame, keep all generic tool icons stable. Add a gentle clockwise light sweep around the loop and a final verification glow. No real logo generation, no icon morphing. | [占位：shot_05 视频] |
| shot_06 | data_compare | Starting from the approved still frame, keep the split-screen composition fixed. Add a subtle contrast pulse: left side dims slightly, right side brightens. No object movement except UI glow. | [占位：shot_06 视频] |
| shot_07 | scene_only | Starting from the approved still frame, keep the workflow board fixed. Add a slow pull-back revealing the complete connected flow and a soft final checkmark glow. No people, no new text. | [占位：shot_07 视频] |

## 执行说明

- 本 demo 不调真实 API。
- 所有视频只以提示词和占位说明呈现。
- 若真实执行，队列中的 `provider` 使用 `grok`，规范名来自 `MODELS.md`。
