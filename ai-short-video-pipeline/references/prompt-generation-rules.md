# Prompt Generation Rules（提示词生成规则）

## Overview

这个文件定义三条铁律：

1. **硬结构**：每个 prompt 由哪几段拼成，顺序不能变
2. **三层分工**：剧本解析、空间锁定卡、风格基因各管什么，不重叠、不遗漏
3. **风格参数表**：每种风格的 6 组基因填什么值

### 核心认知（2026-05-06） #type/discovery #decision/提示词模板

**同一套提示词用在不同模型（GPT-Image-2、Seedream-5.0-lite），效果大差不差。**
想要好的风格图片，关键不是换模型，而是提示词的书写质量。提示词框架模板需要持续优化——这是产出质量的核心杠杆。

### 当前生效说明

用户侧当前默认看到的预设入口，以 [style-presets.md](../../ai-video-image-prompts/references/style-presets.md) 为准。

也就是说：

- 用户交互层优先使用 `AI科普赛博明亮HUD风`、`手绘水彩教学风`、`3D科技讲解风`
- 本文件中的结构化示例负责说明“风格基因应该怎么写、怎么转写进提示词”

不要因为本文件里保留了更详细的示例风格参数，就绕开 `style-presets.md` 的用户侧命名和选择逻辑。

## 1. Prompt Hard Structure（硬结构）

每个镜头的 `image_prompt` 必须按以下字段顺序拼接。无论什么项目、什么风格，这个顺序不变：

```
[空间锚点] + [主体] + [动作/状态] + [构图/景别] + [风格基因转写] + [文字规则] + [负面约束]
```

### 附加规则：品牌 Logo 处理

AI 生图模型不认识真实品牌 logo，写品牌名只会让模型瞎编。本项目维护一份**品牌 Logo 参考库**，所有已知品牌 logo 已上传到 TOS。

**用法：**
- 文案涉及下表中的品牌 → 自动从库中取 `reference_urls`，提示词写 `render the official logo from the reference image`
- 品牌不在表中但属于**全球知名品牌**（如 NVIDIA、Google、Meta、Intel 等）→ 直接在提示词中描述其公认 logo 的视觉特征（形状、颜色、关键元素），GPT-Image-2 可以基于描述渲染出可识别版本
- 品牌较冷门、视觉特征不明显 → 靠口播/字幕识别，生图用画面情境表达

**品牌 Logo 参考库：**

| 品牌 | TOS URL | 添加日期 |
|------|---------|---------|
| Qwen (千问/通义千问) | `https://shdjahdk.tos-cn-beijing.volces.com/ai-short-video-assets/brand-logos/1778070726-%E5%8D%83%E9%97%AE.png` | 2026-05-06 |
| Codex (OpenAI) | `https://shdjahdk.tos-cn-beijing.volces.com/ai-short-video-assets/brand-logos/1778070759-%E4%B8%8B%E8%BD%BD.png` | 2026-05-06 |
| Claude (Anthropic) | `https://shdjahdk.tos-cn-beijing.volces.com/ai-short-video-assets/brand-logos/1778070955-Claude.jpeg` | 2026-05-06 |

**无参考图也能用的品牌（视觉描述即够）：**
- OpenClaw → 小龙虾
- 微信 → 绿色聊天气泡
- 企业微信 → 蓝色工作台图标

这条属于 [主体] 字段的补充约束，不单独成段。

### 附加规则：画面文字最小化

所有 AI 生图模型（包括 GPT-Image-2）无法稳定生成准确的中文或英文文字。因此：

1. **尽量减少画面中的文字量** — UI 界面优先用空白/占位符，不要写长句或多行文字
2. **如必须出现文字，只用一句短语** — 例如 `a single short Chinese label like "指挥中心"`，不要写多行或多句
3. **多行文字、段落文字留给后期剪辑处理** — 生图时不生成可读长文本
4. 提示词中写 `blank UI panels ready for text overlay in post-production` 代替 `filled with Chinese text`

