# Models SSOT

本文件是知行视频 skill 的模型与 provider 命名单一事实来源。用户侧只暴露必要选项；实现层别名、API ID 和停用 provider 在这里收敛。

## 生图模型

| 规范名 | 用户可见 | 用途 | 对应脚本 | 别名收敛 |
| --- | --- | --- | --- | --- |
| `GPT-Image-2` | 是 | 当前唯一启用的生图模型，通过一加 Image-2 接口执行 | `ai-video-prompt-to-images/scripts/gpt_image2_batch.py` | API ID `image2`；`Image-2`、`image-2`、`gpt-image-2` |
| `nanobanana-2` | 否 | 停用：速创 NanoBanana2 生图链路不再执行，脚本仅保留供日后恢复 | `ai-video-prompt-to-images/scripts/nanobanana2_batch.py` | `NanoBanana2`、`image_nanoBanana2` |
| `nanobanana-pro` | 否 | 实现层生图能力，保留为高级/兼容选项 | 暂无独立脚本；沿用 nanobanana 提示词规则 | 无 |
| `seedream-5.0` | 否 | 实现层生图能力，火山方舟 Seedream 5 系列 | `ai-video-prompt-to-images/scripts/seedream5_batch.py` | `Seedream-5.0-lite`、`seedream-5.0-lite`、`Seedream 4.6`、`doubao-seedream-5-0-260128` |

当前用户侧生图只使用 `GPT-Image-2`：`POST https://api.yijiarj.cn/v1/chat/completions`，API model 为 `image2`，鉴权为 `Authorization: Bearer ${YIJIA_API_KEY}`。不再使用速创 `image_gpt` 或 `image_nanoBanana2` 接口。

## 图生视频模型

| 规范名 | 用户可见 | 用途 | 对应脚本 | 别名收敛 |
| --- | --- | --- | --- | --- |
| `grok` | 是 | 当前启用的默认图生视频 provider | `ai-video-generate-videos/scripts/video_generation_router.py` | `grok-imagine-1.0-video-super`、Grok |
| `omni` | 是 | 图生视频 provider，支持首尾帧（多图 `|` 分隔）与视频参考（v2v） | `ai-video-generate-videos/scripts/video_generation_router.py` | `omni_flash` |
| `doubao-seedance-1.0-pro-fast` | 否 | 已接入但当前停用的图生视频 provider | `ai-video-generate-videos/scripts/video_generation_router.py` | `seedance`、`doubao-seedance-1-0-pro-fast-251015` |
| `veo` | 否 | 历史/备用 provider 资料，用户侧不再选择；`veo_3_1-fast` / `veo_3_1-fast-fl` / `veo_3_1-fast-4K` 为同 `/v1/videos` endpoint 的实现层变体 | `ai-video-generate-videos/scripts/video_generation_router.py` | `VEO`、`veo_3_1-fast`、`veo_3_1-fast-fl`、`veo_3_1-fast-4K` |

`omni` 接口：`POST https://api.yijiarj.cn/v1/videos` 创建任务，`GET /v1/videos/{id}` 轮询，鉴权 `Authorization: Bearer ${YIJIA_API_KEY}`。

## 数字人 / 语音模型

| 规范名 | 用户可见 | 用途 | 对应脚本 | 别名收敛 |
| --- | --- | --- | --- | --- |
| `即梦 OmniHuman 1.5` | 否 | 停用：数字人生成 provider，当前不对用户开放 | 暂无本地提交脚本 | `OmniHuman 1.5`、`OmniHuman` |
| `蝉镜数字人` | 否 | 停用：数字人生成 provider，当前不对用户开放 | 暂无本地提交脚本 | `蝉镜` |
| `速创 Digital_Humans` | 否 | 停用：速创数字人异步生成接口，脚本保留供日后恢复 | `ai-video-avatar-track/scripts/digital_humans_batch.py` | `Digital_Humans`、`DIGITAL_HUMANS`、`digital_humans` |
| `速创 TTS` | 是 | 速创异步语音合成，用于画面轨配音、字幕或剪映交付包 | `ai-video-voice-tts/scripts/wuyinkeji_audio_tts.py` | `TTS`、`tts`、`语音合成` |
| `速创语音克隆` | 否 | 停用：速创同步语音克隆，当前不对用户开放 | `ai-video-voice-clone/scripts/wuyinkeji_voice_clone.py` | `语音克隆`、`音色克隆`、`用我的声音读` |
