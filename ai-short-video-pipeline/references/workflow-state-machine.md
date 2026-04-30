# Workflow State Machine

这份文件用于防止 Trae、OpenClaw、Claude Code 等工具在中途调用某个环节时走错流程。

核心原则：

- 任何环节开始前，先判断当前阶段。
- 缺少前置条件时，不继续执行当前环节。
- 每次回复用户时，都要告诉用户当前阶段和下一步。
- 用户只输入 `1` 或 `2` 时，必须根据当前阶段解释含义，不能跨阶段误判。

## Stage List

标准主流程阶段如下：

1. `start`
2. `script_received`
3. `style_selected`
4. `subjects_identified`
5. `subjects_confirmed`
6. `three_views_generated`
7. `three_views_confirmed`
8. `prompts_generated`
9. `prompts_confirmed`
10. `images_generated`
11. `images_approved`
12. `template_save_decision`
13. `video_mode_selected`
14. `videos_generated`
15. `digital_human_assets_ready`
16. `digital_human_generated`
17. `completed`

## Allowed Transitions

```text
start -> script_received
script_received -> style_selected
style_selected -> subjects_identified
subjects_identified -> subjects_confirmed
subjects_confirmed -> three_views_generated
three_views_generated -> three_views_confirmed
three_views_confirmed -> prompts_generated
prompts_generated -> prompts_confirmed
prompts_confirmed -> images_generated
images_generated -> images_approved
images_approved -> template_save_decision
images_approved -> video_mode_selected
template_save_decision -> video_mode_selected
video_mode_selected -> videos_generated
videos_generated -> completed

start -> digital_human_assets_ready
digital_human_assets_ready -> digital_human_generated
digital_human_generated -> completed
```

## Required Gates

### Before Style Selection

Required:

- 文案已收到，或用户明确从已有图片/数字人素材开始

If missing:

```text
现在还不能选择风格。
缺少：文案。
请先发送文案，或说明你要从已有图片/数字人素材开始。
```

### Before Subject Confirmation

Required:

- 文案已收到
- 风格/比例/生图模型已确认
- 重复主体清单已生成

If missing:

```text
现在还不能确认主体。
缺少：风格、比例或生图模型。
请先完成风格和模型选择。
```

### Before Three-View Generation

Required:

- 主体清单已展示
- 用户已确认主体清单

If missing:

```text
现在还不能生成三视图。
缺少：主体清单确认。
请先确认主体清单，或说明需要修改哪些主体。
```

### Before Prompt Generation

Required:

- 主体参考图或三视图已确认

If missing:

```text
现在还不能生成正式图片提示词。
缺少：主体参考图或三视图确认。
请先确认主体是否满意。
```

### Before Image Generation

Required:

- 正式图片提示词已展示
- 用户已确认可以生图

If missing:

```text
现在还不能批量生图。
缺少：正式图片提示词确认。
请先确认提示词，或指出需要修改第几张提示词。
```

### Before Video Generation

Required:

- 图片已生成
- 图片已全部展示
- 用户已确认图片满意

If missing:

```text
现在还不能进入视频生成。
缺少：已确认满意的图片。
请先完成图片生成并确认是否需要修改。
```

### Before Digital Human Generation

Required:

- 音频
- 正面人物视频

If missing:

```text
现在还不能制作数字人。
缺少：音频或正面人物视频。
请上传音频和正面人物视频。
```

### Before Template Save

Required:

- 主讲人锚点已确认
- 风格已确认
- 提示词规则已确认
- 至少一批正式图片已生成并被用户认可

If missing:

```text
现在还不能保存模板。
缺少：已确认的主讲人、风格、提示词规则或满意图片。
请先完成图片流程并确认满意。
```

## Stage Response Format

每次进入或恢复流程时，优先使用：

```text
当前流程状态：
阶段：[current_stage]
已完成：[completed_items]
下一步：[next_action]
你可以回复：[allowed_user_replies]
```

示例：

```text
当前流程状态：
阶段：图片确认
已完成：文案、风格、主体、三视图、提示词、生图
下一步：确认图片是否满意
你可以回复：第几张 + 修改要求；或者输入 2 进入视频生成
```

## Ambiguous Reply Rule

用户只输入 `1` 或 `2` 时，必须按当前阶段解释。

Examples:

- 在风格阶段，`1` = 使用风格模板
- 在主体清单阶段，`1` = 进入三视图生成
- 在三视图确认阶段，`2` = 主体无需修改
- 在图片确认阶段，`2` = 进入视频生成
- 在视频阶段，`2` = 图生视频模式
- 在模板保存样例图阶段，`2` = 不保存样例图

如果当前阶段不明确，不要猜，先恢复状态：

```text
我需要先确认当前流程阶段，避免把 1/2 理解错。
请告诉我你现在是在确认主体、确认图片，还是选择视频模式？
```

## Jump-In Recovery Rule

如果用户从任意环节直接发起请求，例如：

- `直接生成视频`
- `全部生图`
- `保存模板`
- `做数字人`

先检查状态。

如果前置条件满足，继续执行。

如果前置条件不满足，提示缺少什么，并把用户带回正确步骤。