### 逐字段说明

| 字段 | 来源 | 内容 | 可变性 |
|------|------|------|--------|
| 空间锚点 | 空间锁定卡 | 环境锚点简述 + 光线方向 | 同场景不变，切换场景时变 |
| 主体 | 剧本解析 + 三视图 | 人物外貌引用（不重写五官） | 主讲人固定，配角按镜头变 |
| 动作/状态 | 剧本解析关键动作 | 本镜头人物做什么、什么状态 | 每镜不同 |
| 构图/景别 | 空间锁定卡机位参考 | 景别、角度、取景范围 | 每镜不同 |
| 风格基因转写 | 风格参数表 | 色彩+光影+质感+构图+镜头+情绪 的自然语言 | 同项目不变 |
| 负面约束 | Production Bible | 禁止项列表 | 同项目不变 |

### 示例（赛博朋克风 shot_01）

```
[空间锚点] Futuristic tech company HQ interior, dark glass walls, grid floor with glowing neon lines,
main light from overhead holographic displays (cool blue), side fill from wall panels (purple).

[主体] The female host character (match the approved three-view sheet exactly — do not redesign facial features, eyes, face shape or hairstyle),
standing at a command console.

[动作/状态] Reaching toward a holographic display, explaining something to the viewer, confident posture.

[构图/景别] Medium shot, slightly low angle for authority, subject centered, depth of field shallow with background blurred.

[风格] Cyberpunk cinematic, neon blue-purple palette, high contrast, dark backgrounds, glossy metallic surfaces,
8K detail, 35-50mm lens feel, cool teal-magenta color grade, hard edge shadows with neon spill,
clean linework, futuristic mood.

[负面约束] No anime-style oversized eyes, no chibi proportions, no English-only UI text (use Chinese first),
no more than 3 main visual elements in frame, no extra characters, no distorted hands or faces.
```

### 对 API 提交时的处理

提交给生图接口时，上述分块合并为一段连续英文 prompt（因为 GPT-Image-2 等模型英文理解更稳定）：

```text
Futuristic tech company HQ interior, dark glass walls, grid floor with glowing neon lines, main light from overhead holographic displays (cool blue), side fill from wall panels (purple). The female host character (match the approved three-view sheet exactly — do not redesign facial features, eyes, face shape or hairstyle), standing at a command console, reaching toward a holographic display, explaining something to the viewer, confident posture. Medium shot, slightly low angle, subject centered, depth of field shallow with background blurred. Cyberpunk cinematic, neon blue-purple palette, high contrast, dark backgrounds, glossy metallic surfaces, 8K detail, 35-50mm lens feel, cool teal-magenta color grade, hard edge shadows with neon spill, clean linework, futuristic mood. No anime-style oversized eyes, no chibi proportions, no English-only UI text (use Chinese first), no more than 3 main visual elements in frame, no extra characters, no distorted hands or faces.
```

## 2. Three-Layer Division of Labor（三层分工）

### 剧本解析 管什么

| 维度 | 具体内容 | 后续怎么用 |
|------|---------|-----------|
| 角色 | 年龄段、性别、职业气质、服装、状态 | → 填入 prompt [主体] 字段 |
| 场景 | 空间类型、光线条件、关键物品 | → 喂给空间锁定卡 |
| 情绪线 | 文案情绪走向（压抑→转折→振作） | → 调整各镜头的动作/状态语气 |
| 色调线 | 对应情绪的色调方向（冷蓝→过渡→暖金） | → 影响风格基因的 color_palette 微调 |
| 关键动作 | 每个信息点的动作节点 | → 填入 prompt [动作/状态] 字段 |
| 道具/细节 | 品牌、UI 文字、特定物品 | → 补充到 prompt [主体] 或 [动作] 中 |

**不管：** 画法、渲染方式、线条风格、材质质感、负面约束

