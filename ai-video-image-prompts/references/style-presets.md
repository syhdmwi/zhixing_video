# Style Presets

这个文件定义图片风格预设库。

设计目标有两个：

1. 对用户保持简单，优先用数字选择风格模版
2. 对系统保持稳定，每个预设同时提供可继承的结构化风格上下文

也就是说，用户看到的是：

- `赛博朋克风格`
- `素描风格`

系统内部拿到的则不只是一个名字，还包括：

- 风格块
- 色彩倾向
- 光影倾向
- 材质倾向
- 环境倾向
- 构图倾向
- 负面约束建议
- 可选的结构化风格上下文

## Usage Rule

当用户输入文案后，如果还没有给出完整风格描述，优先按以下方式提问：

- 使用风格模版请输入 `1`
- 自主设定风格请输入 `2`

如果用户输入 `1`，再展示当前可选风格模版。

如果用户输入 `2`，再继续按自定义风格描述生成。

如果用户后续又补了新的风格要求，用户补充要求优先级更高。

## Current Presets

### 1. Cyberpunk

- 预设名：`赛博朋克风格`
- 英文标识：`cyberpunk`
- 用户侧一句话说明：
  `偏动漫化和风格化表达，避免写实风格，霓虹灯光，高对比冷暖色，未来都市科技感，金属与玻璃材质，空间纵深强，画面张力强`
- 默认色彩倾向：
  `蓝紫、青色、电光粉、局部高亮霓虹橙`
- 默认光影倾向：
  `夜景霓虹边缘光、局部高反差、也允许阳光明媚的高通透白天赛博场景`
- 默认材质倾向：
  `金属、玻璃、电子屏、发光线条、全息界面、自然植被与科技材质共存`
- 默认环境倾向：
  `未来都市街区、科技办公空间、数字控制台、霓虹走廊、赛博朋克自然环境、阳光明媚的高科技户外空间`
- 默认构图倾向：
  `透视强，前中后景层次清晰，镜头感强，留出标题或信息叠加空间`
- 默认负面约束建议：
  `避免低清晰度、避免脏乱到主体难辨认、避免过暗、避免霓虹过曝、避免赛博元素堆砌失控、避免人物脸部被灯光遮死、避免多余文字和logo、避免写实照片风、避免纪实真人感过强`

```json
{
  "style_name": "赛博朋克风格",
  "style_key": "cyberpunk",
  "style_block": "赛博朋克风格，偏动漫化和风格化表达，避免写实风格，霓虹灯光，高对比冷暖色，蓝紫青粉电光氛围，未来都市科技感，金属与玻璃材质，强烈空间透视，画面张力强",
  "visual_style": {
    "color_palette": {
      "primary": ["#00d8ff", "#5b5fff", "#ff4fd8"],
      "secondary": ["#0b1020", "#151d3b"],
      "accent": ["#ff8a00", "#7bffcf"],
      "background_tendency": "dark or bright futuristic",
      "saturation": "high",
      "contrast": "high"
    },
    "lighting_profile": {
      "type": "neon edge light, holographic glow, or sunlit futuristic clarity",
      "direction": "rim light + side light + motivated environment light",
      "warmth": "cool with selective warm accents",
      "contrast_ratio": "high",
      "shadow_style": "clear shape separation, neon spill, no muddy shadows",
      "practical_lights": true
    },
    "texture_profile": {
      "grain": "clean digital",
      "sharpness": "high detail",
      "material_feel": "metal, glass, holographic UI, luminous surfaces, occasional wet reflections",
      "resolution_feel": "high-end commercial illustration",
      "surface_quality": "crisp, glossy, high-recognition"
    },
    "composition_tendencies": {
      "framing": "strong perspective with foreground-midground-background separation",
      "depth_of_field": "medium to shallow depending on shot goal",
      "rule_of_thirds": true,
      "leading_lines": true,
      "symmetry": "used selectively for impact",
      "negative_space": "reserve clean zones for text overlays or UI"
    },
    "camera_language": {
      "lens_equivalent": "28mm to 50mm",
      "movement_style": "dynamic but readable, cinematic framing",
      "angle_tendency": "slightly low angle or strong perspective angle",
      "transition_style": "clean cut, neon motion, data-like transitions"
    },
    "mood_keywords": ["futuristic", "electric", "high-energy", "clean-tech", "stylized", "commercial"],
    "era_spatial": "future city, tech interiors, holographic workspaces, cyber-natural hybrid environments",
    "post_processing": "bright neon bloom, crisp highlight control, no muddy blacks, no overexposed glow wash"
  }
}
```

