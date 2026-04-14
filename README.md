# AI Short Video Skills Suite

这是一套用于 AI 短视频生产的 Codex skills 打包目录。

## Included Skills

- `ai-short-video-pipeline`
- `ai-video-shot-planner`
- `ai-video-image-prompts`
- `ai-video-prompt-to-images`
- `ai-video-series-archive`
- `ai-video-motion-prompts`
- `ai-video-generate-videos`
- `ai-video-avatar-track`
- `ai-video-edit-assembly`

## What This Suite Covers

- 文案估时与分镜规划
- 角色与重复主体一致性控制
- 生图提示词生成
- 生图批量执行
- 图生视频提示词生成
- `grok` / `seedance` 视频生成
- 数字人生成
- 最终剪辑整合规划

## Required Environment Variables

按需配置，不是每个 skill 都必须全配：

- `NANOBANANA_API_KEY`
- `YIJIA_API_KEY`
- `ARK_API_KEY`
- `SEEDANCE_API_KEY`
- `DIGITAL_HUMANS_API_KEY`
- `WUYINKEJI_API_KEY`

## Notes

- 本分享包不包含任何真实 API key
- 本分享包不包含本地测试结果和临时文件
- 数字人生成阶段要求：
  - 音频必须是公网可访问直链
  - 人物视频必须是公网可访问直链
  - 人物视频需为正面素材，且时长不低于 10 秒

## Suggested Install Method

把这 9 个 skill 目录复制到对方的 Codex skills 目录下即可使用。

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
- `ai-video-avatar-track`
- `ai-video-edit-assembly`

### 4. 配置环境变量

按实际要用的能力配置，不是每个人都要全配。

示例：

```bash
export NANOBANANA_API_KEY="your_nanobanana_key"
export YIJIA_API_KEY="your_grok_or_yijia_key"
export ARK_API_KEY="your_seedance_key"
export DIGITAL_HUMANS_API_KEY="your_digital_humans_key"
```

如果只测某一段流程，只配那一段需要的 key 即可。

### 5. 重启或刷新 Codex

让 Codex 重新读取 skills 目录。

## How To Run Tests

建议不要一上来跑全流程，先按下面顺序做小测试。

### 测试 1：图片提示词生成

目标：

- 验证文案能否正常拆成图片提示词

操作：

- 给一段短文案
- 指定张数、比例、语言、风格
- 让 Codex 使用 `ai-video-image-prompts`

示例提问：

```text
用这段文案，先帮我生成 10 条图片提示词，16:9，中文，卡通风。
```

### 测试 2：提示词转生图

目标：

- 验证 `nanobanana` 生图链路

前提：

- 已配置 `NANOBANANA_API_KEY`

操作：

- 先确认提示词
- 再只跑前 `1~3` 张或 `1~5` 张测试批次

示例提问：

```text
这 5 条提示词可以，先生成前 5 张图给我看。
```

### 测试 3：图生视频

目标：

- 验证 `grok` 或 `seedance` 视频生成链路

前提：

- 已配置 `YIJIA_API_KEY` 或 `ARK_API_KEY`

操作：

- 先只选 1 张图测试
- 确认视频提示词
- 再生成视频

示例提问：

```text
用 grok 先拿第 1 张图测试视频。
```

### 测试 4：数字人生成

目标：

- 验证数字人链路

前提：

- 已配置 `DIGITAL_HUMANS_API_KEY`
- 必须提供两个公网直链：
  - 音频直链
  - 正面人物视频直链

注意：

- 不能给分享页
- 必须是能直接访问文件的直链
- 人物视频时长需不低于 10 秒

示例提问：

```text
现在测试数字人，这是音频直链，这是人物视频直链，帮我提交并查询结果。
```

## Recommended First Full Demo

如果对方想快速体验整套能力，建议用这个顺序：

1. 用 `ai-short-video-pipeline` 或 `ai-video-image-prompts` 从短文案生成 `5~10` 条提示词
2. 只生成前 `3~5` 张图片
3. 只拿第 `1` 张图片测试图生视频
4. 单独测试 1 条数字人
5. 确认每段都通了，再跑全量

## Troubleshooting

### 生图没反应或一直 pending

- 先查 API key 是否正确
- 再缩小测试批次
- 默认先跑 `1~5` 张，不要一开始就全量

### 图生视频人物总在乱动

- `grok` 先优先套用 `grok视频模版套用00`
- 如果还是不稳定，先改用 `seedance` 对比

### 数字人报“获取时长失败”

- 通常是素材链接不是直链
- 检查链接返回的是否真的是 `audio/*` 或 `video/*`
- 不要用分享页代替文件直链
