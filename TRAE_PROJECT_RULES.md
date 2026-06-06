# Trae Project Rules

这份文件是给 Trae 直接粘贴到“项目规则 / Project Rules”里的强制规则模板。

目标不是解释工作流，而是防止 Trae 偷懒、跳步骤、忘记当前阶段。

## 直接粘贴给 Trae 的规则

```text
你现在在执行「知行视频skill」工作流。

这不是普通对话任务，而是一个必须按阶段推进的短视频生产流程。

强制规则：

1. 每次响应前，先检查当前流程阶段。
2. 如果用户只回复 1、2、全部生图、进入视频生成、保存模板 等短指令，禁止猜测，必须先结合当前阶段解释；做数字人、用我的声音读、语音克隆固定回复“该功能当前暂未开放”。
3. 如果当前阶段不明确，先输出“当前流程状态”，不要直接继续执行。
4. 缺少前置条件时，禁止跳步骤。
5. 禁止把多个确认环节合并省略。
6. 禁止因为你“觉得用户应该想要”就跳过主体确认、三视图确认、提示词确认、图片确认。
7. 用户没有确认图片满意前，禁止进入视频阶段。
8. 用户没有确认主体前，禁止生成正式提示词。
9. 用户没有确认正式提示词前，禁止批量生图。
10. 每次都要明确告诉用户：当前阶段、已完成内容、下一步、允许回复什么。

固定输出格式：

当前流程状态：
阶段：[current_stage]
已完成：[completed_items]
下一步：[next_action]
你可以回复：[allowed_user_replies]

如果用户要求继续下一步，但前置条件不满足，固定这样处理：

现在还不能执行这一步。
缺少：[missing_prerequisites]
下一步你需要先完成：[required_step]

必须优先读取这些文件并遵守：
- 用户使用说明.md
- ai-short-video-pipeline/SKILL.md
- ai-short-video-pipeline/references/workflow-state-machine.md
- ai-short-video-pipeline/references/project-state-template.json

如果这些文件之间有冲突，以 workflow-state-machine.md 和 ai-short-video-pipeline/SKILL.md 为最高优先级。
```

## 最推荐的 Trae 配置方式

把下面 4 个文件一起放进 Trae 的项目上下文：

1. [用户使用说明.md](./用户使用说明.md)
2. [ai-short-video-pipeline/SKILL.md](./ai-short-video-pipeline/SKILL.md)
3. [workflow-state-machine.md](./ai-short-video-pipeline/references/workflow-state-machine.md)
4. [project-state-template.json](./ai-short-video-pipeline/references/project-state-template.json)

然后把本文件里的“直接粘贴给 Trae 的规则”完整放进 Trae 的项目规则。

## 为什么这份文件有必要

Trae 的常见问题不是能力不够，而是：

- 它会把长文档压缩总结，漏掉细节
- 它会试图“帮用户省事”，于是跳过确认步骤
- 它会把 `1` / `2` 当成模糊 continuation，而不是阶段内选择
- 它会把 workflow 文档当建议，而不是必须执行的 gate

所以 Trae 需要的是“短、硬、可复制”的规则，而不是再给它一份更长的说明。
