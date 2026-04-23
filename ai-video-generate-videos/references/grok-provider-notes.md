# Grok Provider Notes

当前已接入的 grok 信息：

- provider 名：`grok`
- 当前沿用一加 API：
  - 创建并等待结果：`POST https://api.yijiarj.cn/v1/chat/completions`
  - 返回类型：`text/event-stream`
  - 鉴权：`Authorization: Bearer <YIJIA_API_KEY>`

当前脚本按图生视频场景构造如下请求：

- `model`
  - 当前默认可用模型示例：`grok-imagine-1.0-video-super`
- `messages`
  - `role: user`
  - `content`
    - 文本项：`{"type":"text","text":"<motion_prompt>"}`
    - 图片项：`{"type":"image_url","image_url":{"url":"<source_image_url>"}}`
- `video_config`
  - `video_length`
  - `aspect_ratio`
  - `preset`
  - `resolution_name`

Grok 默认提示词建议：

- 优先使用英文动作提示词，不要只用中文
- 对“人物不要乱动”要写成强约束，而不是只写“不变形”
- 推荐结构：
  - `Slow camera pan left. The subject remains perfectly still. Do not animate walking, body movement, hand movement, or pose change. Keep the character design, face, clothes, and background consistent. Only move the camera.`
- 如果用户要更详细的测试版提示词，可以明确写：
  - `The character remains completely fixed like a still illustration. Lock body position, hand position, head angle, facial expression, and the relative position between the girl and the lobster. No walking, no stepping, no swaying, no hand motion, no blinking, no mouth motion, no pose change. The camera slowly moves upward while gradually pulling away from the subject. Only the camera moves. Do not animate the character. Keep the face, hair, dress, lobster anatomy, and background fully consistent.`

当前已保存固定模板：

- `grok视频模版套用00`
- 模板文件： [grok-video-template-00.md](./grok-video-template-00.md)

默认使用规则：

- 当自动路由或用户明确指定最终使用 `grok` 时，默认直接套用 `grok视频模版套用00`
- 不再默认额外询问用户是否套用该模板
- 优先在该模板基础上替换主体、场景和镜头内容

重要规则：

- 模板里的主体必须是“当前文案和当前镜头里的高频主体”
- 不要因为某个案例里用了龙虾，就把龙虾写死成所有视频提示词里的固定角色
- 如果当前案例的高频主体是兔子、鸡、向日葵、产品、吉祥物或别的关键物，就应动态替换
- 如果当前镜头里没有第二主体，就不要硬塞第二主体描述

当前返回解析规则：

- 该接口不是独立“提交任务 -> 轮询任务”的异步任务接口
- 当前脚本会直接消费 SSE 流
- 会从流式 `delta.content` 中提取：
  - 进度文本，例如 `正在生成视频中，当前进度XX%`
  - 最终 mp4 链接
- 一旦提取到最终 mp4 链接，就视为本次执行成功

注意：

- 这条链路已经替代旧的 `veo` 路由
- 用户侧后续不再需要选择 `veo`
- 如需双图或多图输入，可在 `source_image_url` 中使用 `|` 分隔多个图片 URL，脚本会自动展开成多个 `image_url` 项
- `source_image_url` 必须是公网可访问 URL。如果用户提供本地图片文件，且已配置 TOS，先用总控上传脚本转存到 TOS，再把公网直链写入 `source_image_url`
- 不要把本地路径直接传给 grok
- 如果中文提示词容易触发“人物自己走动”，优先切换为英文强约束提示词
