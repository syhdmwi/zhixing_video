---
name: ai-video-voice-clone
description: 当用户想输入文案，并用自己的参考音频去读这段文案时使用这个 skill。它当前适配速创API的同步语音克隆接口，负责克隆声音、落盘真实音频，并在配置 TOS 时默认上传到火山TOS输出可直接给数字人使用的音频直链。
---

# AI Video Voice Clone

## Overview

这个 skill 只负责“参考音频 + 文案 -> 克隆声音音频”阶段，不负责数字人生成，也不负责最终剪辑。

当前接入的是速创API `语音克隆（同步）` 接口：

- `POST https://api.wuyinkeji.com/api/voice/clone`

这个接口需要：

- `audio_url`
- `text`
- 可选 `name`

接口返回：

- `demo_audio`
- `voice_id`

## Inputs

- 参考音频直链
- 或用户上传的本地参考音频文件
- 要朗读的文案
- 可选音频名称

## Core Rules

- 这个 skill 处理的是“用用户参考音频去读文案”
- 它不是平台预设音色 TTS
- 如果用户想要“像我本人一样读这段文案”，优先使用本 skill
- 如果用户只有文案、并不在意是不是自己的声音，优先用 `ai-video-voice-tts`
- 语音克隆接口需要公网可访问的参考音频 URL；如果用户上传本地参考音频且已配置 TOS，先自动上传到 TOS，再提交语音克隆接口
- 只有 TOS 配置缺失时，才提示用户提供公网参考音频 URL
- 返回的 `demo_audio` 默认先保存到本地
- 如果配置了火山 TOS，脚本会自动上传并输出可直接给数字人使用的公网音频直链
- 同步接口没有轮询过程，因此这里不需要异步查询

## Workflow

### 1. Confirm This Is Voice Clone

如果用户明确说：

- 用我的声音读
- 用我自己的声音念文案
- 参考这条音频克隆我的声音

就应进入本 skill，而不是 `ai-video-voice-tts`。

### 2. Build Clone Request

当前接口至少需要：

- `audio_url`
- `text`

可选：

- `name`

### 3. Run The Script

当前脚本层：

- `scripts/wuyinkeji_voice_clone.py`

### 4. Save Real Audio Output

脚本会：

- 调用语音克隆接口
- 读取 `demo_audio`
- 下载真实音频到本地

### 5. Upload To TOS When Configured

如果配置了 TOS，脚本会继续：

- 上传真实音频文件到火山 TOS
- 输出公网可访问的音频直链
- 这个直链可直接交给 `ai-video-avatar-track`

### 6. Hand Off To Avatar Generation

如果后续要进入数字人生成：

- 优先使用脚本输出的 `uploaded_audio_url`
- 再把音频链接交给 `ai-video-avatar-track`

## Output

至少输出：

- `audio_file`
- `metadata_file`
- `voice_id`
- `demo_audio_url`
- `uploaded_audio_url`

## References

- 脚本用法： [references/script-usage.md](./references/script-usage.md)
- 请求模板： [references/voice-clone-request-example.json](./references/voice-clone-request-example.json)
