# Batch Execution Checklist

这个清单用于在“提示词已确认”之后进入正式生图。

## Before Running

先确认：

- 提示词已经通过用户确认
- 模型已经确定
- 比例已经确定
- 输出张数已经确定
- 人物参考图是否存在

## Queue Requirements

执行队列至少应包含：

- `shot_id`
- `frame_type`
- `model`
- `aspect_ratio`
- `image_prompt`
- `reference_image_required`
- `consistency_note`

## Quality Checks

执行前后都要检查：

- 张数是否完整
- 顺序是否连续
- 纯场景画面是否至少三分之一
- 人物镜头是否沿用同一角色设定
- 重复出现的动物、吉祥物、产品、关键物件是否沿用同一主体设定
- 画风是否统一
- 是否有明显跑偏的个别镜头需要回炉

## Escalation Rule

只有当用户明确要求或执行结果暴露出一致性问题时，才回到上游重新改提示词或重做角色设定。

如果任务长时间停在非终态：

- 先标记为平台卡住，不直接当失败
- 保留全部历史 task_id
- 默认允许自动重提一次
- 如果主体预览阶段连续重提后仍不理想，再询问用户是否有参考图
