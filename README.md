# AI Short Video Skills Suite

这是一套用于 AI 短视频生产的 Codex skills 打包目录，覆盖从文案、主体三视图、生图、视频，到语音克隆、数字人的完整工作流。

## Included Skills

- `ai-short-video-pipeline`
- `ai-video-shot-planner`
- `ai-video-image-prompts`
- `ai-video-prompt-to-images`
- `ai-video-series-archive`
- `ai-video-motion-prompts`
- `ai-video-generate-videos`
- `ai-video-keyframe-edit`
- `ai-video-voice-tts`
- `ai-video-voice-clone`
- `ai-video-avatar-track`
- `ai-video-edit-assembly`

## What This Suite Covers

- 文案估时与镜头数规划
- 重复主体识别与三视图确认
- 按模型切换不同图片提示词模板
- 批量生图执行
- 图生视频
- 图转镜头移动视频
- 文案转音频
- 语音克隆
- 数字人生成
- 最终剪辑整合规划

## Current Workflow Highlights

- 风格、比例、生图模型在同一轮一起选择
- 生图模型支持：
  - `GPT-Image-2`
  - `nanobanana-2`
- 图片提示词会按模型自动切换不同模板：
  - `GPT-Image-2` 更自然、叙事化
  - `nanobanana-2` 更结构化、模块化
- 自主设定风格时：
  - 如果用户给风格参考图，会先分析画风再生成
  - 如果用户说“只参考风格，不参考人物”，就不会继承图里人物设定
- 如果用户提供人物三视图，会直接用作主讲人物锚点，不再重生主讲人物
- 图片生成完成后默认有两个视频分支：
  - `图转镜头移动视频模式`
  - `图生视频模式`
- 视频阶段默认只交付单镜头视频，不自动拼总片

## Required Environment Variables

按需配置，不是每个 skill 都必须全配：

- `GPT_IMAGE2_API_KEY`
- `NANOBANANA_API_KEY`
- `YIJIA_API_KEY`
- `DIGITAL_HUMANS_API_KEY`
- `WUYINKEJI_API_KEY`
- `AUDIO_TTS_API_KEY`
- `VOICE_CLONE_API_KEY`
- `TOS_ACCESS_KEY_ID`
- `TOS_SECRET_ACCESS_KEY`
- `TOS_BUCKET`
- `TOS_REGION`

## Notes

- 本分享包不包含任何真实 API key
- 本分享包不包含本地测试结果和临时文件
- 数字人生成阶段要求：
  - 音频必须是公网可访问直链
  - 人物视频必须是公网可访问直链
  - 人物视频需为正面素材，且时长不低于 10 秒
- 语音克隆和 TTS 如需直接衔接数字人，建议同时配置 TOS 上传参数

## Suggested Install Method

把这 12 个 skill 目录复制到对方的 Codex skills 目录下即可使用。

如果对方只想用部分流程，也可以只安装其中的单个 skill。

## Install Steps

### 1. 解压压缩包

把 `ai-short-video-skills-suite.zip` 解压到本地任意目录。

### 2. 找到 Codex 的 skills 目录

通常复制到：

- `$CODEX_HOME/skills/`

如果对方不确定 `CODEX_HOME`，也可以先在终端里执行：

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
- `ai-video-voice-clone`
- `ai-video-avatar-track`
- `ai-video-edit-assembly`

### 4. 配置环境变量

按实际要用的能力配置，不是每个人都要全配。

示例：

```bash
export GPT_IMAGE2_API_KEY="your_gpt_image2_key"
export NANOBANANA_API_KEY="your_nanobanana_key"
export YIJIA_API_KEY="your_grok_or_yijia_key"
export AUDIO_TTS_API_KEY="your_tts_key"
export VOICE_CLONE_API_KEY="your_voice_clone_key"
export DIGITAL_HUMANS_API_KEY="your_digital_humans_key"
export TOS_ACCESS_KEY_ID="your_tos_ak"
export TOS_SECRET_ACCESS_KEY="your_tos_sk"
export TOS_BUCKET="your_bucket"
export TOS_REGION="cn-beijing"
```

如果只测某一段流程，只配那一段需要的 key 即可。

### 5. 重启或刷新 Codex

让 Codex 重新读取 skills 目录。

## How To Run Tests

建议不要一上来跑全流程，先按下面顺序做小测试。

### 测试 1：图片提示词生成

目标：

- 验证文案能否正常拆成图片提示词
- 验证风格、比例、生图模型三合一选择是否正常

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

- 验证 `GPT-Image-2` 或 `nanobanana-2` 生图链路

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

### 测试 5：语音与数字人

目标：

- 验证 `TTS`
- 验证 `语音克隆`
- 验证 `数字人`

前提：

- 已配置对应 API key
- 数字人需要音频直链和正面人物视频直链

## Recommended First Full Demo

如果对方想快速体验整套能力，建议用这个顺序：

1. 用 `ai-short-video-pipeline` 从短文案开始走完整图片流程
2. 只生成一批小规模图片
3. 进入 `图转镜头移动视频模式` 或 `图生视频模式`
4. 再单独测试 `TTS / 语音克隆 / 数字人`
5. 每一段都确认没问题后，再跑更长文案

## Troubleshooting

### 生图一直 pending 或超时

- 先确认选择的是哪一个生图模型
- 对人物强参考镜头，优先尝试 `GPT-Image-2`
- 对更结构化的场景镜头，可尝试 `nanobanana-2`

### 图转镜头移动视频不够稳

- 当前默认参数已经是稳定版：
  - `8秒`
  - `50fps`
  - 相邻镜头方向不同
- 若还需调整，优先调单镜头，不建议一次改整批

### 数字人报“获取时长失败”

- 通常是素材链接不是直链
- 检查链接返回的是否真的是 `audio/*` 或 `video/*`
- 不要用分享页代替文件直链

### 语音克隆或 TTS 结果不能直接喂数字人

- 需要先把音频转成可访问的公网直链
- 推荐配置 TOS 上传参数，让流程自动完成这一步
