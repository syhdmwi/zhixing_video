# Seedance Provider Notes

当前已接入的 seedance 信息：

- provider 名：`seedance`
- 当前沿用火山方舟视频生成 API：
  - 创建任务：`POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
  - 查询任务：`GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`
  - 数据面 Base URL：`https://ark.cn-beijing.volces.com/api/v3`
  - 鉴权：`Authorization: Bearer <API Key>`
- 当前脚本支持从环境变量读取：
  - `ARK_API_KEY`
  - `SEEDANCE_API_KEY`
  - 优先使用 `ARK_API_KEY`

当前脚本按图生视频场景构造如下请求：

- `model`
- `content`
  - 文本项：`{"type":"text","text":"<motion_prompt>"}`
  - 首帧参考图项：`{"type":"image_url","image_url":{"url":"<source_image_url>"}}`
- `resolution`
- `ratio`
- 可选：`duration` / `frames` / `seed` / `camera_fixed` / `watermark` / `callback_url` / `return_last_frame`

当前状态解析规则：

- 运行中状态：`queued`、`running`
- 成功状态：`succeeded`
- 失败状态：`failed`、`expired`
- 成功后优先提取：
  - `content.video_url`
  - `content.video_urls[0]`
  - 再回退到顶层 `video_url` / `video_urls[0]`

注意：

- 官方文档明确了 `model`、`content`、`resolution`、`ratio`、`duration` 等参数，以及创建/查询路径和状态值。
- `content` 内部对象在当前文档页没有直接给出完整图生视频 JSON 样例。
- 目前脚本使用的是保守推断方案：`text + image_url` 的多模态 `content` 数组，用于首帧图生视频。
- 如果后续真实返回提示字段名不同，再按报错信息微调即可。
