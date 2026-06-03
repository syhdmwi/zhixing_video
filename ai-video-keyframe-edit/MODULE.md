# AI Video Keyframe Edit（模块索引）

> 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。

## 角色

当用户已经生成完静帧图片，并希望通过剪辑方式给图片添加轻微关键帧运镜生成画面轨视频时使用，默认优先使用 FFmpeg。

## 关键 references

- [references/keyframe-queue-example.json](./references/keyframe-queue-example.json) — 关键帧队列示例
- [references/script-usage.md](./references/script-usage.md) — 脚本使用说明

## 上下游

上游：`ai-video-prompt-to-images` / 下游：`ai-video-edit-assembly`。
