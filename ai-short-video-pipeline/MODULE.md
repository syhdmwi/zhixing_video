# AI Short Video Pipeline（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户想把一段文案或口播稿制作成完整的 AI 短视频流程时使用的总控 skill，负责判断何时调用分镜、图片提示词、图生视频、TTS 配音、剪映交付包等子 skills；数字人与语音克隆当前停用。

## 关键 references

- [references/workflow-state-machine.md](./references/workflow-state-machine.md) — 主流程状态机
- [references/project-state-template.json](./references/project-state-template.json) — 项目状态模板
- [references/intake-checklist.md](./references/intake-checklist.md) — 输入收集清单
- [references/prompt-generation-rules.md](./references/prompt-generation-rules.md) — 提示词生成规则
- [references/output-format.md](./references/output-format.md) — 结构化输出格式
- [references/consistency-rules.md](./references/consistency-rules.md) — 一致性规则
- [references/quality-review-loop.md](./references/quality-review-loop.md) — 质量审核回环
- [references/user-guidance-templates.md](./references/user-guidance-templates.md) — 用户引导话术
- [references/polling-progress-rules.md](./references/polling-progress-rules.md) — 轮询进度规则
- [references/provider-config-template.md](./references/provider-config-template.md) — provider 配置模板
- [references/style-gene-structure.md](./references/style-gene-structure.md) — 风格基因结构
- [references/suite-architecture.md](./references/suite-architecture.md) — 套件架构说明

## 上下游

上游：根 [../SKILL.md](../SKILL.md) 或用户直接唤醒 / 下游：按阶段调度各 `ai-video-*` 模块。
