---
name: zhixing_video
description: 知行视频主入口 skill。对外只暴露这一个入口，负责把用户从文案带到分镜、图片、视频、语音、数字人和模板复用。内部仍保留模块化规则与脚本，但用户不需要理解内部模块名。
---

# Zhixing Video

## Overview

这是对外唯一主入口。

用户不应该再被要求理解一组分散的 skill 名称。无论用户说：

- `使用知行视频skill`
- `知行视频 skill`
- `知行视频工作流`
- `帮我从文案开始做视频`

都先进入这个根入口，再由它把任务分派到内部模块。

## User-Facing Rule

对用户只暴露一套主流程，不暴露内部模块名，不要求用户自己判断该读哪个模块。

优先按用户任务理解为这四类：

1. 从文案开始做图片
2. 从图片继续做视频
3. 做数字人
4. 从文案一路做到视频

如果用户是第一次使用，或表达里有：

- `不会用`
- `小白`
- `你带我走`
- `不知道下一步`

则不要先解释内部模块、provider、脚本、队列、TOS 或 API。

## Workflow

主流程阶段顺序以 [ai-short-video-pipeline/references/workflow-state-machine.md](./ai-short-video-pipeline/references/workflow-state-machine.md) 的 `Stage List` 与 `Allowed Transitions` 为唯一权威；根入口只负责用用户能理解的话转述当前阶段，不维护第二套步骤表。

用户侧叙述时，仍按同一条状态机推进：接收文案或现有素材，确认风格、图片比例和生图模型，完成主体、三视图、提示词、生图、审图、视频生成、数字人或模板保存等阶段。任何阶段跳入都先回到状态机检查前置条件。

## Internal Modules

内部模块继续保留，但只作为实现层，不作为用户入口：

- [ai-short-video-pipeline/MODULE.md](./ai-short-video-pipeline/MODULE.md)
- [ai-video-shot-planner/MODULE.md](./ai-video-shot-planner/MODULE.md)
- [ai-video-image-prompts/MODULE.md](./ai-video-image-prompts/MODULE.md)
- [ai-video-prompt-to-images/MODULE.md](./ai-video-prompt-to-images/MODULE.md)
- [ai-video-motion-prompts/MODULE.md](./ai-video-motion-prompts/MODULE.md)
- [ai-video-generate-videos/MODULE.md](./ai-video-generate-videos/MODULE.md)
- [ai-video-keyframe-edit/MODULE.md](./ai-video-keyframe-edit/MODULE.md)
- [ai-video-voice-tts/MODULE.md](./ai-video-voice-tts/MODULE.md)
- [ai-video-voice-clone/MODULE.md](./ai-video-voice-clone/MODULE.md)
- [ai-video-avatar-track/MODULE.md](./ai-video-avatar-track/MODULE.md)
- [ai-video-series-archive/MODULE.md](./ai-video-series-archive/MODULE.md)
- [ai-video-edit-assembly/MODULE.md](./ai-video-edit-assembly/MODULE.md)

## Delegation Rule

根入口负责调度，不自己重写所有细节规则。

执行时优先这样分派：

- 文案理解、状态机、主流程判断 -> `ai-short-video-pipeline/MODULE.md`
- 分镜结构、信息单元、镜头功能 -> `ai-video-shot-planner/MODULE.md`
- 图片提示词、风格预设、三视图 -> `ai-video-image-prompts/MODULE.md`
- 正式生图执行 -> `ai-video-prompt-to-images/MODULE.md`
- 图生视频动作方案 -> `ai-video-motion-prompts/MODULE.md`
- 视频真实提交 -> `ai-video-generate-videos/MODULE.md`
- 图转镜头移动视频 -> `ai-video-keyframe-edit/MODULE.md`
- TTS / 语音克隆 -> `ai-video-voice-tts/MODULE.md`、`ai-video-voice-clone/MODULE.md`
- 数字人 -> `ai-video-avatar-track/MODULE.md`
- 模板保存与样例归档 -> `ai-video-series-archive/MODULE.md`
- 最终整合 -> `ai-video-edit-assembly/MODULE.md`

## Critical Constraints

- 对外只能表现为一个工作流，不表现为多个分散 skill。
- 正式生图必须一镜一任务，不允许把多个分镜合成一张。
- 正式生图阶段禁止总览图、拼图墙、联系表。
- 正式图片与视频展示必须逐张展示，并带 `shot_id`、原文片段、中文提示词。
- 用户不满意时默认改单张，不整批重跑。

## First Reply Template

第一次被用户唤醒时，优先用这种表达：

```text
可以。你把文案、图片、音频或人物视频发我，我按知行视频skill的主流程带你往下走。
```

如果用户只说唤醒词，没有素材，优先问：

```text
你想用知行视频skill做哪一步？
1. 从文案开始做图片
2. 从图片继续做视频
3. 做数字人
4. 从文案一路跑完整流程
```
