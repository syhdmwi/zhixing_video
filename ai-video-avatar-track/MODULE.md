# AI Video Avatar Track（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户要单独制作数字人生成结果时使用，适用于即梦 OmniHuman 1.5、蝉镜数字人和速创 Digital_Humans，并负责素材校验、真实提交、轮询查询和结果展示。

## 关键 references

- [references/avatar-queue-example.json](./references/avatar-queue-example.json) — 数字人任务队列示例
- [references/script-usage.md](./references/script-usage.md) — 脚本使用说明

## 上下游

上游：`ai-short-video-pipeline`、`ai-video-voice-tts`、`ai-video-voice-clone` / 下游：`ai-video-edit-assembly`。
