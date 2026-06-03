# Style Gene Structure（风格基因结构化）

## Overview

风格基因是把「风格」从一段模糊描述拆解成可量化、可组合、可继承的结构化参数。每个风格模板由一组「基因」组成，基因之间可以独立修改、混合搭配、从父模板继承。

## Why

当前模板系统把风格存为一段文字描述，存在以下问题：
- 新文案套用模板时，风格描述可能被模型理解偏移
- 用户想微调某个维度（如「颜色再暖一点」）时，只能重新描述整体风格
- 无法从多个模板混合出新风格（如「A 的色调 + B 的构图 + C 的质感」）
- 不同文案的风格差异无法量化对比

## Style DNA Schema

每个风格模板的 `visual_style` 字段应从扁平文字升级为结构化对象。具体预设值只在 [style-presets.md](../../ai-video-image-prompts/references/style-presets.md) 维护；本文件只定义字段结构。

```text
visual_style
├── style_name
├── style_version
├── color_palette
│   ├── primary
│   ├── secondary
│   ├── accent
│   ├── background_tendency
│   ├── saturation
│   └── contrast
├── lighting_profile
│   ├── type
│   ├── direction
│   ├── warmth
│   ├── contrast_ratio
│   ├── shadow_style
│   └── practical_lights
├── texture_profile
│   ├── grain
│   ├── sharpness
│   ├── material_feel
│   ├── resolution_feel
│   └── surface_quality
├── composition_tendencies
│   ├── framing
│   ├── depth_of_field
│   ├── rule_of_thirds
│   ├── leading_lines
│   ├── symmetry
│   └── negative_space
├── camera_language
│   ├── lens_equivalent
│   ├── movement_style
│   ├── angle_tendency
│   └── transition_style
├── mood_keywords
├── era_spatial
└── post_processing
```

## Gene Categories

### 1. Color Palette（色彩基因）

控制整体色彩倾向。

| Field | Type | Description |
|-------|------|-------------|
| `primary` | string[] | 主色 HEX，1-3 个 |
| `secondary` | string[] | 辅助色 HEX，1-3 个 |
| `accent` | string[] | 强调色 HEX，1-2 个 |
| `background_tendency` | string | 背景倾向：`dark` / `light` / `neutral` / `varied` |
| `saturation` | string | 饱和度：`low` / `medium` / `high` |
| `contrast` | string | 对比度：`low` / `medium` / `high` |

### 2. Lighting Profile（光影基因）

控制光线类型和方向。

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | 光线类型描述 |
| `direction` | string | 主光方向 |
| `warmth` | string | 色温倾向：`warm` / `cool` / `neutral` / `varied` |
| `contrast_ratio` | string | 光比：`low` / `medium` / `high` |
| `shadow_style` | string | 阴影风格描述 |
| `practical_lights` | boolean | 是否使用实景光源 |

### 3. Texture Profile（质感基因）

控制画面材质感和清晰度。

| Field | Type | Description |
|-------|------|-------------|
| `grain` | string | 颗粒感描述 |
| `sharpness` | string | 锐度：`soft` / `medium` / `high detail` |
| `material_feel` | string | 主要材质倾向 |
| `resolution_feel` | string | 分辨率感受 |
| `surface_quality` | string | 表面质感描述 |

### 4. Composition Tendencies（构图基因）

控制构图偏好。

| Field | Type | Description |
|-------|------|-------------|
| `framing` | string | 构图倾向描述 |
| `depth_of_field` | string | 景深描述 |
| `rule_of_thirds` | boolean | 是否遵循三分法 |
| `leading_lines` | boolean | 是否使用引导线 |
| `symmetry` | string | 对称使用方式 |
| `negative_space` | string | 留白使用方式 |

### 5. Camera Language（镜头语言基因）

控制镜头运动和视角。

| Field | Type | Description |
|-------|------|-------------|
| `lens_equivalent` | string | 等效焦距 |
| `movement_style` | string | 运镜风格 |
| `angle_tendency` | string | 角度倾向 |
| `transition_style` | string | 转场风格 |

### 6. Mood & Era（情绪与时空基因）

控制整体情绪和时空背景。

| Field | Type | Description |
|-------|------|-------------|
| `mood_keywords` | string[] | 情绪关键词 |
| `era_spatial` | string | 时空背景描述 |
| `post_processing` | string | 后期处理风格 |

## Inheritance Rules

### 从父模板继承

子模板可以指定 `inherits_from` 字段，声明从哪个父模板继承。未显式覆盖的基因自动沿用父模板的值。

子模板只写 `inherits_from` 和需要覆盖的字段路径。未显式覆盖的基因（光影、质感、构图等）全部继承父模板。父模板引用必须使用 `style_key` 或已保存模板 ID，不使用临时风格名。

### 基因混合

可以从多个模板各取部分基因：

混合时只记录来源模板 ID / `style_key` 与基因组名称，例如“从模板 A 取 `color_palette`，从模板 B 取 `texture_profile`”。不要在混合规则里复制任何来源模板的具体基因值。

### 微调覆盖

用户可以在任何层级做微调：

微调只记录字段路径和用户确认后的新值，例如 `color_palette.saturation` 或 `lighting_profile.warmth`。如果微调来自某个预设，仍保留原始 `style_key` 引用，不复制整段预设 JSON。

## How To Generate Style DNA From Existing Templates

当用户使用旧版扁平风格描述的模板时，自动解析并升级为结构化基因：

1. 从文字描述中提取色彩关键词 → `color_palette`
2. 从文字描述中提取光线关键词 → `lighting_profile`
3. 从文字描述中提取质感关键词 → `texture_profile`
4. 从文字描述中提取构图关键词 → `composition_tendencies`
5. 从文字描述中提取镜头关键词 → `camera_language`
6. 从文字描述中提取情绪关键词 → `mood_keywords`

升级后展示给用户确认，不自动覆盖原模板。

## Prompt Generation From Style DNA

生成正式提示词时，Style DNA 自动转写为提示词中的 Style Block：

```text
Style: [style_block]. Use [color_palette] with [lighting_profile].
Render with [texture_profile]. Keep [composition_tendencies] and [camera_language].
Overall mood: [mood_keywords]. Apply [post_processing].
```

转写规则：
- `color_palette` → 色彩描述句
- `lighting_profile` → 光线描述句
- `texture_profile` → 质感描述句
- `composition_tendencies` + `camera_language` → 镜头描述句
- `mood_keywords` → 情绪关键词
- `post_processing` → 后期描述句

每块之间用逗号连接，形成一段自然语言风格描述。

## Migration Path

旧模板 → 新模板的迁移是渐进式的：

1. 用户套用旧模板时，自动解析为 Style DNA 并展示
2. 用户确认后，保存为新版结构化模板
3. 旧模板保留不删除，新模板用 `_v2` 后缀区分
4. 用户可以随时在新旧模板之间切换

## Related Files

- 模板存档结构： [archive-template.json](../../ai-video-series-archive/references/archive-template.json)
- 风格预设库： [style-presets.md](../../ai-video-image-prompts/references/style-presets.md)
