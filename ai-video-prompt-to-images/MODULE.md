# AI Video Prompt To Images（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户已经确认一批图片提示词、接下来要正式进入生图阶段时使用，负责保持提示词顺序、比例、主体一致性与场景/人物分配。

## 关键 references

- [references/batch-execution-checklist.md](./references/batch-execution-checklist.md) — 批量执行检查清单
- [references/generation-queue-example.json](./references/generation-queue-example.json) — 生图队列示例
- [references/script-usage.md](./references/script-usage.md) — 脚本使用说明

## 上下游

上游：`ai-video-image-prompts` / 下游：`ai-video-motion-prompts`、`ai-video-keyframe-edit`、图片确认阶段。
