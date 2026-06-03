---
name: ai-video-motion-prompts
description: 当用户已经有静帧图片，接下来要为图生视频生成运动提示词时使用这个 skill。它强调基于已确认的静帧生成低风险、易执行、主体可轻微动作的图生视频提示词。
---

# AI Video Motion Prompts

## Overview

这个 skill 只负责“静帧到图生视频”的动作设计，不负责静帧生图，也不负责数字人视频轨。输入应当是已经通过一致性检查的静帧。

默认目标不是给每张图写复杂动作脚本，而是先稳定地让人物、机器人或场景产生小幅、自然、低风险的可用动作。

这个 skill 的职责是：

1. 读取已经生成成功的静帧
2. 为每张图判断动作类型和动作强度
3. 输出适用于图生视频模型的可执行动作提示词
4. 先让用户确认测试批次，再进入图生视频阶段

默认不要把数字人视频轨混进来。数字人视频轨仍然由 `ai-video-avatar-track` 单独处理。

## When To Use

- 用户已经有图片
- 用户要把图片转成短视频镜头
- 用户要让图里的人物、机器人或环境轻微动起来

## Required Inputs

- 已生成成功并通过确认的静帧图片
- `shot_id` 顺序
- 每张图对应的文案含义或 `visual_goal`
- 目标平台和画幅
- 单镜头时长偏好
- 整体运动风格
- 是否先做测试批次
- 当前镜头里谁是主主体
- 当前镜头更偏讲述、展示、情绪还是场景

## Core Rules

- 先确认静帧可用，再写图生视频提示词
- 人物一致性优先于复杂运动
- 默认不写夸张表演或大动作编排
- 先判断 `motion_type`，再判断 `motion_intensity`
- 不要求夸张形变、瞬间换装或不现实的多段动作
- 人物镜头尽量避免大幅转头、夸张嘴型、复杂肢体重构
- 纯场景镜头也应保持小幅、可控运动
- 正式全量生成前，默认优先先做 5 到 10 张测试批次

## Default Motion Types

`motion_type` 定义与 `motion_intensity` 规则以 [image-to-video-prompt-rules.md](../ai-video-generate-videos/references/image-to-video-prompt-rules.md) 的 `§3 Motion Types` 和 `§4 Motion Intensity` 为唯一权威。

动作模板与已验证提示词见：

- [references/image-to-video-prompt-rules.md](../ai-video-generate-videos/references/image-to-video-prompt-rules.md)
- [references/motion-template-library.md](../ai-video-generate-videos/references/motion-template-library.md)

## Keyframe-Light Fallback

如果用户希望“生成的图片去生成视频时，只像关键帧那样轻微移动，人物和环境基本静止”，默认新增这一套模板：

- `关键帧轻运镜模板01`

适用特点：

- 人物静止
- 环境静止
- 道具静止
- 不追求角色表演
- 不追求肢体动作
- 只追求非常轻的镜头位移感

默认思路：

- 把视频理解成“静帧被轻微推镜、左右平移或后拉”
- 主体像海报或关键帧一样基本不动
- 整个画面只允许非常轻的相机运动
- 不允许人物、角色、环境发生明显动画变化

关键帧轻运镜的收紧稳定性正文以 [image-to-video-prompt-rules.md](../ai-video-generate-videos/references/image-to-video-prompt-rules.md) 的 `§5 Default Safe Rules` 为准。

当用户明确提到：

- 像关键帧一样动
- 画面只需要轻微移动
- 人物和环境都静止
- 不要人物动作

就优先套用这套模板，而不是默认动作模板。

## Default Stability Preset

默认稳定性约束以 [image-to-video-prompt-rules.md](../ai-video-generate-videos/references/image-to-video-prompt-rules.md) 的 `§5 Default Safe Rules` 为唯一权威。

如果用户没有特别要求，每条图生视频提示词都应默认附带该安全规则，不要遗漏。

## Default Workflow

### 1. Confirm The Source Images Are Approved

只有当静帧已经生成并且用户认可后，才进入本 skill。

