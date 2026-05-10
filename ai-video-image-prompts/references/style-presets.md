# Style Presets

这个文件定义图片风格预设库。

设计目标有两个：

1. 对用户保持简单，优先用数字选择风格模版
2. 对系统保持稳定，每个预设同时提供可继承的结构化风格上下文

也就是说，用户默认看到的主风格入口是：

- `AI科普赛博明亮HUD风`
- `手绘水彩教学风`
- `3D科技讲解风`
- `黑白素描概念讲解风`

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

## Current Primary Presets

### 1. AI科普赛博明亮HUD风

- 预设名：`AI科普赛博明亮HUD风`
- 英文标识：`cyberpunk_bright_hud_infographic`
- 用户侧一句话说明：
  `明亮赛博科技感、HUD 信息图界面、蓝青紫霓虹高对比、适合 AI 科普和技术讲解`
- 默认色彩倾向：
  `高亮蓝青、霓虹紫、电光粉、深蓝黑背景`
- 默认光影倾向：
  `发光 HUD 面板、体积光、中心高亮、冷色科技光`
- 默认材质倾向：
  `玻璃 HUD、全息界面、反光地面、抛光数字材质`
- 默认环境倾向：
  `未来实验室、数字指挥中心、黑场科技空间、数据可视化展示台`
- 默认构图倾向：
  `中心主体 + 左右信息面板，构图有秩序，适合叠加标题和信息`
- 默认负面约束建议：
  `避免写实真人照片感、避免可爱夸张二次元大眼、避免暖色自然光主导、避免拥挤杂乱、避免过多文字、避免超过 3 到 4 个主视觉元素`

```json
{
  "style_name": "AI科普赛博明亮HUD风",
  "style_key": "cyberpunk_bright_hud_infographic",
  "style_block": "AI 科普赛博明亮 HUD 风，明亮赛博科技感，HUD 信息图界面，蓝青紫霓虹高对比，未来实验室和数字指挥中心氛围，适合 AI 科普和技术讲解",
  "visual_style": {
    "color_palette": {
      "primary": ["#00D8FF", "#267BFF"],
      "secondary": ["#050712", "#101B55"],
      "accent": ["#B13CFF", "#FF3CFF"],
      "background_tendency": "dark",
      "saturation": "high",
      "contrast": "high"
    },
    "lighting_profile": {
      "type": "emissive neon, holographic glow, volumetric light beams",
      "direction": "center-weighted, UI panels as light sources",
      "warmth": "cool",
      "contrast_ratio": "high",
      "shadow_style": "deep navy-black shadows, bloom and light trails on glowing elements",
      "practical_lights": false
    },
    "texture_profile": {
      "grain": "none, clean digital",
      "sharpness": "high detail on UI panels, bloom softening on edges",
      "material_feel": "glossy glass HUD panels, reflective floor, transparent overlays",
      "resolution_feel": "cinematic 4K",
      "surface_quality": "polished 3D render, smooth gradients"
    },
    "composition_tendencies": {
      "framing": "symmetrical centered, subject in middle with floating panels left and right",
      "depth_of_field": "shallow to medium, background dissolved in darkness",
      "rule_of_thirds": false,
      "leading_lines": true,
      "symmetry": "primary",
      "negative_space": "dark navy void around center composition"
    },
    "camera_language": {
      "lens_equivalent": "wide to medium, cinematic 16:9",
      "movement_style": "static or slow push-in",
      "angle_tendency": "straight-on or slightly low angle",
      "transition_style": "clean cuts"
    },
    "mood_keywords": ["futuristic", "empowering", "high-tech", "intelligent", "optimistic", "dramatic"],
    "era_spatial": "dark futuristic cyber lab, holographic command center, digital dashboard room",
    "post_processing": "heavy bloom, volumetric light, lens flare on glow elements, clean digital grade"
  }
}
```

### 2. 手绘水彩教学风

- 预设名：`手绘水彩教学风`
- 英文标识：`hand_painted_watercolor_educational`
- 用户侧一句话说明：
  `温暖手绘、水彩纸纹理、轻松教学氛围、适合知识科普和入门讲解`
- 默认色彩倾向：
  `米白纸色、雾蓝、浅棕、灰绿、低饱和暖色`
- 默认光影倾向：
  `柔和漫射光、低对比、无强烈硬阴影`
- 默认材质倾向：
  `水彩晕染、纸张肌理、墨线轮廓、手工绘本感`
- 默认环境倾向：
  `故事书世界、教学桌面、公告板、温暖教室、纸本空间`
- 默认构图倾向：
  `讲解型平面叙事，主体和辅助内容左右分布，留白自然`
- 默认负面约束建议：
  `避免数字 HUD、避免玻璃金属强反光、避免电影级景深、避免写实照片、避免现代无衬线冷感排版、避免冷硬赛博氛围`