### 空间锁定卡 管什么

| 维度 | 具体内容 | 后续怎么用 |
|------|---------|-----------|
| 环境锚点 | ≥3 个固定参照物及位置 | → 填入 prompt [空间锚点] 字段 |
| 光线方向 | 主光源来源、方向、色温 | → 填入 prompt [空间锚点] 字段 |
| 人物站位 | 默认位置、可选位置 | → 约束 prompt [主体] 的位置描述 |
| 轴线管理 | 人物 ↔ 参照物的空间关系 | → 防止相邻镜头空间跳变 |
| 机位参考 | 默认景别、特写景别、全景景别 | → 填入 prompt [构图/景别] 字段 |

**不管：** 色彩方案、渲染风格、材质质感、情绪氛围

### 风格基因 管什么

| 基因组 | 具体内容 | 后续怎么用 |
|--------|---------|-----------|
| color_palette | 主色、辅色、强调色、饱和度、对比度 | → 转写为 prompt [风格] 段 |
| lighting_profile | 光线类型、方向、色温、阴影风格 | → 转写为 prompt [风格] 段 |
| texture_profile | 颗粒感、锐度、材质、表面质感 | → 转写为 prompt [风格] 段 |
| composition_tendencies | 构图倾向、景深、留白 | → 转写为 prompt [风格] 段 |
| camera_language | 焦距、运镜风格、角度 | → 转写为 prompt [风格] 段 |
| mood_keywords | 情绪关键词、时空背景、后期处理 | → 转写为 prompt [风格] 段 |

**不管：** 具体人物外貌、具体场景布局、具体动作内容

### 三层关系图

```
剧本解析（内容层）
  ├─ 角色 ──→ [主体]
  ├─ 关键动作 ──→ [动作/状态]
  ├─ 场景信息 ──→ 喂给空间锁定卡
  └─ 情绪/色调线 ──→ 微调风格基因

空间锁定卡（空间层）
  ├─ 环境锚点 ──→ [空间锚点]
  ├─ 光线方向 ──→ [空间锚点]
  └─ 机位参考 ──→ [构图/景别]

风格基因（风格层）
  └─ 6组参数 ──→ [风格基因转写]

负面约束（安全层）
  └─ 禁止项列表 ──→ [负面约束]
```

## 3. 风格参数表（Style Gene Presets）

以下是预置风格模板。新项目套用时，从表中选一个填入对应基因值。

每个预设的负面约束默认包含**画面文字最小化规则**（见 §1 附加规则）。

### 预设：AI 科普赛博明亮 HUD 风（Cyberpunk Bright HUD Infographic）

适用：AI 知识科普视频、技术产品展示、科技教育类内容

```json
{
  "style_name": "AI科普赛博明亮HUD风",
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
    "material_feel": "glossy glass HUD panels + reflective floor + transparent overlays",
    "resolution_feel": "cinematic 4K",
    "surface_quality": "polished 3D render, smooth gradients"
  },
  "composition_tendencies": {
    "framing": "symmetrical centered, subject in middle with floating panels left/right",
    "depth_of_field": "shallow to medium, background dissolved in darkness",
    "rule_of_thirds": false,
    "leading_lines": true,
    "symmetry": "primary — centered focal point",
    "negative_space": "dark navy void surrounding center composition"
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
```

**负面约束（此风格默认）：**

```
- No anime-style oversized eyes or chibi proportions
- No photorealistic humans — use iconic/symbolic geometric AI avatars
- Minimize on-screen text — use bold glowing single-word English labels only
- If a well-known brand is referenced, render its OFFICIAL logo from reference image
- No more than 3-4 main visual elements per frame
- No warm colors or natural lighting
- No cluttered compositions — organized infographic layout
- Deep navy-black (#050712) background, glossy glass HUD panels, reflective floor as scene anchors
```

### 预设：手绘水彩教学风（Hand-Painted Watercolor Educational）

