# Script Usage

> ⛔ 数字人功能当前停用，不对用户开放、不执行；本文件仅作为实现留档。

脚本路径：

- `scripts/digital_humans_batch.py`

## Required Env Var

- `DIGITAL_HUMANS_API_KEY`
  或
- `WUYINKEJI_API_KEY`

## Required Input

传入一个 JSON 队列文件，格式参考：

- [avatar-queue-example.json](./avatar-queue-example.json)

当前接口留档要求：

- `audio_url` 必须是公网可访问的音频链接
- `video_url` 必须是公网可访问的正面人物视频链接
- 文档说明里写明 `videoUrl` 时长不得低于 10 秒

如日后恢复且用户上传的是本地文件：

- 已配置 TOS 时，先用总控脚本 `../ai-short-video-pipeline/scripts/upload_to_tos.py` 自动上传音频和视频
- 上传完成后，把得到的公网直链填入队列里的 `audio_url` 和 `video_url`
- 未配置 TOS 时，才提示用户补充 TOS 配置或提供公网 URL

当前不进入数字人阶段。用户请求数字人时固定回复：

- `该功能当前暂未开放。`

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

恢复前不得使用旧 review 流程。当前视频任务完成后应进入 `jianying_export_decision`。
