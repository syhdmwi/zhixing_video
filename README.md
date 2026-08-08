# AI Short Video Workflow Suite

这是一套面向 AI 编程工具和智能体工具的短视频工作流包，适合把一段文案一路做成：

- 图片
- 视频
- 配音
- 剪映手动交付包
- 可复用模板

它对外是一个主 skill：`zhixing_video`。也可以迁移到 OpenClaw、Trae、Claude Code 等支持项目规则、上下文文档或自定义工作流的工具里使用。

如果你是第一次用，不用先理解所有目录名字。你只需要知道自己现在想做哪件事。

## 新手先看这里

你可以直接这样开口：

- `这是我的文案，先带我走图片流程。`
- `这些图片已经确认，帮我进入视频生成。`
- `这是文案，帮我从图片一路做到视频。`

如果你不知道该从哪里开始，最稳的第一句话是：

```text
这是我的文案，帮我从头开始做。
```

也可以使用统一唤醒词：

```text
使用知行视频skill，帮我从文案开始做视频。
```

如果流程中断、换工具后接不上，或你不知道下一步该做什么，可以说：

```text
使用知行视频skill，帮我恢复当前流程状态。
```

如果你是第一次把这套 skills 分享给别人，建议让对方先看这份：

- [SOP：如何使用知行视频skill](./SOP-如何使用知行视频skill.md)
- [用户使用说明](./用户使用说明.md)
- [3分钟快速开始](./3分钟快速开始.md)
- [跨工具使用说明](./跨工具使用说明.md)

## 看一个完整样例

想先看“文案 -> 分镜 -> 风格 -> 主体 -> 图片提示词 -> 图生视频提示词 -> 交付包”的静态跑通结果，可以直接看：

- [examples/demo-ai-popsci/](./examples/demo-ai-popsci/)

## 你会经历的流程

正常情况下，系统会按下面的顺序带你走：

1. 收文案
2. 选风格和比例，自动使用 `GPT-Image-2`
3. 自动识别重复主体
4. 确认主体参考图或三视图
5. 先给你看正式提示词
6. 再批量生图
7. 生成完成后先让你确认要不要改图
8. 确认无误后再进入视频生成
9. 满意后可保存为模板，下次新文案直接套用

你不需要自己处理：

- 公网链接
- 对象存储
- TOS
- 队列文件
- API 提交格式

如果模型接口需要公网图片、音频、视频链接，而你上传的是本地文件，系统会优先自动转存后再提交。

## 三个常用入口

### 1. 我只想做图片

直接说：

```text
这是我的文案，先带我走图片流程。
```

### 2. 我已经有图片，想继续做视频

直接说：

```text
这些图片已经确认，帮我进入视频生成。
```

### 3. 我想跑完整流程

直接说：

```text
这是文案，帮我从图片一路做到视频。
```

## 你需要准备什么

最少只需要准备其中一种：

- 一段文案
- 一批图片
- 一段音频

如果你有这些材料，效果会更稳：

- 主讲人参考图
- 主讲人三视图
- 主要角色参考图
- 风格参考图

如果没有，也可以先开始，系统会默认补齐基础流程。

## 当前支持的主要能力

- 文案估时与镜头数规划
- 流程状态机，防止中途调用时走错顺序
- 重复主体识别与三视图确认
- 按模型切换不同图片提示词模板
- 批量生图执行
- 图生视频
- 图转镜头移动视频
- 文案转音频
- 剪映手动交付包
- 主讲人、风格和提示词规则保存为模板
- 新文案套用已有模板
- 最终剪辑整合规划

## 当前流程特点

- 风格、比例会先确认；生图模型固定为 `GPT-Image-2`
- 正式生图统一通过一加 Image-2 接口执行，API model 为 `image2`
- `nanobanana-2` 已停用，不再作为用户选项或执行链路
- 图片提示词统一使用 `GPT-Image-2` 模板
- 自主设定风格时：
  - 如果用户给风格参考图，会先分析画风再生成
  - 如果用户说“只参考风格，不参考人物”，就不会继承图里人物设定
- 如果用户提供人物三视图，会直接用作主讲人物锚点，不再重生主讲人物
- 图片生成完成后默认有两个视频分支：
  - `图转镜头移动视频模式`
  - `图生视频模式`
- 视频阶段默认只交付单镜头视频，不自动拼总片
- 视频生成完成后会询问是否导出剪映手动交付包
- 模板默认保存主讲人、风格和提示词规则；重复主体默认随新文案重新识别
- 正式图样例只有用户选择编号后才保存进模板
- 数字人和语音克隆当前暂未开放；TTS 文案转音频保留可用

## Internal Workflow Modules

这些目录现在是内部模块，不是给用户单独选择的外部 skill：

- `ai-short-video-pipeline`
- `ai-video-shot-planner`
- `ai-video-image-prompts`
- `ai-video-prompt-to-images`
- `ai-video-series-archive`
- `ai-video-motion-prompts`
- `ai-video-generate-videos`
- `ai-video-keyframe-edit`
- `ai-video-voice-tts`
- `ai-video-voice-clone`（停用，保留实现）
- `ai-video-avatar-track`（停用，保留实现）
- `ai-video-edit-assembly`

## 高级配置

如果你只是想先体验流程，可以先跳过这一段。

## Required Environment Variables

按需配置，不是每个 skill 都必须全配：

- `YIJIA_API_KEY`
- `WUYINKEJI_API_KEY`
- `AUDIO_TTS_API_KEY`
- `TOS_ACCESS_KEY_ID`
- `TOS_SECRET_ACCESS_KEY`
- `TOS_BUCKET`
- `TOS_REGION`

