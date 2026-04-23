---
name: ai-video-voice-tts
description: 当用户只有文案、还没有成品音频，但想先把文案转成可用于数字人的音频时使用这个 skill。它当前适配速创API的异步语音合成接口，负责文本转音频、任务查询、真实音频文件落盘、可选上传到火山TOS并输出数字人可用直链。注意：当前接入的是 TTS，不是音色克隆。
---

# AI Video Voice TTS

## Overview

这个 skill 只负责“文案转音频”阶段，不负责数字人生成，也不负责最终剪辑。

当前接入的是速创API `语音合成` 异步接口：

- `POST https://api.wuyinkeji.com/api/async/audio_tts`
- `GET https://api.wuyinkeji.com/api/async/detail`

注意：

- 你刚给的官方文档是 `语音合成`
- 不是“音色快速复刻”接口
- 所以当前这个 skill 是 `文案转音频`
- 如果后面要做“声音克隆”，还需要接入速创文档里单独的 `语音克隆（同步）` 接口

## Inputs

- 文案文本
- `voice_id`
- 语速
- 音量
- `language_boost`

## Current Default

如果用户没特别指定，默认：

- `voice_id`: `male-qn-qingse`
- `speed`: `1`
- `vol`: `1`
- `language_boost`: `auto`

## Core Rules

- 当前 skill 只处理 TTS，不把它叫成“音色克隆”
- 如果用户只有文案，没有成品音频，可以先用本 skill 生成音频
- 生成结果默认先保存到本地文件
- 如果配置了火山 TOS，就通过火山官方 Python SDK 自动把真实音频上传到 TOS，并输出可直接给数字人使用的公网直链
- 如果用户已经有成品音频，就不要强行走本 skill
- 所有轮询中的进度汇报，默认遵循总控里的统一规则：[references/polling-progress-rules.md](../ai-short-video-pipeline/references/polling-progress-rules.md)

## Workflow

### 1. Confirm This Is TTS

如果用户提供的是速创 `语音合成` 文档，应按 TTS 处理，不要误判成声音克隆。

### 2. Build TTS Request

当前接口至少需要：

- `text`
- `voice_id`

可选参数：

- `speed`
- `vol`
- `language_boost`

### 3. Run The Script

当前脚本层：

- `scripts/wuyinkeji_audio_tts.py`

### 4. Save Real Audio Output

脚本会先提交异步任务，再轮询查询结果。任务成功后会把远程结果下载到本地。

注意：

- 速创当前返回的下载结果可能是 `tar` 包
- 脚本会自动解包，拿到真正的 `.mp3/.wav` 音频文件
- 不会再把 `tar` 包误当成音频直接交给数字人

### 5. Optional Upload To TOS

如果配置了 TOS，脚本会继续：

- 上传真实音频文件到火山 TOS
- 输出公网可访问的音频直链
- 这个直链可直接交给 `ai-video-avatar-track`

### 6. Hand Off To Avatar Generation

如果后续要进入数字人生成：

- 先确认音频效果
- 优先使用脚本输出的 `uploaded_audio_url`
- 再把音频链接交给 `ai-video-avatar-track`

## Output

至少输出：

- `audio_file`
- `metadata_file`
- `voice_id`
- `audio_url`
- `uploaded_audio_url`
- `task_id`

## References

- 脚本用法： [references/script-usage.md](./references/script-usage.md)
- 请求模板： [references/tts-request-example.json](./references/tts-request-example.json)
