# AI Video Voice TTS（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户只有文案、还没有成品音频，但想先把文案转成可用于数字人的音频时使用，当前适配速创API异步语音合成接口。

## 关键 references

- [references/script-usage.md](./references/script-usage.md) — 脚本使用说明
- [references/tts-request-example.json](./references/tts-request-example.json) — TTS 请求示例

## 上下游

上游：`ai-short-video-pipeline` 或用户文案 / 下游：`ai-video-avatar-track`、`ai-video-edit-assembly`。
