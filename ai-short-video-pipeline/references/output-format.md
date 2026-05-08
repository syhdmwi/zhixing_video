# Output Format

默认输出分为 7 段。除非用户要求更短，否则尽量按这个顺序交付。

## 1. Project Summary

至少包含：

- 目标平台
- 画幅
- 目标时长或估算时长
- 总镜头数
- 主角设定一句话摘要
- 风格设定一句话摘要

## 1.5 剧本解析

在分镜表之前输出，作为后续所有步骤的结构化输入。至少包含：

- 【角色】每个角色的年龄、性别、职业气质、穿着、状态
- 【场景】每个场景的空间类型、光线条件、关键物品
- 【情绪线】按文案节奏分段的情绪变化
- 【色调线】对应情绪线的色调过渡
- 【关键动作】按时间顺序的动作节点
- 【道具/细节】需要出现的品牌、界面、道具等元素

## 1.6 空间锁定卡

剧本解析之后、分镜表之前输出。每个场景各一张卡。至少包含：

- 【环境锚点】≥3个固定参照物及其位置
- 【光线方向】主光源和辅助光的来源、方向、色温
- 【人物站位】默认位置和备选位置
- 【轴线管理】视线轴线和情绪轴线
- 【机位参考】默认景别、距离、高度

## 2. Immutable Blocks

使用以下结构：

### Character Block

用一段完整文字描述主角，不拆成碎词。

### Style Block

用一段完整文字描述全片统一视觉风格。

### Negative Block

列出需要在所有镜头中持续规避的问题。

## 3. Shot List

每个镜头都要有以下字段：

| Field | Meaning |
| --- | --- |
| `shot_id` | 镜头编号 |
| `time_range` | 时间范围 |
| `narration_excerpt` | 对应口播片段 |
| `visual_goal` | 该镜头的表达目标 |
| `frame_type` | `avatar` / `b-roll` / `split` |
| `image_prompt` | 生图提示词 |
| `image_to_video_prompt` | 图生视频提示词 |
| `edit_note` | 转场、字幕、强调元素、节奏说明 |

## 4. Prompt Writing Pattern

图片提示词推荐结构：

```text
[Character Block]
[Style Block]
[Shot-specific visual instructions]
[Composition and camera instructions]
[Negative Block]
```

图生视频提示词推荐结构：

```text
Starting from the approved still frame, describe subject motion, camera motion, environmental motion, pacing, and constraints that prevent face drift or body deformation.
```

## 5. Avatar Integration Plan

至少说明：

- 数字人在哪些镜头出镜
- 哪些口播片段适合被 B-roll 覆盖
- 哪些句子必须保留口型同步主画面

## 6.5 Quality Review Report

静帧全部生成后，展示给用户之前，先输出质量审核报告。

至少包含：

- 审核总览：总镜头数、通过数、需关注数
- 需关注镜头列表：每张列出 shot_id、问题类型、问题描述、严重程度（🔴/🟡/🟢）、建议操作
- 整体趋势：是否存在渐变漂移或整体性偏移
- 建议：下一步操作建议

严重程度分级：
- 🔴 必须修改：角色串脸、空间错乱、风格突变、肢体严重畸形
- 🟡 建议修改：服装细节微变、光线轻微偏差、构图略单调
- 🟢 轻微可忽略：色温差异、背景细节不同

如果存在 🔴 问题，在展示图片之前先展示报告，建议用户先处理。
如果全部通过，报告可以简短带过，直接展示图片。

详细审核维度见 [quality-review-loop.md](./quality-review-loop.md)。

## 7. Editing Notes

至少说明：

- 开头钩子如何落地
- 哪些位置需要快切
- 哪些位置适合放大字幕
- BGM 氛围建议
- SFX 使用建议
- 结尾 CTA 呈现方式

## 7. Export Checklist

至少检查：

- 所有镜头编号连续
- 角色设定前后一致
- 风格设定前后一致
- 时长与镜头数匹配
- 口播片段没有漏句
- 图生视频提示词不要求不现实的大幅变形运动