### 2. Sketch

- 预设名：`素描风格`
- 英文标识：`sketch`
- 用户侧一句话说明：
  `铅笔线稿质感，黑白灰层次，纸张纹理，线条清晰，阴影排线自然，结构感明确，画面简洁克制`
- 默认色彩倾向：
  `黑白灰为主，可接受极轻微米白纸色`
- 默认光影倾向：
  `克制的明暗对比，结构光明确，不做夸张霓虹或彩色打光`
- 默认材质倾向：
  `铅笔、炭笔、纸张、排线、轻颗粒纸面纹理`
- 默认环境倾向：
  `人物结构研究、场景草图、建筑草图、物体结构图、简洁叙事画面`
- 默认构图倾向：
  `结构清晰，主次分明，避免花哨背景抢主体`
- 默认负面约束建议：
  `避免彩色霓虹、避免油画厚涂、避免照片写实质感、避免过多杂乱背景、避免线条糊掉、避免过强景深虚化、避免多余文字和logo`

```json
{
  "style_name": "素描风格",
  "style_key": "sketch",
  "style_block": "素描风格，铅笔线稿质感，黑白灰层次，纸张纹理，线条清晰，阴影排线自然，结构感明确，克制的明暗对比，画面简洁",
  "visual_style": {
    "color_palette": {
      "primary": ["#1d1d1d", "#5a5a5a"],
      "secondary": ["#8c8c8c", "#e8e2d6"],
      "accent": ["#b0b0b0"],
      "background_tendency": "light paper or neutral",
      "saturation": "very low",
      "contrast": "medium"
    },
    "lighting_profile": {
      "type": "structural light for form reading",
      "direction": "clear single-direction study light or soft ambient light",
      "warmth": "neutral",
      "contrast_ratio": "medium",
      "shadow_style": "cross-hatching, tonal pencil shading, clean edge control",
      "practical_lights": false
    },
    "texture_profile": {
      "grain": "paper tooth visible",
      "sharpness": "line clarity first",
      "material_feel": "graphite, charcoal, dry pencil, matte paper",
      "resolution_feel": "high-quality illustration board study",
      "surface_quality": "matte, tactile, hand-drawn"
    },
    "composition_tendencies": {
      "framing": "clean composition with readable silhouette and structure",
      "depth_of_field": "minimal optical blur, structure remains readable",
      "rule_of_thirds": true,
      "leading_lines": true,
      "symmetry": "not required",
      "negative_space": "simple blank paper breathing room"
    },
    "camera_language": {
      "lens_equivalent": "35mm to 70mm equivalent framing logic",
      "movement_style": "static illustration feel",
      "angle_tendency": "descriptive and readable",
      "transition_style": "clean editorial cut"
    },
    "mood_keywords": ["clean", "structural", "quiet", "analytical", "minimal", "hand-drawn"],
    "era_spatial": "paper sketch world, design study board, monochrome illustrative environment",
    "post_processing": "preserve pencil texture, keep grayscale range readable, avoid artificial digital glow"
  }
}
```

## Interaction Rule

当用户输入 `1` 后，再展示以下可选项：

- `赛博朋克风格 请输入 1`
- `素描风格 请输入 2`
- `自主设定风格请输入 0`

## System Rule

当系统内部加载风格预设时：

1. 优先读取该预设的 `style_block`
2. 再读取 `visual_style` 里的结构化字段
3. 生成正式提示词时，同时继承：
   - 风格块
   - 色彩倾向
   - 光影倾向
   - 材质倾向
   - 环境倾向
   - 构图倾向
   - 负面约束建议

不要只把预设名写进提示词里就结束。

## Extension Rule

如果后面继续新增预设，例如水彩、油画、像素风、国风、商业广告风，优先继续往这个文件里追加，不要把预设散落在多个 skill 里重复维护。
