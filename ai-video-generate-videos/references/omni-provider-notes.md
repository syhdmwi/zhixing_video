# Omni Provider Notes

当前接入的 omni 信息：

- provider 名：`omni`
- 规范名：`omni`
- API model ID：`omni_flash-v2v`

## Endpoint

- 创建任务：`POST https://api.yijiarj.cn/v1/videos`
- 轮询任务：`GET https://api.yijiarj.cn/v1/videos/{id}`
- 鉴权：`Authorization: Bearer ${YIJIA_API_KEY}`

## Create 参数

只使用以下参数：

- `prompt`：必填，图生视频动作提示词
- `model`：必填，固定使用 `omni_flash-v2v`
- `size`：必填，格式为 `WxH`，例如 `1920x1080`、`720x720`、`1024x1024`
- `input_reference`：可选，输入参考；首尾帧或多图用 `|` 分隔，也可用于视频参考 v2v
- `remix_id`：可选

不传 `duration`。

## Polling

创建任务后按返回的 `id` 轮询：

```text
GET /v1/videos/{id}
```

轮询响应中按 `status` 和 `progress` 判断任务进度。

## 与 grok 的区别

- `grok` 当前走 `POST /v1/chat/completions` 流式接口。
- `omni` 走 `POST /v1/videos` + `GET /v1/videos/{id}` 异步接口。
- `omni` 支持首尾帧、多图参考（用 `|` 分隔）与视频参考 v2v。