适用：AI 知识科普、儿童/入门教学、温暖叙事类内容

```json
{
  "style_name": "手绘水彩教学风",
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
    "shadow_style": "painted soft irregular shadows, occasional watercolor halo glow around light sources",
    "practical_lights": false
  },
  "texture_profile": {
    "grain": "heavy cold-press watercolor paper grain visible throughout",
    "sharpness": "soft — watercolor pigment blooms and uneven ink outlines",
    "material_feel": "watercolor washes + ink outlines + paper texture + paint splatters",
    "resolution_feel": "handmade storybook illustration",
    "surface_quality": "matte, mottled, aged parchment, no gloss"
  },
  "composition_tendencies": {
    "framing": "left-right visual storytelling, mascot on one side and object/scene on the other",
    "depth_of_field": "flat staged depth, minimal realistic perspective",
    "rule_of_thirds": false,
    "leading_lines": false,
    "symmetry": "occasional for character-portrait or infographic shots",
    "negative_space": "cream parchment breathing room around center composition"
  },
  "camera_language": {
    "lens_equivalent": "flat illustrative lens, 16:9 storyboard frame",
    "movement_style": "static, motion conveyed through pose/arrows/splashes not camera",
    "angle_tendency": "straight-on or slightly elevated desk-level view",
    "transition_style": "clean storyboard cuts"
  },
  "mood_keywords": ["warm", "cozy", "whimsical", "educational", "handmade", "gentle", "storybook", "analog creativity"],
  "era_spatial": "cozy analog classroom or workshop desk, watercolor storybook world, vintage paper bulletin-board",
  "post_processing": "no digital post-processing — the watercolor texture itself is the finish"
}
```

**此风格专用角色系统：**

本风格使用一个固定 mascot 代替传统主讲人：
- 简笔画小人：圆白脑袋 + 蓝色围巾 + 黑色单线身体
- 简单面部表情（点眼 + 弧线嘴）
- 作为全片的视觉锚点和讲解者
- 所有镜头中保持一致外观

**文本呈现规则（此风格专用）：**

- 所有画面文字以**手写毛笔/马克笔书法**风格呈现
- 写在便签、气泡、海报、翻页板、黑板等载体上
- 不使用数字 UI 或打印字体
- 中文优先

**负面约束（此风格默认）：**

```
- No photorealistic rendering — everything must look hand-painted
- No glossy 3D surfaces, no digital UI, no HUD panels
- No cinematic depth of field or lens blur
- No hard directional shadows or dramatic lighting
- No modern sans-serif typography — all text must be brush-calligraphy or hand-lettered
- The stick-figure mascot must appear in most frames as the narrator
- Mascot appearance: round white head, blue scarf, simple black line body — do not redesign
- Background always cream/parchment paper tone, never pure white or dark
- Visible watercolor grain, pigment blooms, and uneven ink lines are required — not defects
- No more than 3-4 main visual elements per frame
- Warm, gentle, cozy atmosphere only — no cold or aggressive tones
```

### 预设：3D 科技讲解风（3D Tech Explainer）

适用：商业短视频科普、产品演示、知识讲解、概念可视化

