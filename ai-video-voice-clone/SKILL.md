---
name: ai-video-voice-clone
description: 语音克隆实现模块当前停用，不对用户开放、不执行；实现保留供日后恢复。
---

> ⛔ 语音克隆功能当前停用，不对用户开放、不执行；实现保留供日后恢复。

# AI Video Voice Clone

## Overview

这个 skill 当前停用。以下接口、脚本和请求说明仅作为实现留档，不作为用户可用入口；任何“用我的声音读 / 语音克隆 / 音色克隆”请求都应由总控回复“该功能当前暂未开放”。

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

- 这个 skill 当前不处理用户请求
- 它不是平台预设音色 TTS
- 如果用户想要“像我本人一样读这段文案”，固定回复：`该功能当前暂未开放。`
- 如果用户只有文案、并不在意是不是自己的声音，优先用 `ai-video-voice-tts`
- 语音克隆接口实现资料保留，但当前不提示用户提供参考音频 URL
- 不为当前用户请求提交语音克隆接口
- 返回字段和上传逻辑仅作为恢复时的实现参考
- 同步接口没有轮询过程，因此这里不需要异步查询

## Workflow

### 1. Confirm This Is Voice Clone

如果用户明确说：

- 用我的声音读
- 用我自己的声音念文案
- 参考这条音频克隆我的声音

不要进入本 skill，固定回复：`该功能当前暂未开放。` 如果用户改为使用平台预设音色朗读，可转入 `ai-video-voice-tts`。

### 2. Build Clone Request

当前接口至少需要：

- `audio_url`
- `text`

可选：

- `name`

### 3. Run The Script

脚本保留但当前不执行：

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
- 当前不把该直链交给任何活跃用户流程

### 6. Hand Off

当前不再衔接数字人生成；如日后恢复，应重新确认总控状态机和模型可见性。


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
