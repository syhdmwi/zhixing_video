# Archive Fields

## Required Core Fields

- `series_name`: 用户看得懂的档案名称
- `series_slug`: 文件名使用的稳定 slug
- `default_image_model`: 后续默认生图模型
- `default_aspect_ratio`: 后续默认比例
- `default_output_language`: 后续默认输出语言
- `style_summary`: 固定风格描述
- `negative_constraints`: 固定负面约束

## Subject Assets

`subject_anchors` 里每个主体至少保存：

- `subject_id`
- `subject_type`
- `summary`
- `preview_images`
- `three_view_images`

## Review Assets

以下内容越完整，后续复用越稳：

- `style_reference_images`
- `approved_preview_images`
- `approved_three_view_images`
- `approved_final_images`

## Usage Rule

下次复用时，优先继承：

1. 已确认图片锚点
2. 固定风格描述
3. 固定负面约束
4. 默认模型与比例