```json
{
  "style_name": "3D科技讲解风",
  "color_palette": {
    "primary": ["#00D4FF", "#7B68EE"],
    "secondary": ["#0A0E27", "#1A1F3A"],
    "accent": ["#FF6B9D", "#00E5A0"],
    "background_tendency": "dark",
    "saturation": "medium-high",
    "contrast": "medium-high"
  },
  "lighting_profile": {
    "type": "cool ambient + screen fill + soft key + holographic glow + neon rim",
    "direction": "top-down cool ambient, screen panels as fill from front, soft face light on subject, neon rim from behind",
    "warmth": "cool",
    "contrast_ratio": "medium-high — subject bright, background darkened",
    "shadow_style": "soft shadows on subject, deep background with neon spill",
    "practical_lights": true
  },
  "texture_profile": {
    "grain": "none, clean digital 3D render",
    "sharpness": "high detail on UI panels and tech objects, smooth on subject",
    "material_feel": "transparent glass panels + matte tech surfaces + holographic projections + subtle metallic accents",
    "resolution_feel": "cinematic 4K, commercial-grade",
    "surface_quality": "polished 3D render, smooth gradients, clean anti-aliased edges"
  },
  "composition_tendencies": {
    "framing": "dual-subject: character on one side + info/holographic object on the other, centered focal point",
    "depth_of_field": "medium — subject sharp, background slightly softened",
    "rule_of_thirds": false,
    "leading_lines": true,
    "symmetry": "balanced dual-subject, not strict symmetry",
    "negative_space": "zoned info layers with breathing room for subtitle overlay"
  },
  "camera_language": {
    "lens_equivalent": "35mm to 50mm, 16:9 commercial short-video framing",
    "movement_style": "slow push-in, slight lateral drift, smooth follow, eye-level to the action",
    "angle_tendency": "eye-level or slightly elevated, transitioning from subject toward info layer",
    "transition_style": "clean cuts, occasional smooth rack focus from subject to info"
  },
  "mood_keywords": ["futuristic", "clean", "premium", "commercial", "light-cyberpunk", "intelligent", "high-recognition", "trustworthy"],
  "era_spatial": "futuristic tech interior, digital lab, holographic workspace, abstract concept space, server environment",
  "post_processing": "clean digital grade, subtle bloom on holographic elements, no heavy film grain"
}
```

**此风格专用角色系统：**

- 一个可替换的 3D 主讲角色担任全片视觉 IP
- 角色承担讲解、演示、互动、引导视线功能
- 不固定外貌、不锁定服装——不同项目可换不同的主讲形象
- 同一项目内保持一致外观

**此风格视觉特征：**

- 画面中同时存在「角色」和「信息对象」，形成双主体构图
- 信息对象包括：全息模型、流程节点、数据图表、产品界面、象征性概念物
- 大量使用透明玻璃面板、发光数据节点、数字图表、云服务图标、信息流动轨迹
- UI 界面层级清晰，主次关系明确
- 适合字幕叠加，信息层分区清晰

**负面约束（此风格默认）：**

```
- No heavy/dark cyberpunk — keep it light, clean, and commercial
- No photorealistic humans — host is 3D rendered, stylized, premium
- No warm natural lighting — maintain cool tech atmosphere
- No cluttered compositions — info layers must be clearly zoned
- No gritty textures or film grain — clean digital finish
- No anime-style or cartoon rendering — premium 3D commercial quality
- Subject must be prominent against darkened background
- Info objects must be clearly readable and well-lit
- Composition must leave space for subtitle overlay
- No more than 3-4 main visual elements per frame (character + info object + accent element)
```



### 附加规则：构图多样性强制约束（2026-05-08）

**问题：** 连续多镜使用同一套句式（如「人在左指向右面板」），导致画面雷同。

**规则：写一批提示词前，必须先规划镜头类型分布，写完必须自检。**

#### 镜头类型多样性要求

每个批次（≤15 张）必须满足以下分布，不满足则重写：

| 要求 | 规则 |
|------|------|
| 主机位变化 | 每 3 镜中，至少 2 种不同的景别（特写/中景/广角/大全景） |
| 构图变化 | 每 3 镜中，至少 2 种不同的主体布局（左/右/居中/纯信息无人） |
| 动作变化 | 每 5 镜中，至少 3 种不同的主体动作（指/演示/观察/行走/互动/回应），不能全是指向面板 |
| 纯信息镜头 | 每 10 镜中，至少 1 张纯信息可视化（无人物） |
| 特殊角度 | 每 10 镜中，至少 1 张俯拍或低角度 |

#### 自检清单

生完一批提示词后、提交 API 前，强制自问：

