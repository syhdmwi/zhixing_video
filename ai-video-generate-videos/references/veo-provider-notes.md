# VEO Provider Notes

基于用户提供的一加 API 文档，当前可确认的 veo 链路：

## Create

- `POST https://api.yijiarj.cn/v1/videos`
- `Authorization: Bearer <YIJIA_API_KEY>`
- `Content-Type: application/json`

### Known Body Fields

- `prompt`
- `model`
- `size`
- `input_reference`
- `remix_id`

### Notes

- 文档备注中的首尾帧模型别名已在根目录 [MODELS.md](../../MODELS.md) 收敛到 `veo`
- 多张图片 / 首尾帧场景建议使用 `https://apius.yijiarj.cn`

## Poll

- `GET https://api.yijiarj.cn/v1/videos/{video_id}`
- `Authorization: Bearer <YIJIA_API_KEY>`

### Known Response Fields

- `id`
- `url`
- `size`
- `model`
- `object`
- `status`
- `quality`
- `seconds`
- `progress`
- `created_at`
