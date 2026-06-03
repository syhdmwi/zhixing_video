# Prompt Generation Rules（提示词生成规则）

## Overview

这个文件定义三条铁律：

1. **硬结构**：每个 prompt 由哪几段拼成，顺序不能变
2. **三层分工**：剧本解析、空间锁定卡、风格基因各管什么，不重叠、不遗漏
3. **风格基因转写方法**：如何把已锁定的 6 组风格基因写进 prompt

### 当前生效说明

用户侧当前默认看到的预设入口，以 [style-presets.md](../../ai-video-image-prompts/references/style-presets.md) 为准。

也就是说：

- 用户交互层优先使用 `AI科普赛博明亮HUD风`、`手绘水彩教学风`、`3D科技讲解风`、`黑白素描概念讲解风`
- 本文件只负责说明“风格基因怎么转写进提示词”

预设清单、`style_key`、`style_block`、6 组基因值和默认负面约束都以 `style-presets.md` 为唯一事实来源；不要在本文件复制或改写预设基因值。

## 1. Prompt Hard Structure（硬结构）

每个镜头的 `image_prompt` 必须按以下字段顺序拼接。无论什么项目、什么风格，这个顺序不变：

```
[空间锚点] + [主体] + [动作/状态] + [构图/景别] + [风格基因转写] + [画面文字处理规则] + [负面约束]
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

### 附加规则：画面文字处理规则（默认）

所有 AI 生图模型（包括 GPT-Image-2）都不擅长稳定生成准确的中文或英文文字。因此，画面里的文字默认只做**辅助理解**，不能承担主要叙事。

#### 全局默认规则

1. **默认不生成任何可读长文字**
   - 包括中文标题、英文标签、参数面板文字、品牌说明牌、段落字卡、复杂表格、小字密集说明
2. **默认每镜最多 1 个主文字信息点**
   - 建议控制在 `3~6` 字
   - 解释型、数据型、UI 型镜头，必要时可放宽到 `1 个主信息点 + 1~2 个辅助标签`
   - 每个辅助标签尽量不超过 `4` 字
3. **纯氛围镜、过渡镜、情绪特写镜优先无字**
4. **信息密度优先靠结构层表达**
   - 用模块关系、流程节点、状态颜色、警示标记、图表走势、输入输出链路去表达
   - 不靠小字堆叠、复杂参数墙、大段说明文案去表达
5. **文字必须放在自然视觉容器内**
   - 留白区
   - 暗色区
   - 信息面板区
   - 自然屏幕 / 卡片 / 状态栏 / 提示框区域
   - 不得遮挡核心主体
6. **信息图默认只保留结构，不保留真实可读字**
   - 可以写 `blank infographic panels ready for text overlay in post-production`
7. **所有多行文字、段落文字、数字说明优先留给后期叠字**
8. **只有用户明确要求且画面必须依赖极少量短词时，才允许极少量占位词**
   - 默认项目不要主动启用这条例外

#### 风格适配规则

1. **文字容器风格必须服从当前全局风格模板**
   - 不能把所有项目都强行做成科技 HUD
2. **科技风项目**
   - 可优先使用 HUD 标签、玻璃信息卡、全息标题条、状态栏、系统弹窗、发光提示框
3. **非科技风项目**
   - 使用与当前风格一致的容器语言
   - 例如手绘/纸面项目使用柔和教学卡、纸面注释框、板书式模块框
   - 黑白素描概念项目使用素描信息框、报刊式对照框、结构标记框
4. **默认避免手写、纸条、便签、印章式文字表现**
   - 只有当前风格模板明确允许纸面/手绘/课堂感表达时例外

#### 负面约束建议

在负面约束里优先加入：

```text
no readable long text, no Chinese paragraph text, no English paragraph text, no dense data wall, no complex table typography, no title card blocks, no small unreadable labels
```

### 附加规则：抽象主体三视图

当主体不是人物、动物或现实产品，而是抽象概念、系统模块、知识结构、流程节点、RAG 卡片、知识中枢、网络拓扑、数据模块等“抽象主体”时，三视图阶段必须额外遵守：

1. **先锁资产类型，再生成**  
   未收到用户另行指定时，抽象主体默认按 `科技装置型` 处理，不允许模型自由决定有的变成角色、有的变成图标、有的变成商品。

2. **再锁完成度类型**  
   抽象主体默认输出为 `商业科技插画设定图 / 科技讲解资产图`，不是：
   - 写实工业产品渲染
   - 商品广告主视觉
   - 摄影棚硬件展示图
   - 吉祥物 / Q版角色 / 贴纸图标

3. **统一版式**  
   默认白底或浅灰底，正面 / 侧面 / 背面同图排版，一张图只服务一个主体。

4. **统一风格锚点**  
   同一项目里，如果后面的抽象主体已经生成出被确认的好结果，前面的抽象主体重做时必须向这批已确认结果看齐，保持同一套材质、光影、线条完成度和设定图语言。

推荐在三视图负面约束中固定加入：

```text
no mascot character, no chibi proportions, no sticker icon style, no photorealistic industrial product render, no hardware advertising hero shot, no studio product photography look
```

### 附加规则：人物默认非写实

除非用户明确要求：

- 写实
- 真人感
- 纪实照片感
- 半写实人像
- `photorealistic`

否则所有人物镜头都默认按**非写实风格化人物**处理。

#### 项目级默认字段

每个项目都应显式维护：

- `character_render_mode`

默认值：

- `stylized_illustration`

可选值建议：

- `stylized_illustration`
- `anime_illustration`
- `3d_stylized`
- `sketch_illustration`
- `photorealistic`（仅用户明确要求时启用）

#### 参考图规则

如果用户提供的参考图是真人头像、真人照片、证件照、自拍或真人三视图，默认解释为：

1. **参考人物身份特征**
   - 脸型
   - 五官比例
   - 发型
   - 年龄感
2. **不继承照片质感**
   - 不要真实皮肤质感
   - 不要摄影棚打光
   - 不要 DSLR/写真感
   - 不要自动收敛到写实人像

也就是说，参考图负责锁“是谁”，不负责锁“照片材质”。

#### 人物默认负面约束

当 `character_render_mode` 不是 `photorealistic` 时，人物镜头默认补入：

```text
no photorealistic portrait, no realistic skin texture, no DSLR portrait look, no studio photography lighting, no passport-photo look, no live-action human rendering
```

### 逐字段说明

| 字段 | 来源 | 内容 | 可变性 |
|------|------|------|--------|
| 空间锚点 | 空间锁定卡 | 环境锚点简述 + 光线方向 | 同场景不变，切换场景时变 |
| 主体 | 剧本解析 + 三视图 | 人物外貌引用（不重写五官） | 主讲人固定，配角按镜头变 |
| 动作/状态 | 剧本解析关键动作 | 本镜头人物做什么、什么状态 | 每镜不同 |
| 构图/景别 | 空间锁定卡机位参考 | 景别、角度、取景范围 | 每镜不同 |
| 风格基因转写 | `style-presets.md` 或项目自定义风格上下文 | 色彩+光影+质感+构图+镜头+情绪 的自然语言 | 同项目不变 |
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

### 0.5 先有 visual_carrier，再写 prompt

正式 `image_prompt` 不是从原文直接长出来的，而是先经过：

- 文案类型判断
- 信息单元表
- 镜头功能层
- `visual_carrier` 分配

再进入提示词拼装。

`visual_carrier` 的值集合与分类语义以 [../SKILL.md](../SKILL.md) 的 `3.4 视觉承载层` 为准；本节只说明提示词转写重点，不重新定义分类法。

也就是说，同一句 `source_text`，如果它的 `visual_carrier` 不同，提示词结构重点就不同：

- `host_primary`：人物口播表达优先
- `host_with_visual`：人物 + 辅助视觉并置
- `scene_only`：环境和空间叙事优先
- `concept_explainer`：结构、机制、关系可视化优先
- `data_compare`：对比信息、指标关系优先
- `ui_closeup`：界面、窗口、上传区、流程面板优先
- `brand_symbolic`：品牌符号、品牌识别元素优先

不要跳过 `visual_carrier`，直接把原文句子翻译成“看起来像 prompt 的英文段落”。

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

## 3. 风格基因转写方法（Style Gene Transcription）

风格预设库、4 个预设名称、`style_key`、`style_block`、6 组结构化基因和默认负面约束，统一以 [style-presets.md](../../ai-video-image-prompts/references/style-presets.md) 为准。本文件不再维护任何预设 JSON 或具体基因值。

本节只规定：拿到已锁定的风格基因后，如何把它们稳定转写进每条 `image_prompt`。

### 3.1 输入要求

进入正式提示词生成前，项目必须已经锁定以下风格上下文：

- `style_key`：来自 `style-presets.md`，或自定义风格生成的项目内 key
- `style_block`：一句完整风格块，用于快速定调
- `visual_style.color_palette`
- `visual_style.lighting_profile`
- `visual_style.texture_profile`
- `visual_style.composition_tendencies`
- `visual_style.camera_language`
- `visual_style.mood_keywords`
- `negative_constraints`

如果用户选择 1/2/3/4 预设，直接从 `style-presets.md` 读取对应 `style_key` 和完整上下文。如果用户选择 0 自定义风格，也必须先整理成同样的 6 组结构，再进入批量 prompt。

### 3.2 转写顺序

风格层在 prompt 中只填 `[风格基因转写]` 和 `[负面约束]`，不得覆盖空间层和内容层。

推荐转写顺序：

1. 先写 `style_block`，用一句话固定整体画风。
2. 从 `color_palette` 转写色彩倾向：主色、辅助色、背景明暗、饱和度、对比度。
3. 从 `lighting_profile` 转写光源语言：光型、方向、冷暖、阴影方式、发光或自然光特征。
4. 从 `texture_profile` 转写材质和完成度：纸面、玻璃、3D、线稿、颗粒、清洁度、渲染质感。
5. 从 `composition_tendencies` 转写构图约束：主体位置、信息层布局、留白、景深、画面秩序。
6. 从 `camera_language` 转写镜头语言：镜头感、角度倾向、运动倾向；静帧 prompt 只写画面感，不写真实视频动作。
7. 从 `mood_keywords` 转写情绪气质：只选 3-5 个关键词，不堆满整串形容词。
8. 最后合并 `negative_constraints`，并追加 §1 的画面文字最小化规则。

### 3.3 字段边界

| 基因组 | 转写位置 | 不应越界 |
| --- | --- | --- |
| `color_palette` | 色彩、背景明暗、对比度 | 不替代具体场景物件 |
| `lighting_profile` | 光型、方向、阴影、发光特征 | 不改变空间锁定卡的光源位置 |
| `texture_profile` | 材质、颗粒、渲染完成度 | 不重写主体身份 |
| `composition_tendencies` | 信息层布局、留白、主次关系 | 不覆盖 `shot_function` |
| `camera_language` | 景别倾向、镜头感、角度语言 | 不写图生视频动作 |
| `mood_keywords` | 情绪、气质、观感 | 不替代文案内容 |

### 3.4 推荐句式

将 6 组基因压缩成一段自然语言，不要把 JSON 键名直接塞进 prompt。

```text
[style_block]. Use [color_palette] with [lighting_profile]. Render with [texture_profile]. Keep [composition_tendencies] and [camera_language]. Overall mood: [mood_keywords]. [negative_constraints].
```

写作要点：

- 每条 prompt 都必须继承同一个项目级风格上下文。
- 同一批 prompt 中，风格层句式可以略微变化，但基因含义不能漂移。
- 镜头差异主要来自主体、动作、空间和 `visual_carrier`，不要靠临时改风格制造差异。
- 不要只写预设名；必须把 `style_block` 和关键基因转写成模型可读的视觉语言。
- 不要复制整段 JSON 给生图模型；JSON 只用于系统内部锁定上下文。



### 附加规则：构图多样性强制约束

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
3. 总控根据用户选择的风格，从 [style-presets.md](../../ai-video-image-prompts/references/style-presets.md) 加载对应 `style_key`、`style_block`、6 组基因和负面约束
4. 三选一：
   - 直接用预设风格 → 从 `style-presets.md` 取参数
   - 从预设出发微调 → 从 `style-presets.md` 取参数，用户改个别基因值
   - 完全自定义 → 用户逐个描述 6 组基因
5. 合并三层数据 → 按 **硬结构（本文档 §1）** 生成每个镜头的 prompt

### 镜头拆分时

`ai-video-shot-planner` 的 Step 1 输出的每行镜头数据，在进入 `ai-video-image-prompts` 之前，必须先补上：

- `spatial_lock_ref`：关联到哪个空间锁定卡
- `style_gene_ref`：关联到哪个风格基因模板
- 只有这两样都补上了，才允许进入提示词生成

### 换项目 / 换风格时

如果用户说"下次换个风格"：

- **需要重做的**：风格基因参数（从 `style-presets.md` 选另一个预设，或重新定义）
- **不需要重做的**：剧本解析（文案变了才重做）、空间锁定卡（场景变了才重做）、硬结构（永远不变）
- **可能需要微调的**：负面约束（某些风格有特殊禁止项）

## 5. 文件关系

```
ai-short-video-pipeline/references/
├── prompt-generation-rules.md    ← 本文档（提示词生成总规则）
├── consistency-rules.md          ← 一致性控制规则（角色/风格/空间稳定性）
├── style-gene-structure.md       ← 风格基因数据结构定义
├── quality-review-loop.md        ← 质量审核回环规则
└── output-format.md              ← 标准输出格式

ai-short-video-pipeline/scripts/
└── calc_shot_plan.py             ← 时长和镜头数估算
```
