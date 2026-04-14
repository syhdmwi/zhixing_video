# Suite Architecture

这套方案不是单 skill 直出，而是总控 + 子 skill 协作。

## Production Graph

1. `ai-short-video-pipeline`
   负责总控、拆任务、确定调用顺序。
2. `ai-video-shot-planner`
   输入文案，输出时长估算、镜头数、镜头表、数字人/B-roll 分配。
3. `ai-video-image-prompts`
   输入镜头表、用户参考图和风格要求，输出适配生图模型的提示词。
4. `ai-video-prompt-to-images`
   输入用户已确认的提示词批次，输出并执行生图队列。
5. `ai-video-motion-prompts`
   输入已生成静帧和镜头目标，输出图生视频提示词，并默认先生成测试批次动作方案。
6. `ai-video-generate-videos`
   输入已确认静帧、已确认镜头运动模板和 provider 选择结果，输出并执行真实图生视频任务。
7. `ai-video-avatar-track`
   输入文案和数字人出镜策略，输出数字人视频轨生成说明。
8. `ai-video-edit-assembly`
   输入数字人视频轨和画面视频轨，输出最终剪辑整合方案。

## Separation Rule

必须明确：

- 数字人视频轨单独生成
- 画面视频轨单独生成
- 两者只在剪辑阶段合流

## Recommended Order

推荐顺序：

1. 总控确认任务范围
2. 分镜 skill 产出镜头表
3. 生图提示词 skill 产出静帧提示词
4. 提示词确认后，生图执行 skill 产出静帧
5. 图生视频 skill 先产出测试批次视频动作提示词
6. 用户选择 provider，再由视频执行 skill 提交真实图生视频任务
7. 测试批次通过后，再进入全量图生视频
8. 数字人 skill 产出独立口播视频轨方案
9. 剪辑整合 skill 产出成片方案
