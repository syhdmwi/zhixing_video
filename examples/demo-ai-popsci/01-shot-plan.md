# 01 Shot Plan

SSOT 引用：
- 流程状态机：[../../ai-short-video-pipeline/references/workflow-state-machine.md](../../ai-short-video-pipeline/references/workflow-state-machine.md)
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)，本例使用 `style_key=cyberpunk_bright_hud_infographic`
- 模型清单：[../../MODELS.md](../../MODELS.md)，本例使用 `image_model=GPT-Image-2`、`video_provider=grok`
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)
- 输出格式：[../../ai-short-video-pipeline/references/output-format.md](../../ai-short-video-pipeline/references/output-format.md)

## 项目摘要

- 项目名：demo-ai-popsci
- 目标时长：约 45 秒
- 画幅：16:9
- 总镜头数：7
- 主讲人：`host_cyber_female_01`
- 风格：`cyberpunk_bright_hud_infographic`

## 信息单元表

| unit_id | source_text | claim_type | importance | visual_carrier |
| --- | --- | --- | --- | --- |
| unit_01 | AI 现在不只是会聊天 | hook | 高 | host_primary |
| unit_02 | 它正在变成会干活的同事 | setup | 高 | host_with_visual |
| unit_03 | 过去我们复制资料、写表格、查邮件、手动汇总 | compare | 高 | ui_closeup |
| unit_04 | 智能体可以理解目标、拆步骤、调用工具、检查结果，并交回可检查草稿 | explain | 高 | concept_explainer |
| unit_05 | 遥控器只能按键，实习生会问清楚任务再交付 | compare | 高 | data_compare |
| unit_06 | 给 AI 一个小目标，让它跑完整流程 | cta | 中 | scene_only |

## 镜头表

| shot_id | time_range | unit_id | narration_excerpt | shot_function | visual_carrier | visual_goal |
| --- | --- | --- | --- | --- | --- | --- |
| shot_01 | 00:00-00:05 | unit_01 | 你有没有发现，AI 现在不只是会聊天 | hook | host_primary | 主讲人抛出反常识观点 |
| shot_02 | 00:05-00:11 | unit_02 | 它正在变成一个会干活的同事 | setup | host_with_visual | 主讲人与 AI 同事概念并置 |
| shot_03 | 00:11-00:18 | unit_03 | 过去我们打开十几个软件...手动汇总 | compare | ui_closeup | 展示旧流程的多窗口混乱 |
| shot_04 | 00:18-00:25 | unit_04 | 智能体可以理解目标，自己拆步骤 | explain | concept_explainer | 机制流程图解释智能体 |
| shot_05 | 00:25-00:32 | unit_04 | 调用工具、检查结果，还能把重复动作先跑一遍 | evidence | brand_symbolic | 工具链节点被串联成闭环 |
| shot_06 | 00:32-00:39 | unit_05 | 遥控器只能按键，实习生会问清楚任务再交付 | compare | data_compare | 左右对照“遥控器 vs 实习生” |
| shot_07 | 00:39-00:45 | unit_06 | 别只问它答案，试着给它一个小目标 | cta | scene_only | 以完整流程看板收束 CTA |

## 配比检查

- `scene_only`：1/7，少于完整长片目标，但本 demo 只有 7 镜，保留 1 个纯场景 CTA 镜头。
- 非纯人物解释镜头：`ui_closeup`、`concept_explainer`、`brand_symbolic`、`data_compare` 共 4/7。
- 人物镜头：`host_primary`、`host_with_visual` 共 2/7。
- 结论：短 demo 内节奏平衡，不需要补镜。
