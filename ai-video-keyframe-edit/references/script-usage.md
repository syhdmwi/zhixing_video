# Script Usage

脚本：

- [scripts/ffmpeg_keyframe_batch.py](../scripts/ffmpeg_keyframe_batch.py)

## Purpose

把一批静帧图片转成“关键帧轻运镜”视频片段，并在可用时拼接成最终画面轨。

## Example

```bash
python3 scripts/ffmpeg_keyframe_batch.py \
  --queue-file /path/to/keyframe-queue.json \
  --out-dir /path/to/out \
  --fps 50
```

如果当前机器没装 `ffmpeg`，脚本会保留任务单和命令计划，但不会假装执行成功。

## Queue Fields

每个项目至少包含：

- `shot_id`
- `source_image`
- `duration_seconds`
- `output_name`

可选字段：

- `motion_preset`
- `resolution`
- `fps`
- `zoom_strength`
- `pan_strength`
- `motion_curve`
- `oversample_factor`

如果这些字段省略，当前默认值是：

- `duration_seconds = 8`
- `fps = 50`
- `motion_curve = linear`
- `zoom_strength = 0.10`
- `pan_strength = 0.10`

这套默认值对所有方向统一生效：
- 向左
- 向右
- 向上
- 向下
- 向前
- 向后

补充说明：

- 向左、向右、向上、向下使用统一平移实现
- 向前、向后保留相同默认值，但内部使用更稳的高精度推拉渲染方式

## Motion Assignment

如果 `motion_preset` 省略，或写成 `auto`，脚本会自动分配关键帧方向：

- 可用方向：左、右、上、下、前、后
- 分配顺序默认随机
- 但会保证相邻镜头方向不同

## Output

输出目录里默认包含：

- 单镜头渲染计划
- `ffmpeg` 命令计划
- 拼接清单
- 最终输出路径（如果成功执行）
