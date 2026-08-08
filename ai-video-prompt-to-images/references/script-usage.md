# Script Usage

当前唯一启用的正式生图脚本：

- `scripts/gpt_image2_batch.py`

`scripts/nanobanana2_batch.py` 已停用，直接运行会在读取 API key 或发起网络请求前退出。

## Required Env Var

- `YIJIA_API_KEY`

## API Contract

- 文档：[一加 Image-2 图片生成](https://dvqyn6o2vd.apifox.cn/447322097e0)
- Endpoint：`POST https://api.yijiarj.cn/v1/chat/completions`
- 鉴权：`Authorization: Bearer ${YIJIA_API_KEY}`
- API model：`image2`
- 请求字段：`messages`、`model`、`size`
- 参考图：在 `messages[0].content` 中使用 `image_url` 项，可传多张公网图片
- 返回结果：从 `choices[0].message.content` 的 Markdown 图片链接中提取图片 URL

脚本会把常用画幅映射到接口支持的尺寸：

- `16:9` -> `1792x1024`
- `9:16` -> `1024x1792`
- `1:1` -> `1024x1024`
- `21:9` -> `1920x822`
- `9:21` -> `822x1920`

## Required Input

传入一个 JSON 队列文件，格式参考：

- [generation-queue-example.json](./generation-queue-example.json)

## Example

```bash
YIJIA_API_KEY="your-key" \
python3 scripts/gpt_image2_batch.py \
  --queue-file references/generation-queue-example.json \
  --aspect-ratio 16:9 \
  --max-retries 1 \
  --out batch-result.json
```

## Output

脚本同步逐镜提交，并输出：

- `generation_queue`
- `execution_notes`
- `qc_checklist`
- `rendered_images_for_review`

每个队列项保留 `shot_id`、规范模型名、API model、尺寸、响应 ID、图片 URL、重试记录与下一步动作。生成成功后，应按 `shot_id` 顺序直接展示图片，再让用户确认保留或回炉的镜头。
