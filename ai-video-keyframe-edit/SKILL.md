---
name: ai-video-keyframe-edit
description: 当用户已经生成完静帧图片，并希望直接通过剪辑方式给这些图片添加轻微关键帧运镜，生成画面轨视频时使用这个 skill。它优先使用 FFmpeg 做自动化关键帧剪辑，不依赖图生视频模型。
---

# AI Video Keyframe Edit

## Overview

这个 skill 负责把“已经生成好的静帧图片”直接剪成一条带轻微关键帧运镜的视频轨。

它不走图生视频模型，不让人物表演，不让环境发生动画，而是通过剪辑层的轻微推拉、平移、上移、下移，做出类似剪映关键帧的效果。

默认目标是：

- 让静帧像关键帧一样轻微移动
- 人物、环境、道具保持静止
- 尽量避免模型幻觉、跑形、变脸
- 优先生成稳定的画面轨

## Recommended Tool

默认推荐实现工具：

- `FFmpeg`

原因：

- 最容易脚本化
- 不依赖图生视频模型
- 可以稳定批量处理
- 可以直接实现轻微推拉和平移
- 后面最容易接进 skill 工作流

不作为首选的工具：

- 剪映：用户手工使用体验很好，但公开自动化能力不稳定，不适合作为默认程序化方案
- Premiere：可以做，但更适合做插件或复杂编辑工具链，实施成本更高

## When To Use

- 用户已经确认了一批静帧图
- 用户想先做“图转镜头移动视频模式”
- 用户想避免图生视频的人物乱动、环境乱动
- 用户只需要轻微运镜感，不需要角色表演

## Core Rules

- 所有源素材都必须是用户已确认的静帧图片
- 默认不让人物动
- 默认不让环境动
- 默认不让道具动
- 只允许非常轻微的相机运动感
- 默认先做测试批次，再做全量
- 如果本机没有安装 `ffmpeg`，先产出剪辑任务单和命令计划，不强行伪执行

## Default Motion Presets

默认只用这 6 种轻运镜模板：

1. `subtle_pullback`：轻微后拉
2. `subtle_pushin`：轻微推进
3. `subtle_pan_left`：轻微左移
4. `subtle_pan_right`：轻微右移
5. `subtle_pan_up`：轻微上移
6. `subtle_pan_down`：轻微下移

默认每张图只选一个，不做复杂组合动作。
默认批量模式下会自动在这 6 个方向里随机分配，并保证前一张和后一张不使用同一个方向。
默认所有方向统一使用同一套正式强度：

- `duration_seconds = 8`
- `fps = 50`
- `motion_curve = linear`
- `zoom_strength = 0.10`
- `pan_strength = 0.10`

也就是说，前后左右上下六个方向都默认按同一档速度和强度执行。

补充说明：

- 左右上下使用统一的平移实现
- 前后推拉保留相同默认值，但内部使用更稳的高精度裁切再缩回成片尺寸的实现
- 这样可以尽量减少推拉镜头比平移镜头更容易出现的抖动感

## Default Workflow

### 1. Confirm Images Are Approved

只有用户已经确认图片后，才进入本 skill。

### 2. Choose The Keyframe Edit Branch

在“全部生图完成”后，默认给用户两个分支：

- 进入 `图转镜头移动视频模式`
- 进入 `图生视频模式`

如果用户选择本分支，就不再走图生视频模型。

### 3. Build A Keyframe Edit Queue

每张图片至少要有：

- `shot_id`
- `source_image`
- `duration_seconds`
- `output_name`

`motion_preset` 可省略。省略后脚本会自动分配关键帧方向，默认规则是：

- 在左 / 右 / 上 / 下 / 前 / 后 6 个方向里随机分配
- 相邻镜头方向不能相同
- 优先让整批镜头的运镜方向有变化，避免连续重复

如果队列里没有手动写：

- `duration_seconds`
- `fps`
- `motion_curve`
- `zoom_strength`
- `pan_strength`

就默认使用上面的正式参数。

### 4. Render With FFmpeg

如果本机有 `ffmpeg`：

- 对每张图片执行单独的关键帧运镜
- 生成单镜头视频
- 最后按顺序拼接成一条画面轨

如果本机没有 `ffmpeg`：

- 先输出剪辑任务单
- 输出可直接运行的命令计划
- 等安装好 `ffmpeg` 后再执行

### 5. Show The Result

生成成功后，直接展示：

- 每个镜头的视频
- 或最终拼好的画面轨

## Output

至少输出：

- `shot_id`
- `source_image`
- `motion_preset`
- `duration_seconds`
- `edit_mode`
- `render_plan`
- `output_path`

如果是批量执行，还应输出：

- `concat_plan`
- `final_video_path`

## References

- 使用说明： [references/script-usage.md](./references/script-usage.md)
- 队列示例： [references/keyframe-queue-example.json](./references/keyframe-queue-example.json)
- 执行脚本： [scripts/ffmpeg_keyframe_batch.py](./scripts/ffmpeg_keyframe_batch.py)