```
❏ 这批里有没有 3 张连续的镜头，人物站在同一侧做同一个手势？→ 有就重写
❏ 这批里有没有 2 张连续的镜头，景别完全一样？→ 有就重写
❏ 这批里纯信息镜头（无人物）够不够？→ 10 镜中至少 1 张
❏ 人物站在画面左边的次数 vs 右边的次数是否平衡？→ 不能全在一边
```

**不通过自检的批次，不允许提交 API。**

#### 处理主讲人镜头时的写作禁忌

以下句式在同批中**最多使用 2 次**，超了就重写：

- `stands on the left, one hand pointing toward...`
- `stands on the right, gesturing toward...`
- `hands spread in an explanatory gesture, facing toward...`
- `hand extended in a demonstration gesture toward...`

**替代写法示例：**

- 人物正面面对镜头，身后是浮空信息面板（host front-facing, info behind）
- 人物侧身从画面边缘走入，视线引导观众看向中心信息对象（walking into frame）
- 人物只露手部局部，正在操作全息界面（hands-only close-up）
- 人物坐在控制台前，侧后角度，面板在面前展开（over-the-shoulder）
- 无人物，纯信息可视化（no host at all）

---

## 4. 使用流程

### 新项目启动时

1. `ai-video-shot-planner` 完成 **剧本解析**（Step 0）→ 产出内容层数据
2. `ai-video-shot-planner` 完成 **空间锁定卡**（Step 0.5）→ 产出空间层数据
3. 总控根据用户选择的风格，从 **风格参数表（本文档 §3）** 中加载对应基因
4. 三选一：
   - 直接用预设风格 → 从表里取参数
   - 从预设出发微调 → 从表里取参数，用户改个别基因值
   - 完全自定义 → 用户逐个描述 6 组基因
5. 合并三层数据 → 按 **硬结构（本文档 §1）** 生成每个镜头的 prompt

### 镜头拆分时

`ai-video-shot-planner` 的 Step 1 输出的每行镜头数据，在进入 `ai-video-image-prompts` 之前，必须先补上：

- `spatial_lock_ref`：关联到哪个空间锁定卡
- `style_gene_ref`：关联到哪个风格基因模板
- 只有这两样都补上了，才允许进入提示词生成

### 换项目 / 换风格时

如果用户说"下次换个风格"：

- **需要重做的**：风格基因参数（从表里选另一个预设，或重新定义）
- **不需要重做的**：剧本解析（文案变了才重做）、空间锁定卡（场景变了才重做）、硬结构（永远不变）
- **可能需要微调的**：负面约束（某些风格有特殊禁止项）

### 昨天的问题复盘

昨天 RALV 项目 16 个镜头的失败模式：

| 问题 | 根因 | 本次规范修复 |
|------|------|------------|
| 风格太二次元 | 写了"anime style"但没有硬约束"不要 oversized eyes" | §3 赛博朋克负面约束第一条 |
| 画面太密集 | 没限制元素数量 | §3 负面约束"no more than 3-4 main elements" |
| AI 角色太像真人 | 没约束角色风格方向 | §3 负面约束"AI characters should be iconic/symbolic" |
| 文字全是英文 | 没指定语言方向 | §3 负面约束"Chinese first, English secondary" |
| 空间一致性漂移 | 空间锁定卡没有真正继承到 prompt | §1 硬结构 [空间锚点] 第一个字段，不可跳过 |

## 5. 文件关系

```
ai-short-video-pipeline/references/
├── prompt-generation-rules.md    ← 本文档（提示词生成总规则）
├── consistency-rules.md          ← 一致性控制规则（角色/风格/空间稳定性）
├── style-gene-structure.md       ← 风格基因数据结构定义（本文档 §3 的格式参考）
├── quality-review-loop.md        ← 质量审核回环规则
└── output-format.md              ← 标准输出格式

ai-short-video-pipeline/scripts/
└── calc_shot_plan.py             ← 时长和镜头数估算
```
