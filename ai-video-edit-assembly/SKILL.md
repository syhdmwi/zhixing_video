---
name: ai-video-edit-assembly
description: 当用户已经分别生成了数字人视频轨和画面视频轨，接下来要把两者剪成一条完整短视频时使用这个 skill。它负责转场、覆盖关系、字幕、音乐、封面和平台导出建议。
---

# AI Video Edit Assembly

## Overview

这个 skill 只负责后期整合。输入是至少两条素材轨：

- 数字人视频轨
- 画面视频轨

## When To Use

- 数字人素材和画面素材已经分别生成
- 用户要做最终成片
- 用户要适配抖音、视频号、小红书

## Core Rules

- 不重新设计前期分镜，除非明显冲突
- 优先保证口播信息传达完整
- B-roll 覆盖不能破坏关键口型同步段
- 平台导向优先考虑竖屏节奏和开头钩子

## Output

至少输出：

- 成片结构概述
- 时间线整合建议
- 每段素材覆盖关系
- 字幕强调点
- BGM/SFX 建议
- 封面与 CTA 建议
- 平台导出建议

### 剪映交付包（手动导入）

如用户需要在剪映国内版继续二次创作，额外输出一份手动导入交付包：

- 规范命名素材：按 `shot_id` 对齐视频、音频、数字人和 B-roll 素材。
- 时间线清单：`timeline.csv`，列出每个镜头的起止时间、轨道、素材文件、转场和 BGM 标记。
- 字幕文件：标准 `subtitles.srt`，用于剪映导入字幕。
- 交付清单：`delivery-manifest.json`，记录项目、镜头、轨道和交付文件。
- 导入指引：参考 [references/jianying-handoff-guide.md](references/jianying-handoff-guide.md)，只采用手动导入路线。
