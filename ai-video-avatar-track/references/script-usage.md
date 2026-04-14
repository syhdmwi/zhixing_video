# Script Usage

脚本路径：

- `scripts/digital_humans_batch.py`

## Required Env Var

- `DIGITAL_HUMANS_API_KEY`
  或
- `WUYINKEJI_API_KEY`

## Required Input

传入一个 JSON 队列文件，格式参考：

- [avatar-queue-example.json](./avatar-queue-example.json)

当前接口要求：

- `audio_url` 必须是公网可访问的音频链接
- `video_url` 必须是公网可访问的正面人物视频链接
- 文档说明里写明 `videoUrl` 时长不得低于 10 秒

## Example

```bash
DIGITAL_HUMANS_API_KEY="your-key" \
python3 scripts/digital_humans_batch.py \
  --queue-file references/avatar-queue-example.json \
  --poll-interval 30 \
  --timeout 600 \
  --out avatar-result.json
```

## Output

脚本会输出：

- `generation_queue`
- `execution_notes`
- `rendered_videos_for_review`

其中每个结果项至少包含：

- `segment_id`
- `video_name`
- `task_id`
- `status`
- `status_label`
- `render_url`
- `message`
- `updated_at`

默认 review 流程：

- 视频任务全部完成后，先展示数字人视频
- 再让用户确认是否满意
- 如果用户还没制作数字人，则先询问是否需要制作数字人；需要的话，再让用户提供音频和人物视频链接
