# AI Video Generate Videos（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户已经有静帧图片和已确认的图生视频动作方案，接下来要真实提交视频生成任务时使用；当前默认使用 grok，seedance 暂时停用。

## 关键 references

- [references/grok-provider-notes.md](./references/grok-provider-notes.md) — grok provider 说明
- [references/grok-video-template-00.md](./references/grok-video-template-00.md) — grok 固定模板
- [references/omni-provider-notes.md](./references/omni-provider-notes.md) — omni provider 说明
- [references/seedance-provider-notes.md](./references/seedance-provider-notes.md) — seedance 停用说明
- [references/provider-queue-example.json](./references/provider-queue-example.json) — provider 队列示例
- [references/image-to-video-prompt-rules.md](./references/image-to-video-prompt-rules.md) — 图生视频提示词规则
- [references/motion-template-library.md](./references/motion-template-library.md) — 运动模板库
- [references/veo-provider-notes.md](./references/veo-provider-notes.md) — Veo provider 备注

## 上下游

上游：`ai-video-motion-prompts` / 下游：`ai-video-edit-assembly` 或结果展示。