```json
{
  "style_name": "手绘水彩教学风",
  "style_key": "hand_painted_watercolor_educational",
  "style_block": "手绘水彩教学风，温暖手绘感，水彩纸纹理，低饱和柔和色彩，适合知识科普、入门讲解和轻松叙事",
  "visual_style": {
    "color_palette": {
      "primary": ["#F5F0E8", "#3A4A6B"],
      "secondary": ["#7B8FA1", "#8B7355"],
      "accent": ["#C9A96E", "#6B8E6B"],
      "background_tendency": "light",
      "saturation": "low",
      "contrast": "soft"
    },
    "lighting_profile": {
      "type": "diffuse warm ambient, no hard directional source",
      "direction": "omnidirectional soft fill",
      "warmth": "warm",
      "contrast_ratio": "low",
      "shadow_style": "painted soft irregular shadows, occasional watercolor halo glow",
      "practical_lights": false
    },
    "texture_profile": {
      "grain": "heavy watercolor paper grain visible",
      "sharpness": "soft, watercolor pigment blooms and uneven ink outlines",
      "material_feel": "watercolor washes, ink outlines, paper texture, paint splatters",
      "resolution_feel": "handmade storybook illustration",
      "surface_quality": "matte, mottled, aged parchment"
    },
    "composition_tendencies": {
      "framing": "left-right visual storytelling, mascot or host on one side and object or scene on the other",
      "depth_of_field": "flat staged depth, minimal realistic perspective",
      "rule_of_thirds": false,
      "leading_lines": false,
      "symmetry": "occasional",
      "negative_space": "cream parchment breathing room"
    },
    "camera_language": {
      "lens_equivalent": "flat illustrative lens, 16:9 storyboard frame",
      "movement_style": "static, motion conveyed by pose and layout",
      "angle_tendency": "straight-on or slightly elevated desk-level view",
      "transition_style": "clean storyboard cuts"
    },
    "mood_keywords": ["warm", "cozy", "whimsical", "educational", "handmade", "gentle", "storybook"],
    "era_spatial": "cozy analog classroom, workshop desk, watercolor storybook world, vintage paper bulletin board",
    "post_processing": "no digital post-processing, watercolor texture is the finish"
  }
}
```

### 3. 3D科技讲解风

- 预设名：`3D科技讲解风`
- 英文标识：`3d_tech_explainer`
- 用户侧一句话说明：
  `商业短视频常用的 3D 科技讲解风，人物和信息层并重，适合产品演示和概念可视化`
- 默认色彩倾向：
  `蓝青、紫色、荧光粉、深色科技背景`
- 默认光影倾向：
  `屏幕补光、冷色环境光、柔和主光、轻霓虹轮廓光`
- 默认材质倾向：
  `透明玻璃面板、科技磨砂材质、全息投影、少量金属点缀`
- 默认环境倾向：
  `科技办公室、讲解舞台、数字产品空间、信息可视化场景`
- 默认构图倾向：
  `人物主体和信息对象分区并置，适合短视频讲解镜头`
- 默认负面约束建议：
  `避免画面过暗、避免 UI 堆满画面、避免信息层太多导致主体被淹没、避免低幼卡通、避免写实照片感、避免杂乱文字`

```json
{
  "style_name": "3D科技讲解风",
  "style_key": "3d_tech_explainer",
  "style_block": "3D 科技讲解风，商业短视频常用的 3D 科技讲解视觉，人物与信息层并重，蓝青紫科技色调，适合产品演示、概念可视化和知识讲解",
  "visual_style": {
    "color_palette": {
      "primary": ["#00D4FF", "#7B68EE"],
      "secondary": ["#0A0E27", "#1A1F3A"],
      "accent": ["#FF6B9D", "#00E5A0"],
      "background_tendency": "dark",
      "saturation": "medium-high",
      "contrast": "medium-high"
    },
    "lighting_profile": {
      "type": "cool ambient, screen fill, soft key, holographic glow, neon rim",
      "direction": "top-down cool ambient, front fill from panels, soft face light, rim from behind",
      "warmth": "cool",
      "contrast_ratio": "medium-high",
      "shadow_style": "soft shadows on subject, deep background with neon spill",
      "practical_lights": true
    },
    "texture_profile": {
      "grain": "none, clean digital 3D render",
      "sharpness": "high detail on UI panels and tech objects, smooth on subject",
      "material_feel": "transparent glass panels, matte tech surfaces, holographic projections, subtle metallic accents",
      "resolution_feel": "cinematic 4K, commercial-grade",
      "surface_quality": "polished 3D render, smooth gradients, clean edges"
    },
    "composition_tendencies": {
      "framing": "dual-subject composition, character on one side plus holographic object or info layer on the other",
      "depth_of_field": "medium, subject sharp and background slightly softened",
      "rule_of_thirds": false,
      "leading_lines": true,
      "symmetry": "balanced but not strict",
      "negative_space": "zoned info layers with breathing room for subtitle overlay"
    },
    "camera_language": {
      "lens_equivalent": "35mm to 50mm, 16:9 commercial short-video framing",
      "movement_style": "slow push-in, slight lateral drift, smooth follow",
      "angle_tendency": "eye-level or slightly elevated",
      "transition_style": "clean editorial tech cuts"
    },
    "mood_keywords": ["commercial", "clear", "smart", "futuristic", "educational", "premium"],
    "era_spatial": "tech workspace, product demo stage, holographic explainer scene",
    "post_processing": "clean digital grade, restrained bloom, premium commercial finish"
  }
}
```

