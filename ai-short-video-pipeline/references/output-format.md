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

## 6. Editing Notes

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
