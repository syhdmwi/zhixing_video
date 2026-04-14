# Script Usage

脚本路径：

- `scripts/nanobanana2_batch.py`

## Required Env Var

- `NANOBANANA_API_KEY`

## Required Input

传入一个 JSON 队列文件，格式参考：

- [generation-queue-example.json](./generation-queue-example.json)

## Example

```bash
NANOBANANA_API_KEY="your-key" \
python3 scripts/nanobanana2_batch.py \
  --queue-file references/generation-queue-example.json \
  --aspect-ratio 16:9 \
  --size 1K \
  --max-stuck-retries 1 \
  --out batch-result.json
```

## Output

脚本会输出：

- `generation_queue`
- `execution_notes`
- `qc_checklist`

在支持图片展示的客户端里，脚本返回的成功结果不应只作为数据保存。默认还应把生成成功的 `result` 图片按 `shot_id` 顺序直接展示给用户确认。

其中每个队列项会带：

- `shot_id`
- `task_id`
- `status`
- `status_label`
- `result`
- `message`
- `retry_attempts_used`
- `next_action`
- `attempts`

其中 `attempts` 会保留每次提交后的历史 `task_id`、状态和是否超时，便于平台卡住时继续排查或手动重提。

## Review Step

默认 review 流程：

- 先展示图片
- 再给链接
- 再让用户指出要保留或要修改的镜头
