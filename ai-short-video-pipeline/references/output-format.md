# Output Format

默认输出分为 9 段。除非用户要求更短，否则尽量按这个顺序交付。

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

## 1.55 文案类型判断

在剧本解析后、信息单元表前输出。至少包含：

- 【主类型】观点输出 / 教学解释 / 新闻信息 / 对比论证 / 案例拆解 / 情绪叙事
- 【副类型】如有混合结构，写第二类型
- 【镜头语言建议】这篇文案后续更适合人物口播、概念解释、界面图、数据对比，还是情绪场景

## 1.57 信息单元表

在正式分镜表之前输出，作为镜头规划的直接输入。每个信息单元至少包含：

- `unit_id`
- `source_text`
- `claim_type`
- `importance`
- `visual_carrier`

这里先拆“信息单元”，不要先拆“镜头”。

## 1.6 镜头功能与视觉承载表

在空间锁定卡之前输出。每个镜头至少包含：

- `shot_id`
- `unit_id`
- `shot_function`
- `visual_carrier`
- `visual_goal`

推荐枚举值：

- `shot_function`：`hook` / `setup` / `explain` / `compare` / `evidence` / `transition` / `emotion_push` / `cta`
- `visual_carrier`：使用 [../SKILL.md](../SKILL.md) 的 `3.4 视觉承载层` 定义，不在输出格式文件维护第二份枚举

## 1.65 空间锁定卡

只对需要真实空间逻辑的镜头输出。每个场景各一张卡。至少包含：

- 【环境锚点】≥3个固定参照物及其位置
- 【光线方向】主光源和辅助光的来源、方向、色温
- 【人物站位】默认位置和备选位置
- 【轴线管理】视线轴线和情绪轴线
- 【机位参考】默认景别、距离、高度

## 2. Immutable Blocks

使用以下结构：

### Character Block

用一段完整文字描述主角，不拆成碎词。

至少补充一个字段：

- `character_render_mode`

默认值：

- `stylized_illustration`

可选值建议：

- `stylized_illustration`
- `anime_illustration`
- `3d_stylized`
- `sketch_illustration`
- `photorealistic`（仅用户明确要求时启用）

### Style Block

用一段完整文字描述全片统一视觉风格。

### Negative Block

列出需要在所有镜头中持续规避的问题。

## 3. Shot List

每个镜头都要有以下字段：

| Field | Meaning |
| --- | --- |
| `shot_id` | 镜头编号 |
| `unit_id` | 对应信息单元编号 |
| `time_range` | 时间范围 |
| `narration_excerpt` | 对应口播片段 |
| `shot_function` | 该镜头在整条视频里的功能 |
| `visual_carrier` | 该镜头采用的人物/场景/概念/界面承载方式 |
| `visual_goal` | 该镜头的表达目标 |
| `frame_type` | 兼容字段，可保留旧系统枚举 |
| `image_prompt_cn` | 对应中文提示词，给用户直接查看 |
| `image_prompt` | 生图提示词 |
| `image_to_video_prompt_cn` | 对应中文视频提示词，给用户直接查看 |
| `image_to_video_prompt` | 图生视频提示词 |
| `edit_note` | 转场、字幕、强调元素、节奏说明 |

用户侧展示规则：

- 展示分镜表时，默认同时展示 `narration_excerpt` 和 `image_prompt_cn`
- 不要只给英文 `image_prompt`
- 如果后续进入视频阶段，默认同时展示 `narration_excerpt` 和 `image_to_video_prompt_cn`
- 英文提示词保留为执行层字段，中文提示词负责给用户阅读和校对
- 正式生图结果只能逐张展示，不能用总览图、拼图墙、联系表、宫格图替代
- 每张正式生图结果都必须继续保留 `shot_id`、`narration_excerpt`、`image_prompt_cn`

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

- 主讲人或核心主体在哪些镜头出现
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
