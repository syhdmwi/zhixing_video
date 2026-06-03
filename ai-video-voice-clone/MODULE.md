# AI Video Voice Clone（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户想输入文案并用自己的参考音频去读这段文案时使用，当前适配速创API同步语音克隆接口并输出可用于数字人的音频。

## 关键 references

- [references/script-usage.md](./references/script-usage.md) — 脚本使用说明
- [references/voice-clone-request-example.json](./references/voice-clone-request-example.json) — 语音克隆请求示例

## 上下游

上游：`ai-short-video-pipeline` 或用户参考音频 / 下游：`ai-video-avatar-track`、`ai-video-edit-assembly`。