### 4. 黑白素描概念讲解风

- 预设名：`黑白素描概念讲解风`
- 英文标识：`monochrome_sketch_concept_explainer`
- 用户侧一句话说明：
  `黑白铅笔素描、新闻概念插画感、纸面底色和排线阴影明显，适合复刻观点口播类 AI 插画视频`
- 默认色彩倾向：
  `黑白灰为主，暖白纸底，可带极少量局部强调色但默认克制`
- 默认光影倾向：
  `结构光明确，纸面排线阴影，整体低彩度、低炫光`
- 默认材质倾向：
  `铅笔线稿、炭笔排线、纸张纹理、概念草图感、新闻插画感`
- 默认环境倾向：
  `办公室、法庭、会议室、实验室、演讲现场、社会议题场景、概念说明场景`
- 默认构图倾向：
  `主体明确，画面像观点插画或新闻概念图，允许局部夸张象征元素，但整体结构清晰`
- 默认负面约束建议：
  `避免霓虹赛博色、避免厚涂油画、避免写实照片感、避免强 3D 材质、避免卡通低幼、避免背景过满、避免多余彩色元素、避免复杂无意义文字`

```json
{
  "style_name": "黑白素描概念讲解风",
  "style_key": "monochrome_sketch_concept_explainer",
  "style_block": "黑白素描概念讲解风，黑白铅笔线稿和排线阴影，暖白纸面底色，新闻概念插画感，适合观点口播、财经科技评论和社会议题讲解",
  "visual_style": {
    "color_palette": {
      "primary": ["#1F1F1F", "#5E5E5E"],
      "secondary": ["#B9B1A4", "#EDE7DC"],
      "accent": ["#C97A3D", "#7BA7D9"],
      "background_tendency": "warm paper light",
      "saturation": "very low",
      "contrast": "medium"
    },
    "lighting_profile": {
      "type": "structural light with hand-drawn shading",
      "direction": "clear form light, sketch-style tonal separation",
      "warmth": "neutral to slightly warm",
      "contrast_ratio": "medium",
      "shadow_style": "cross-hatching, pencil shading, charcoal-like depth",
      "practical_lights": false
    },
    "texture_profile": {
      "grain": "visible paper grain",
      "sharpness": "line clarity first",
      "material_feel": "graphite pencil, charcoal shading, sketchbook paper, editorial concept drawing",
      "resolution_feel": "high-quality editorial illustration board",
      "surface_quality": "matte, tactile, hand-drawn"
    },
    "composition_tendencies": {
      "framing": "single strong concept per frame, readable silhouette, concept-illustration layout",
      "depth_of_field": "minimal optical blur, rely on drawing structure",
      "rule_of_thirds": true,
      "leading_lines": true,
      "symmetry": "optional",
      "negative_space": "clean paper breathing room around key concept"
    },
    "camera_language": {
      "lens_equivalent": "35mm to 70mm framing logic",
      "movement_style": "illustrative still-frame logic",
      "angle_tendency": "readable, descriptive, slightly dramatic when needed",
      "transition_style": "editorial cut, concept board continuity"
    },
    "mood_keywords": ["editorial", "analytical", "serious", "conceptual", "hand-drawn", "narrative"],
    "era_spatial": "news illustration world, concept storyboard, social-issue explainer scenes",
    "post_processing": "preserve pencil texture and paper tone, keep grayscale hierarchy clear, avoid digital glow"
  }
}
```

## Interaction Rule

当用户输入 `1` 后，再展示以下可选项：

- `AI科普赛博明亮HUD风 请输入 1`
- `手绘水彩教学风 请输入 2`
- `3D科技讲解风 请输入 3`
- `黑白素描概念讲解风 请输入 4`
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

如果后面继续新增预设，例如油画、像素风、国风、商业广告风，优先继续往这个文件里追加，不要把预设散落在多个 skill 里重复维护。