## Notes

- 本分享包不包含任何真实 API key
- 本分享包不包含本地测试结果和临时文件
- 数字人和语音克隆当前暂未开放，相关实现文件保留但不作为用户入口。
- TTS 保留可用，生成音频可用于画面轨配音、字幕或剪映交付包。

## Suggested Install Method

如果使用 Codex，优先把整个项目目录作为一个主 skill 包来使用，对外入口是根目录下的 [SKILL.md](./SKILL.md)。

如果使用 OpenClaw、Trae、Claude Code 或其它 AI 编程工具，请优先查看：

- [跨工具使用说明](./跨工具使用说明.md)

这些工具如果不能直接识别 Codex skill 目录，也可以把根入口 [SKILL.md](./SKILL.md) 和核心说明文档作为项目规则、工作流文档或上下文导入。

内部模块继续保留给实现层引用，不要求用户单独安装或理解。

## Install Steps

### 1. 解压压缩包

把 `ai-short-video-skills-suite.zip` 解压到本地任意目录。

### 2. 选择安装方式

Codex：

把模块目录复制到：

- `$CODEX_HOME/skills/`

OpenClaw / Trae / Claude Code：

- 把本项目作为普通项目文件夹打开
- 把 [用户使用说明](./用户使用说明.md) 和 [跨工具使用说明](./跨工具使用说明.md) 放进工具的项目上下文
- 如果工具支持自定义规则文件，把根入口 [SKILL.md](./SKILL.md) 作为总控规则导入

如果使用 Codex 但不确定 `CODEX_HOME`，可以先在终端里执行：

```bash
echo $CODEX_HOME
```

### 3. 复制 skill 目录

把下面这些目录复制进去：

- `ai-short-video-pipeline`
- `ai-video-shot-planner`
- `ai-video-image-prompts`
- `ai-video-prompt-to-images`
- `ai-video-series-archive`
- `ai-video-motion-prompts`
- `ai-video-generate-videos`
- `ai-video-keyframe-edit`
- `ai-video-voice-tts`
- `ai-video-voice-clone`（停用，保留实现）
- `ai-video-avatar-track`（停用，保留实现）
- `ai-video-edit-assembly`

### 4. 配置环境变量

按实际要用的能力配置，不是每个人都要全配。

示例：

```bash
export YIJIA_API_KEY="your_yijia_key"
export AUDIO_TTS_API_KEY="your_tts_key"
export TOS_ACCESS_KEY_ID="your_tos_ak"
export TOS_SECRET_ACCESS_KEY="your_tos_sk"
export TOS_BUCKET="your_bucket"
export TOS_REGION="cn-beijing"
```

如果只测某一段流程，只配那一段需要的 key 即可。

### 5. 重启或刷新工具

让当前使用的 AI 工具重新读取 skills、项目规则或上下文文档。

## How To Run Tests

建议不要一上来跑全流程，先按下面顺序做小测试。

### 测试 1：图片提示词生成

目标：

- 验证文案能否正常拆成图片提示词
- 验证风格、比例选择与默认 `GPT-Image-2` 是否正常贯通

示例提问：

```text
这是一段文案，先带我走一遍图片提示词流程。
```

### 测试 2：三视图与主体一致性

目标：

- 验证重复主体识别
- 验证主讲人物三视图和关键主体三视图流程

建议：

- 主讲人物如果已有三视图，直接上传
- 其它高频角色让系统单独生成三视图

### 测试 3：批量生图

目标：

- 验证一加 `GPT-Image-2` 生图链路

建议：

- 先跑一小批
- 图片生成完成后，整批查看

示例提问：

```text
这批提示词可以，全部生图。
```

### 测试 4：视频阶段

目标：

- 验证图片转视频的两个分支

分支：

- `图转镜头移动视频模式`
- `图生视频模式`

注意：

- 默认只交付单镜头视频
- 不会自动拼接成总片，除非你明确要求

### 测试 5：TTS 与剪映交付包

目标：

- 验证 `TTS`
- 验证剪映手动交付包三件套

前提：

- 如需真实 TTS，已配置对应 API key
- 视频镜头已有 `shot_id`、时间线和口播文本

## Recommended First Full Demo

如果对方想快速体验整套能力，建议用这个顺序：

1. 用 `ai-short-video-pipeline` 从短文案开始走完整图片流程
2. 只生成一批小规模图片
3. 进入 `图转镜头移动视频模式` 或 `图生视频模式`
4. 再单独测试 `TTS / 剪映手动交付包`
5. 每一段都确认没问题后，再跑更长文案

## Troubleshooting

### 生图请求失败或没有返回图片

- 确认已配置 `YIJIA_API_KEY`
- 确认请求模型为规范名 `GPT-Image-2`，执行层 API model 为 `image2`
- 确认参考图是接口可访问的公网 URL

### 图转镜头移动视频不够稳

- 当前默认参数已经是稳定版：
  - `8秒`
  - `50fps`
  - 相邻镜头方向不同
- 若还需调整，优先调单镜头，不建议一次改整批

### 剪映交付包导入后时间线不一致

- 先检查 `timeline.csv` 的 `shot_id`、起止时间和素材文件名是否与实际文件一致
- 再检查剪映导入后是否按 `order` 从小到大排轨
- 字幕错位时优先检查 `subtitles.srt` 时间码

### TTS 结果如何用于交付包

- TTS 音频可作为配音素材导入剪映
- 如果需要在外部工具引用，可配置 TOS 上传参数输出公网直链
