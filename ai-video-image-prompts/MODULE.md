# AI Video Image Prompts（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户要把一段文案直接转换成一组可执行的生图提示词时使用，强调主体一致性、风格一致性和批量提示词结构。

## 关键 references

- [references/style-presets.md](./references/style-presets.md) — 风格预设 SSOT
- [references/reusable-template-system.md](./references/reusable-template-system.md) — 可复用模板系统
- [references/gpt-image2-prompt-template-01.md](./references/gpt-image2-prompt-template-01.md) — GPT-Image-2 提示词模板
- [references/nanobanana-prompt-template-01.md](./references/nanobanana-prompt-template-01.md) — nanobanana 提示词模板
- [references/subject-consistency-rules.md](./references/subject-consistency-rules.md) — 主体一致性规则
- [references/subject-consistency-template-01.md](./references/subject-consistency-template-01.md) — 主体一致性模板
- [references/subject-preview-workflow.md](./references/subject-preview-workflow.md) — 主体预览流程
- [references/character-approval-workflow.md](./references/character-approval-workflow.md) — 角色确认流程
- [references/character-review-template.md](./references/character-review-template.md) — 角色审核模板
- [references/three-view-template.md](./references/three-view-template.md) — 三视图模板
- [references/master-prompt-template.md](./references/master-prompt-template.md) — 母提示词模板
- [references/example-openclaw-master-prompt.md](./references/example-openclaw-master-prompt.md) — OpenClaw 示例母提示词
- [references/script-to-image-playbook.md](./references/script-to-image-playbook.md) — 文案转画面规则
- [references/execution-queue-template.json](./references/execution-queue-template.json) — 执行队列模板

## 上下游

上游：`ai-short-video-pipeline`、`ai-video-shot-planner` / 下游：`ai-video-prompt-to-images`、`ai-video-series-archive`。