如果图片还没确认，先回到 `ai-video-prompt-to-images`，不要跳过图片确认直接做动作提示词。

### 2. Ask The Motion Intake Questions

至少先确认：

- 这批图是否先只做测试批次
- 单镜头目标时长是几秒
- 每张图更适合哪一种动作类型
- 动作强度是否保持低动态优先

如果用户没特别说，默认：

- 先做 `5` 到 `10` 张测试批次
- 单镜头 `4` 到 `5` 秒
- `low` 动态优先
- 人物镜头保守优先

### 3. Assign One Motion Type To Each Image

在写动作提示词前，先判断每张图更适合哪一种动作类型：

- 主讲人表达观点，优先 `讲述型`
- 机器人或吉祥物解说，优先 `展示型`
- 沉思、压迫、悲伤、犹豫，优先 `情绪型`
- 办公室、法庭、会议室、城市环境，优先 `场景型`
- 强对比、强冲突、强情绪峰值，才考虑 `冲突型`

不要给一张图同时塞多个复杂动作目标。

### 4. Build Motion Prompts From Templates

默认动作提示词应当尽量短，直接可执行，例如：

- The host makes a slight natural head movement and subtle breathing motion, with a very small hand gesture near the body. The camera gently pushes in. Keep the face, hairstyle, outfit, body proportions, and background composition unchanged.
- The robot makes a slight head turn and a small arm movement as if explaining something. The camera gently pushes in. Keep the robot design, proportions, materials, background structure, and original art style unchanged.
- The person shows subtle breathing, a slight downward or upward head movement, and a very small eye-line change. The camera slowly pushes in. Keep the face, hairstyle, outfit, body proportions, and original art style unchanged.

如果用户要“关键帧感”，默认提示词应改成更收紧的版本，例如：

- 画面像关键帧插画一样基本静止，人物、环境、主要角色和道具全部保持固定不动，只做非常轻微的相机向左平移
- 画面像关键帧插画一样基本静止，人物、环境、主要角色和道具全部保持固定不动，只做非常轻微的相机向右平移
- 画面像关键帧插画一样基本静止，人物、环境、主要角色和道具全部保持固定不动，只做非常轻微的相机后拉远
- 纯场景竖向空间镜头可使用非常轻微的相机向上或向下移动；人物镜头不用

不要在默认模板之外额外加长段说明，除非用户明确要求。

### 5. Let The User Confirm The Motion Batch

动作提示词写完后，不要直接默认进入图生视频执行。先让用户确认：

- 哪些镜头方向合适
- 哪些镜头方向想换
- 是否需要先只跑测试批次

### 6. Pass The Approved Motion Batch Forward

只有当用户确认动作设计后，才进入图生视频执行阶段。

如果后面要补图生视频 API 或执行脚本，应由本 skill 的后续脚本层承接，但不要在这里编造平台私有参数。

## Prompt Structure

每个镜头至少说明：

- 主体动作
- 镜头运动
- 风格保持
- 防止脸漂和肢体畸变的约束

推荐结构：

```text
[Source image summary]
[Motion type and subject action]
[Camera motion]
[Style lock]
[Default stability preset]
```

## Output

每个镜头至少产出：

- `shot_id`
- `source_image_requirement`
- `motion_type`
- `motion_intensity`
- `camera_motion`
- `default_stability_preset`
- `motion_prompt`
- `stability_note`
- `risk_note`

如果是批量输出，至少还应包含：

- `recommended_duration_seconds`
- `test_batch_priority`

## References

- 动作设计规则： [references/motion-design-rules.md](./references/motion-design-rules.md)
- 图生视频提示词规则： [references/image-to-video-prompt-rules.md](../ai-video-generate-videos/references/image-to-video-prompt-rules.md)
- 动作模板库： [references/motion-template-library.md](../ai-video-generate-videos/references/motion-template-library.md)
- 输出模板： [references/output-template.md](./references/output-template.md)
- openclaw 示例： [references/openclaw-motion-example.json](./references/openclaw-motion-example.json)
