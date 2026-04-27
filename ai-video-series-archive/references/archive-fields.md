# Template Fields

模板只保存跨文案稳定复用的内容。

不要默认把每篇文案临时出现的重复主体保存进去。

## Required Core Fields

- `template_name`: 用户看得懂的模板名称
- `template_slug`: 文件名使用的稳定 slug
- `template_type`: 默认使用 `series_style_template`
- `created_at`: 创建时间
- `created_from_script`: 创建模板时使用的文案来源，可为空

## Main Character

`main_character` 用于保存长期稳定出场的主讲人。

推荐字段：

- `description`: 主讲人文字描述
- `front_draft_url`: 已确认的正面定稿
- `three_view_url`: 已确认的主讲人三视图
- `notes`: 人物相关注意事项

主讲人是模板的核心资产，默认保存。

## Visual Style

`visual_style` 用于保存画面风格。

推荐字段：

- `summary`: 风格摘要
- `reference_image_urls`: 用户提供或确认的风格参考图
- `approved_style_sample_urls`: 用户明确选择保存的正式成图样例

正式成图样例不能自动保存。
只有用户明确输入图片编号后，才保存到 `approved_style_sample_urls`。

## Prompt Rules

`prompt_rules` 用于保存提示词写法和约束。

推荐字段：

- `image_prompt_structure`: 图片提示词结构
- `negative_constraints`: 负面约束
- `composition_preference`: 构图偏好
- `brand_logo_rule`: 品牌、地标、标志性元素处理规则
- `subject_rule`: 重复主体与固定主体处理规则

## Defaults

`defaults` 用于保存下次默认值。

推荐字段：

- `aspect_ratio`
- `image_model`
- `video_mode`
- `output_language`

## Fixed Subjects

`fixed_subjects` 只保存用户明确要求长期固定出场的角色或物体。

默认应为空数组。

不要把每篇文案自动识别出来的重复主体保存到这里。

示例：

```json
"fixed_subjects": []
```

如果用户明确说“小龙虾以后每篇都要出现”，才保存：

```json
"fixed_subjects": [
  {
    "subject_id": "openclaw_lobster",
    "subject_type": "mascot",
    "description": "红色可爱小龙虾，不要机甲风",
    "three_view_url": ""
  }
]
```

## Do Not Save By Default

以下内容默认不保存进通用模板：

- 每篇文案临时出现的重复主体
- 单次项目的完整任务队列
- 用户未选择的正式成图
- 不满意或勉强通过的图片

如果需要回溯单次项目，应另存为项目档案，而不是通用模板。
