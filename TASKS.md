# Codex 执行任务卡

> 配套 [OPTIMIZATION_PLAN.md](./OPTIMIZATION_PLAN.md)。Codex 按 Phase 顺序执行，每个 Phase 做完**停下汇报**等 Claude review。
> 约束：严格遵守 OPTIMIZATION_PLAN §2 架构原则。改动前先读相关文件，不要凭记忆改。
> 标记：`[ ]` 待办 / `[~]` 进行中 / `[x]` review 通过。

---

## Phase 1 — 步骤 / 流程

### [x] T1.1 统一镜头分类法到 visual_carrier
- **目标**：消除 `frame_type`（旧 4 值）与 `visual_carrier`（新 7 值）双轨。
- **权威定义处**：`ai-short-video-pipeline/SKILL.md` 的 §3.4 视觉承载层（visual_carrier 7 值）。
- **改动点**：
  - 在权威处补一张 **frame_type → visual_carrier 映射表**（people_primary→host_primary，people_with_scene→host_with_visual，scene_only→scene_only，concept_explainer→concept_explainer）。
  - `ai-video-image-prompts/SKILL.md` 中所有以 `frame_type` 为主的段落（Core Rules、Frame Type Balance Gate、Output 等）：改为以 `visual_carrier` 为主，`frame_type` 仅注明"粗粒度兼容别名，见 pipeline 映射表"。不要删除向后兼容说明。
- **验收**：全仓库只有一处定义分类法语义；image-prompts 不再独立定义 4 值体系，只引用。
- **不要**：改变配比检查的业务含义（scene_only 仍约占 1/3）。

### [x] T1.2 主流程顺序收敛为引用
- **目标**：主流程"步骤顺序"只在一处权威定义，其它引用。
- **权威处**：`ai-short-video-pipeline/references/workflow-state-machine.md`（Stage List + Allowed Transitions）。
- **改动点**：根 `SKILL.md` 的 `## Workflow`（15 步）、pipeline `SKILL.md` 的流程顺序、image-prompts 的 `LLM Meta-Prompt Mode` 末尾 9 步 —— 保留各自面向不同读者的"叙述"，但顺序事实改为"以 workflow-state-machine.md 为准"的引用句，且确保三处描述彼此不矛盾。
- **验收**：三处流程描述与状态机阶段一一对应，无顺序冲突。

### [x] T1.3 统一风格选择编号
- **目标**：消除「1=模板/2=自定义」与「1/2/3/4 + 0=自定义」并存。
- **统一方案**：`1/2/3/4 = 四个预设`，`0 = 自主设定风格`（与前台固定选项块一致）。
- **改动点**：`style-presets.md` 的 `## Usage Rule`(第 30-40 行附近) 与 `## Interaction Rule`(第 335-343 行附近) 统一为该方案；root SKILL.md / pipeline SKILL.md / image-prompts SKILL.md 中的风格选择话术对齐。
- **验收**：全仓库风格选择编号唯一。

> `[REVIEW Phase 1]` Codex 停。Claude 检查：流程语义未变、阶段列表唯一、分类法唯一、编号唯一。
>
> **Claude review 结论（2026-06-03）：T1.2/T1.3 通过；T1.1 基本通过，但有 1 个必修遗漏：**
> - **[FIX-1.1a] §3.6 残留旧词表**：`ai-short-video-pipeline/SKILL.md` 与 `MODULE.md` 的 §3.6「空间锁定卡的适用范围」仍使用已废弃的旧值 `scene_demo`/`concept_diagram`/`ui_interface`/`symbolic_insert`（不在权威 7 值集合内，已成悬空值）。改为 7 值规范名：
>   - 必须做真实空间锁定：`host_primary`、`host_with_visual`、`scene_only`（真实场景镜头）
>   - 默认不强制：`concept_explainer`、`ui_closeup`、`data_compare`、`brand_symbolic`
>   - 映射依据：scene_demo→scene_only，concept_diagram→concept_explainer，ui_interface→ui_closeup，symbolic_insert→brand_symbolic
> - FIX-1.1a 已完成并验证（§3.6 两文件均改为 7 值规范名，旧词表全仓库零残留）。**Phase 1 全部通过，已打本地 commit 存档点。可进入 Phase 2。**
> - 已确认的加分项（保留）：shot-planner 的 `frame_type`→`track_type` 改名；§3.2 词表统一到 §3.4。

---

## Phase 2 — 技能结构

### [x] T2.1 MODULE.md 瘦身为薄索引（12 模块）
- **目标**：消除 MODULE.md 与 SKILL.md 的整文件重复（当前 11/12 模块字节相同）。
- **改动点**：每个 `ai-*/MODULE.md` 改写为薄索引，模板：
  ```markdown
  # <模块名>（模块索引）
  > 本模块完整规则见同目录 [SKILL.md](./SKILL.md)。本文件只做角色定位与导航。
  ## 角色
  <一句话职责，取自 SKILL.md frontmatter description>
  ## 关键 references
  - [references/xxx.md](./references/xxx.md) — 用途
  ## 上下游
  上游：<谁给输入> / 下游：<交给谁>
  ```
- **保留**：根 SKILL.md 的 `Internal Modules` 链接仍指向 MODULE.md（现在是索引，链接有效）。
- **验收**：`diff MODULE.md SKILL.md` 不再相同；MODULE.md 均 < 40 行；无信息丢失（SKILL.md 仍是完整规则）。

### [x] T2.2 修复悬空引用 cyberpunk-template-01.md
- **现状**：`ai-video-image-prompts/MODULE.md` 与 `SKILL.md` 引用了不存在的 `references/cyberpunk-template-01.md`。
- **处理**：删除这两处引用，改为指向已存在的 `references/reusable-template-system.md`。
- **验收**：`grep -r cyberpunk-template-01` 无结果；无悬空 markdown 链接。

### [x] T2.3 校正根 SKILL.md 委派表
- **改动点**：root `SKILL.md` 的 `Delegation Rule` 与 pipeline `SKILL.md` 的 `Skill Map`，逐条核对模块名、职责与各模块 SKILL.md frontmatter 一致（注意 seedance 已停用、grok 为当前视频 provider 等现状）。
- **验收**：委派表 11/12 模块名称与职责与实际 SKILL.md 一致，无失效项。

> `[REVIEW Phase 2]` Codex 停。Claude 检查：无重复整文件、无悬空链接、委派表与实际一致。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - T2.1：12 个 MODULE.md 全部瘦身到 15–28 行、与 SKILL.md 不再相同（净删 3305 行）；SKILL.md 行数基本不变，规则完整保留；薄索引模板（角色/指向/references/上下游）齐全。
> - T2.2：`cyberpunk-template-01` 全仓库零引用，改指向 `reusable-template-system.md`。
> - 全仓库 markdown 相对链接断链检查：0 断链；根 SKILL.md 的 12 条 Internal Modules 链接全部有效。
> - T2.3：根委派表 + pipeline Skill Map 与各模块实际职责一致，grok 启用 / seedance 停用状态已标注。

---

## Phase 3 — 风格模板

### [x] T3.1 风格预设 SSOT 化
- **权威处**：`ai-video-image-prompts/references/style-presets.md`（4 预设，含结构化基因 JSON）。
- **改动点**：`ai-short-video-pipeline/references/prompt-generation-rules.md §3 风格参数表`：
  - 删除其中重复的 3 段基因 JSON。
  - 改为：保留"如何把 6 组基因转写进 prompt"的方法论；预设清单与基因值"以 style-presets.md 为准"的引用。
- **验收**：基因 JSON 全仓库只有一份（在 style-presets.md）；prompt-generation-rules 不再列举具体预设基因值。

### [x] T3.2 补齐第 4 预设的全仓库一致性
- **改动点**：所有列举风格预设处都包含 4 个（含「黑白素描概念讲解风」），无 3/4 不一致。
- **验收**：`grep` 风格名，四个预设在每个枚举点都齐全。

### [x] T3.3 templates/ 落地示例模板
- **新建**：`templates/cyber-host-template.json`，按 `templates/README.md` 描述的字段（主讲人锚点、风格摘要=引用 style-presets 的 key、提示词规则、负面约束、默认比例、默认模型、用户选定样例占位）。与 Phase 5 demo 配套（同一主讲人/风格）。
- **验收**：JSON 合法；字段与 README 约定一致；风格字段引用 style-presets 的 `style_key` 而非复制整段。

> `[REVIEW Phase 3]` Claude 检查：预设数量/命名/编号一致、基因 JSON 单份、示例模板合规。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - T3.1：prompt-generation-rules.md 预设基因 JSON 清零；style-gene-structure.md 为纯 schema（无预设硬编码值）；基因块仅 style-presets.md 一份(4个)。
> - T3.2：四预设在所有枚举点齐全，无只列 3 个的残留。
> - T3.3：cyber-host-template.json 合法，用 style_key 引用而非复制基因；字段对齐 README；默认值 GPT-Image-2/grok/16:9 与 SSOT 一致。

---

## Phase 4 — 视频提示词

### [x] T4.1 新建 MODELS.md（模型 SSOT）
- **新建**根目录 `MODELS.md`，含三张表：生图模型、图生视频模型、数字人/语音模型。每行：规范名 / 用户可见(是·否) / 用途 / 对应脚本 / 别名收敛。
- **基线事实**（以现状为准，Codex 核对脚本后填写）：
  - 生图：`GPT-Image-2`(用户可见)、`nanobanana-2`(用户可见)、`nanobanana-pro`(实现层)、`seedream-5.0`(实现层，脚本 seedream5_batch.py)。
  - 图生视频：`grok`(当前启用)、`doubao-seedance-1.0-pro-fast`(seedance 当前停用，标注)。
  - 数字人/语音：即梦 OmniHuman 1.5、蝉镜数字人、速创 Digital_Humans / 速创 TTS / 速创语音克隆。
- **验收**：MODELS.md 覆盖所有出现过的模型名并给出规范写法。

### [x] T4.2 全仓库模型名规范化
- **改动点**：按 MODELS.md 规范写法统一所有 .md 与脚本常量；消除 `Seedream-5.0-lite`/`Seedream 4.6` 等孤立写法（除非确为不同模型——若是，必须进 MODELS.md 表）。
- **验收**：`grep -rhoE` 模型名集合 = MODELS.md 规范集合，无孤立写法。

### [x] T4.3 dev 笔记迁出 operational reference
- **新建** `CHANGELOG.md`，迁入：`prompt-generation-rules.md` 的「核心认知(2026-05-06)」「昨天 RALV 项目复盘」表、「构图多样性强制约束(2026-05-08)」的问题背景叙述（**保留规则本体，移走 dev 叙事与日期复盘**）。
- **验收**：reference 文件只剩当前生效规则；被移走内容在 CHANGELOG 可追溯。

> `[REVIEW Phase 4]` Claude 检查：模型名唯一规范、提示词规则与 SSOT 对齐、reference 无 dev log。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - T4.1：MODELS.md 三张表覆盖全部模型名与别名收敛(含 veo 历史 provider)。
> - T4.2：正文零孤立写法(Seedream-5.0-lite/4.6 仅留在 MODELS 别名列与 CHANGELOG)；脚本将规范显示名与真实 API ID 正确分离(seedream/grok)，gpt_image2 仅改元数据标签不影响调用(payload 无 model 字段)；3 脚本 py_compile 通过。
> - T4.3：CHANGELOG 迁入 2026-05-06 核心认知 / 2026-05-08 构图多样性背景 / RALV 复盘；规则本体(硬结构/三层分工/构图多样性约束)原样保留。

---

## Phase 5 — 最小可跑样例（demo）

### [x] T5.1 准备样例文案
- **新建** `examples/demo-ai-popsci/00-source-script.md`：一段 ~45s（中文约 170 字）AI 科普口播文案，含钩子/解释/对比/CTA 结构，便于触发完整流程但规模小。

### [x] T5.2 逐阶段产出静态产物（不调 API）
- 按重构后流程产出：`01-shot-plan.md`（时长+镜头数估算+信息单元表+visual_carrier 分配+配比检查）、`02-style-selection.md`（引用某个 style-presets 预设 key + 比例 + 模型）、`03-subjects-and-three-views.md`（重复主体清单 + 每主体三视图提示词）、`04-image-prompts.md`（6~8 条按硬结构拼装的正式图片提示词，每条含 shot_id/原文片段/中文说明/英文 prompt/负面约束）、`05-image-to-video-prompts.md`（对应图生视频动作提示词）、`06-delivery-package.md`（交付包汇总）。
- 图片/视频本体用"提示词 + [占位：此处为生成图/视频]"呈现。
- **验收**：每个产物引用的是重构后的 SSOT（风格 key、模型名、visual_carrier）；前后阶段数据一致（同一主讲人、同一风格、shot_id 贯通）。

### [x] T5.3 末态状态机快照
- **新建** `examples/demo-ai-popsci/project-state.json`：基于 `ai-short-video-pipeline/references/project-state-template.json` 结构，填到 `videos_generated`/`completed` 附近的合理末态，字段与状态机阶段一致。
- **验收**：JSON 合法、阶段值在 workflow-state-machine 的 Stage List 内。

### [x] T5.4 README 增加 demo 入口
- **改动点**：`README.md` 新增"看一个完整样例"小节，链接 `examples/demo-ai-popsci/`。
- **验收**：链接有效。

> `[REVIEW Phase 5]` Claude 检查：demo 端到端完整、每步对齐 SSOT、可作为对外 showcase。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。第一轮重构完成。**
> - 8 个产物齐全(00-06 + project-state.json)，README 入口有效。
> - 自动校验：7 个 shot_id 的 visual_carrier 在 分镜表/图片提示词/图生视频 三处完全一致，全部属 7 值规范集。
> - SSOT 引用处处正确：style_key=cyberpunk_bright_hud_infographic、模型=GPT-Image-2/grok、主讲人 host_cyber_female_01 全程贯通；project-state current_stage=completed 在 Stage List 内。
> - 软性观察(留作下轮打磨，不卡通过)：shot_05 brand_symbolic 语义略偏(实为泛化工具符号)；scene_only 占 1/7 低于约 1/3 默认(已文档化为 7 镜 demo 例外)。

---

## Round 2 — 扩充风格预设库

> 目标：新增第 5 个正式风格预设「复古纸质拼贴风」。**强约束**：第一轮已把风格选择编号统一为 `1-4 预设 + 0 自定义`，本轮新增后必须同步**所有枚举点**为 `1-5 预设 + 0 自定义`，否则会破坏已建立的一致性。基因 JSON 仍只许存在于 `style-presets.md`（SSOT）。

### [x] R2.1 在 style-presets.md 新增预设 5「复古纸质拼贴风」
- **唯一落点**：`ai-video-image-prompts/references/style-presets.md`，新增 `### 5. 复古纸质拼贴风`，格式严格对齐现有 4 个预设（用户侧一句话说明 + 各 default 倾向 bullet + 完整 `visual_style` JSON）。
- **预设规格（按此插入，可微调措辞但不改语义）**：
  - 预设名：`复古纸质拼贴风`
  - 英文标识 / style_key：`vintage_paper_collage`
  - 用户侧一句话：`复古纸质拼贴、剪纸人物、旧报纸纹理与胶带印章元素、红棕色档案室氛围、纪录片分镜感，适合历史复盘、调查叙事和案例拆解`
  - 默认人物渲染方式：`剪纸拼贴插画人物，非写实真人`
  - 推荐文字容器语言：`手写便签、打字机字条、档案标签、印章戳记、报纸标题剪贴（仍遵守无可读长文字，仅作纹理）`
  - 完整基因 JSON 已迁入 `ai-video-image-prompts/references/style-presets.md`，任务卡不再保留副本，避免破坏 SSOT。
  - 默认负面约束建议：`避免高光 3D 渲染、避免霓虹赛博色、避免干净数字 HUD、避免现代扁平矢量、避免写实电影照片感、避免纯白或纯黑背景（用做旧纸色）、避免可读长文字与段落、保留胶带/印章/纸纹做旧作为特征而非瑕疵`
- **验收**：style-presets.md 有 5 个 `style_key` 块；新预设 JSON 字段结构与前 4 个一致；基因 JSON 未出现在其它文件。

### [x] R2.2 全仓库枚举点同步为 5 预设 + 编号 1-5/0
- **改动点**（逐一核对，先 grep 现有 4 预设枚举处再补第 5 个）：
  - `style-presets.md`：顶部 `Usage Rule` 选项列表、底部 `Interaction Rule` 选项列表 → 加 `复古纸质拼贴风 请输入 5`，自定义保持 `0`。
  - `ai-video-image-prompts/SKILL.md` 与 `MODULE.md`：前台固定选项块（风格 1-4 → 1-5）、"如果用户输入 `1`、`2`、`3` 或 `4`" → 含 `5`。
  - `ai-short-video-pipeline/SKILL.md`：Intake 里的风格选项清单（`...请输入 1..4` + `自主设定风格请输入 0`）、"模板加载" 段落里"当前可选/当前可用模板"的 4 个名字 → 补第 5 个。
  - `ai-short-video-pipeline/references/user-guidance-templates.md`：风格选项块（5 行 → 6 行）。
  - `ai-short-video-pipeline/references/workflow-state-machine.md`：Ambiguous Reply Rule "在风格阶段 `1`/`2`/`3`/`4` = 四个风格预设" → "1-5 = 五个风格预设"。
  - `SOP-如何使用知行视频skill.md`：风格选项块补第 5 个。
- **验收**：`grep "复古纸质拼贴风"` 在以上每个枚举点都出现；全仓库再无"只列 4 个预设"的风格选择块；编号方案唯一为 `1-5 + 0`。

> `[REVIEW Round 2]` Codex 停。Claude 检查：基因 JSON 单份且结构对齐、所有枚举点齐 5 预设、编号唯一 1-5/0、无断链。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - R2.1：style-presets.md 现有 5 个 style_key 块，新预设 vintage_paper_collage 结构与前 4 个一致；5 个 JSON 块全部合法；基因 JSON 仅此一处。
> - R2.2：前台块/Usage/Interaction/pipeline Intake/user-guidance/状态机/SOP 所有枚举点均补齐第 5 个；编号唯一 1-5+0；image-prompts/MODULE.md 为薄索引不枚举风格(正确)；无真实断链。

---

## Round 3 — 扩充风格预设库（第 6 预设）

> 目标：新增第 6 个正式风格预设「羊毛毡定格动画风」。**强约束**：编号从 `1-5 + 0` 扩为 `1-6 + 0`，必须同步**所有枚举点**（同 Round 2 列表）。基因 JSON 仍只许在 `style-presets.md`。
> **架构注意**：画幅 9:16 是项目级独立参数，**不锁进基因 JSON**，只在用户侧一句话里写"推荐画幅 9:16"；8K 归入 `resolution_feel`。

### [x] R3.1 在 style-presets.md 新增预设 6「羊毛毡定格动画风」
- **唯一落点**：`ai-video-image-prompts/references/style-presets.md`，新增 `### 6. 羊毛毡定格动画风`，格式严格对齐现有预设。
- **预设规格（按此插入，可微调措辞不改语义）**：
  - 预设名：`羊毛毡定格动画风`
  - 英文标识 / style_key：`wool_felt_stop_motion`
  - 用户侧一句话：`羊毛毡定格动画质感、黏土手工感、毛茸茸针脚纹理、皮克斯式 3D 卡通、柔光电影级渲染，商务氛围；推荐画幅 9:16`
  - 默认人物渲染方式：`毡偶 / 黏土风格化角色，皮克斯式 3D，非写实真人`
  - 推荐文字容器语言：`手作毡布标签、纸牌道具、软质标牌（仍遵守无可读长文字，仅作纹理）`
  - 完整基因 JSON 已迁入 `ai-video-image-prompts/references/style-presets.md`，任务卡不再保留副本，避免破坏 SSOT。
  - 默认负面约束建议：`避免写实真人照片、避免冷硬赛博霓虹、避免扁平 2D 矢量、避免廉价塑料光泽、避免锐利数字 HUD、避免可读长文字与段落、保留羊毛纤维/针脚/手工不完美作为特征而非瑕疵`
- **验收**：style-presets.md 有 6 个 `style_key` 块且结构一致；JSON 全部合法；基因 JSON 未出现在其它文件；画幅未被写进 JSON 字段。

### [x] R3.2 全仓库枚举点同步为 6 预设 + 编号 1-6/0
- **改动点**：同 Round 2 R2.2 的全部枚举点（style-presets Usage/Interaction、image-prompts SKILL 前台块、pipeline SKILL Intake 与模板加载段、user-guidance-templates、workflow-state-machine 的 Ambiguous Reply Rule、SOP），把 `复古纸质拼贴风 请输入 5` 之后补 `羊毛毡定格动画风 请输入 6`，编号方案改为 `1-6 + 0`。
- **验收**：`grep "羊毛毡定格动画风"` 在每个枚举点都出现；无"只列到 5"的残留；编号唯一 `1-6 + 0`。

> `[REVIEW Round 3]` Codex 停。Claude 检查：基因 JSON 单份且结构对齐、画幅未入基因、所有枚举点齐 6 预设、编号唯一 1-6/0、无断链。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - R3.1：style-presets.md 现 6 个 style_key 块，新预设 wool_felt_stop_motion 结构对齐；6 个 JSON 全合法；基因 JSON 仅此一处；无独立 aspect_ratio 字段(9:16 仅作 camera_language 描述，同现有预设惯例)。
> - R3.2：所有枚举点补齐第 6 个，前台块编号 1-6+0，无'只列到 5'残留，无断链。

---

## Round 4 — 删除「3D科技讲解风」预设

> 目标：删除预设「3D科技讲解风」(`3d_tech_explainer`)，预设库从 6 → 5。**强约束**：删除后重新编号为 `1-5 + 0`，保持其余预设相对顺序（原 4/5/6 上移为 3/4/5），所有枚举点同步，不留编号空洞。基因 JSON 仍只在 `style-presets.md`。
> 已确认：demo 与 templates 未引用该预设，删除不影响样例。

**重排后目标编号：**
- 1 AI科普赛博明亮HUD风
- 2 手绘水彩教学风
- 3 黑白素描概念讲解风（原 4）
- 4 复古纸质拼贴风（原 5）
- 5 羊毛毡定格动画风（原 6）
- 0 自主设定风格

### [x] R4.1 删除 style-presets.md 中的预设块与列举
- `ai-video-image-prompts/references/style-presets.md`：
  - 删除整个 `### 3. 3D科技讲解风` 段落（含一句话说明、各 default bullet、`3d_tech_explainer` 基因 JSON、负面约束）。
  - 把原 `### 4./5./6.` 重新编号为 `### 3./4./5.`。
  - 顶部 `Usage Rule` 列表与底部 `Interaction Rule` 列表删除 `3D科技讲解风 请输入 3`，其余项重排为 `1-5 + 0`。
- **验收**：style-presets.md 剩 5 个 `style_key` 块，section 编号连续 `### 1.`～`### 5.`，5 个 JSON 全合法，无 `3d_tech_explainer` 残留。

### [x] R4.2 全仓库枚举点删除 + 重排为 1-5/0
- 逐一处理以下点（删除该项并把后续编号上移）：
  - `ai-video-image-prompts/SKILL.md`：两处前台/选项块（约 line 175、202 区域）删 `3 3D科技讲解风`，4/5/6 → 3/4/5。
  - `ai-short-video-pipeline/SKILL.md`：Intake 选项清单（约 line 390 `3D科技讲解风 请输入 3 - ...` 整行删除并重排）；"模板加载"段（约 line 413）的内联"当前可选"名单删除「3D科技讲解风」。
  - `ai-short-video-pipeline/references/user-guidance-templates.md`（约 line 38）删 `3 3D科技讲解风` 并重排。
  - `ai-short-video-pipeline/references/prompt-generation-rules.md`（约 line 17）内联名单删除 `3D科技讲解风`（此处仅名字、无编号）。
  - `SOP-如何使用知行视频skill.md`（约 line 158）删 `3 3D科技讲解风` 并重排。
  - `ai-video-image-prompts/references/reusable-template-system.md`（约 line 41）示例命名 `3D科技讲解风模板01` 改为某个保留预设（如 `复古纸质拼贴风模板01`），不要留已删预设。
- **验收**：`grep -rn "3D科技讲解风\|3d_tech_explainer"`（排除 OPTIMIZATION_PLAN/TASKS/CHANGELOG）零结果；所有风格选择块编号为连续 `1-5 + 0`，无空号、无 `请输入 6`；无断链。

> `[REVIEW Round 4]` Codex 停。Claude 检查：预设块已删且 section 重排连续、基因 JSON 单份且 5 块合法、所有枚举点重排为 1-5/0 无残留无空号、无断链。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - R4.1：3D科技讲解风/3d_tech_explainer 全仓库零残留；style-presets.md 剩 5 个 style_key，section 重排连续 ###1-5，5 JSON 合法。
> - R4.2：所有枚举点重排为 1-5+0，无空号、无'请输入6'残留；reusable-template-system 示例命名已更新为保留预设；无断链。

---

## Round 5 — 优化图生视频提示词

> 目标：闭合"分镜→视频"的词表断层、SSOT 去重、修 grok 冲突、按风格差异化运动，并把用户实测验证过的中文动作提示词正式沉淀。
> **SSOT 决策**：
> - 图生视频 **规则** 唯一权威 = `ai-video-generate-videos/references/image-to-video-prompt-rules.md`（motion_type 定义、motion_intensity、安全/稳定约束、映射表）。
> - 图生视频 **模板/样板** 唯一权威 = `ai-video-generate-videos/references/motion-template-library.md`（含已验证中文提示词库）。
> - `ai-video-motion-prompts/SKILL.md` 与 `references/motion-design-rules.md` 不再各自重复定义，改为引用上述两处；motion-design-rules 仅保留它独有的"镜头方向预设 + 人物/场景方向规则 + 风险等级"。

### [x] R5.1 沉淀已验证动作提示词库（11 条，用户实测流畅）
- **落点**：`motion-template-library.md` 新增章节「已验证动作提示词库（中文 · grok 实测流畅）」。
- **要求**：以下 11 条**逐字保留**，每条加标签行 `visual_carrier / motion_type / motion_intensity / camera`。语言保持中文（已实测可用，不要翻译成英文替换原文，可在条目下附英文等价版供英文 provider）。
  1. `主讲人轻微点头，眼神稳定看镜头，肩膀有细微呼吸感，镜头轻微推近，保持人物发型、服装、肤色完全不变，画面风格稳定，不要新增角色，不要闪烁。` — host_primary / 讲述型 / low / 推近
  2. `数据流动轻微闪烁，画面缓慢横移，展示AI内容泛滥的场景，保持场景结构稳定，风格不变。` — scene_only / 场景型 / low / 横移
  3. `主讲人轻微抬手强调，点头幅度稍明显，眼神坚定，镜头轻微推近，保持人物外观完全不变。` — host_primary / 讲述型 / medium / 推近
  4. `AI工具界面轻微动效，按钮有极小幅动画，镜头缓慢横移，保持场景稳定。` — ui_closeup / 展示型 / low / 横移
  5. `主讲人表情严肃，眼神略显忧虑，头部轻微下沉，镜头轻微推近，保持人物外观不变。` — host_primary / 情绪型 / low / 推近
  6. `极简画面缓慢淡出淡入，镜头缓慢后拉，展示大面积留白，保持风格稳定。` — scene_only / 场景型 / low / 后拉
  7. `画面轻微呼吸感，色温保持稳定，镜头缓慢推近，展示电影质感，保持风格不变。` — scene_only / 情绪型 / low / 推近
  8. `主讲人伸手与界面互动，手指轻微动效，镜头轻微推近，保持人物外观完全不变。` — host_with_visual / 展示型 / medium / 推近
  9. `对比画面缓慢切换，镜头轻微环绕感，保持场景稳定，风格不变。` — data_compare / 冲突型 / medium / 环绕
  10. `主讲人自信表情，轻微点头，眼神坚定，镜头轻微推近，保持人物外观完全不变。` — host_primary / 讲述型 / low / 推近
  11. `主讲人微笑看镜头，自然站姿，胳膊自然下垂，肩膀放松，镜头轻微推近，保持人物外观完全不变。` — host_primary / 讲述型 / low / 推近
- **验收**：11 条逐字在库中；每条都有标签行；章节注明"实测可用、可直接套用"。

### [x] R5.2 建立 visual_carrier → motion_type → 模板 映射表（SSOT）
- **落点**：`image-to-video-prompt-rules.md` 新增「visual_carrier 运动映射表」。
- **内容**：7 个 visual_carrier 各给出：推荐 motion_type、默认 motion_intensity、推荐 camera、对应模板/已验证提示词编号。建议：
  - host_primary→讲述型/low/推近·横移（验证 1,3,5,10,11）
  - host_with_visual→展示型/low-medium/推近（验证 8）
  - scene_only→场景型/low/横移·后拉·推近（验证 2,6,7）
  - concept_explainer→展示型/low/横移·推近
  - data_compare→冲突型(对比)/medium/轻微环绕·横移（验证 9）
  - ui_closeup→展示型/low/横移·推近（验证 4）
  - brand_symbolic→展示型/low/横移·推近
- **验收**：7 个 visual_carrier 全覆盖；映射引用 R5.1 的已验证编号；`motion-template-library.md` §8 旧"中文映射"键改为对齐 visual_carrier 或指向本表，不再是第三套词表。

### [x] R5.3 SSOT 去重 + 补全镜头预设
- 稳定性约束：以 `image-to-video-prompt-rules.md §5 Default Safe Rules` 为唯一权威；`motion-prompts/SKILL.md` 的「Default Stability Preset」与 `motion-design-rules.md §5` 改为引用（keyframe 收紧版只在一处保留）。
- motion_intensity：以 `image-to-video-prompt-rules.md §4` 为唯一权威；motion-prompts SKILL 改引用。
- motion_type 定义：以 `image-to-video-prompt-rules.md §3` 为唯一权威；motion-prompts SKILL「Default Motion Types」改引用。
- **补缺口**：`motion-design-rules.md §2 固定镜头预设` 增加 `缓慢推近(push-in)` 与 `轻微环绕(slight orbit，仅用于对比/冲突镜头)`——因为模板与已验证提示词大量使用，但原 §2 缺失。
- 语言规则：`image-to-video-prompt-rules.md §6` 改为"语言随 provider；grok/速创实测中文可用，英文 provider 用英文等价版"，不要一刀切要求英文。
- **验收**：稳定性/强度/类型在仓库中各只有一处定义，其余为引用；§2 含推近与环绕；§6 不再硬性要求英文。

### [x] R5.4 修 grok 模板与人物镜头规则的冲突
- `grok-video-template-00.md` 的 `grok视频模版套用00` 默认"镜头上移+后拉"与 `motion-design-rules §3`（人物镜头避免上下移动）冲突。
- **处理**：把该模板默认相机运动改为人物安全方向（后拉 / 轻微横移 / 轻微推近）；"上移"仅在注释里标明"仅用于纯场景竖向空间镜头，人物镜头不用"。
- **验收**：grok 模板默认不再对人物镜头用上移；与 motion-design-rules §3 口径一致。

### [x] R5.5 按风格差异化运动适配
- **落点**：`image-to-video-prompt-rules.md` 新增「风格运动适配」section，对 style-presets 的 5 个 `style_key` 各给一句运动基调指引，例如：
  - cyberpunk_bright_hud_infographic：数据流光/面板微动 + 推近·横移
  - hand_painted_watercolor_educational：极简、淡入淡出、几乎静止，轻后拉
  - monochrome_sketch_concept_explainer：静帧感、极轻推近，避免明显动画
  - vintage_paper_collage：纸片层移/定格顿挫感、轻横移
  - wool_felt_stop_motion：定格动画顿挫节奏、缓慢推近、电影柔光呼吸感
- **验收**：5 个 style_key 全覆盖；引用 style-presets 的 key，不复制基因。

> `[REVIEW Round 5]` Codex 停。Claude 检查：11 条逐字保留且打标签、visual_carrier 映射表 7 值全覆盖且消除第三套词表、稳定性/强度/类型各单份、§2 含推近·环绕、grok 冲突已修、5 风格运动适配齐全、无断链。
>
> **Claude review 结论（2026-06-03）：全部通过，已打本地 commit 存档点。**
> - R5.1：11 条实测中文提示词逐字保留于 motion-template-library，每条带 visual_carrier/motion_type/intensity/camera 标签。
> - R5.2：image-to-video-prompt-rules 新增 visual_carrier 运动映射表(7 值全覆盖, 引用已验证编号); 模板库 §8 旧第三词表(主讲人出镜等)已删, 改为指向该映射表。
> - R5.3：稳定性(§5 Default Safe Rules)/intensity(§4)/motion_type(§3) 各唯一权威, motion-design-rules 与 motion-prompts SKILL 改引用; §2 补 推近+环绕; §6 语言改为随 provider(中文实测可用)。
> - R5.4：grok 模版00 默认改人物安全方向(后拉/横移/推近), 上移仅标注纯场景竖向。
> - R5.5：5 个 style_key 运动适配齐全; 无断链。

---

## Round 6 — 新增图生视频模型 omni（用户可选）

> 目标：把 `omni` 接成与 `grok` 并列、用户可选的图生视频模型。grok 仍为 auto 默认，omni 仅在用户显式选择时使用。
> **已核实事实（来自官方 Apifox 文档，勿编造其它字段）**：
> - 规范名 `omni`，**API model ID = `omni_flash-v2v`**。
> - 接口 `POST https://api.yijiarj.cn/v1/videos`（异步），轮询 `GET /v1/videos/{id}`；鉴权 `Authorization: Bearer ${YIJIA_API_KEY}`。
> - 参数：`prompt`(必填) / `model`(必填) / `size`(WxH，如 `1920x1080`/`720x720`/`1024x1024`) / `input_reference`(可选，**可传首尾帧，多图用 `|` 分隔**；omni 额外支持**视频参考 v2v**) / `remix_id`(可选)。
> - **无 duration 参数**。同 endpoint 另有 veo 系列(`veo_3_1-fast`/`-fast-fl`/`-4K`)，属同族实现层。
> - 与现有 `video_generation_router.py` 的 `submit_veo`/`poll_veo`(POST `/v1/videos` + GET `/v1/videos/{id}`) **完全同形**，复用即可。

### [x] R6.1 MODELS.md 登记 omni
- 图生视频模型表新增一行：`omni` / 用户可见=是 / 用途=图生视频，支持首尾帧(多图 `|` 分隔)与视频参考(v2v) / 脚本 `video_generation_router.py` / 别名收敛 `omni_flash-v2v`。
- veo 行补注：`veo_3_1-fast`/`-fast-fl`/`-4K` 为同 `/v1/videos` endpoint 的实现层变体。
- **验收**：omni 在表中且标用户可见；API model ID `omni_flash-v2v` 写明；endpoint 与鉴权准确。

### [x] R6.2 新增 omni-provider-notes.md
- 新建 `ai-video-generate-videos/references/omni-provider-notes.md`：endpoint、鉴权、参数(prompt/model=`omni_flash-v2v`/size WxH/input_reference 首尾帧或视频参考用 `|` 分隔/可选 remix_id)、异步 status+progress、轮询 `GET /v1/videos/{id}`、size 示例、无 duration；并写"与 grok 的区别：omni 支持首尾帧与视频参考"。
- **验收**：仅含文档已给出的字段，不编造私有参数；与 grok-provider-notes.md 风格一致。

### [x] R6.3 router 接入 omni
- `video_generation_router.py` 新增 provider `omni`，复用 `/v1/videos` create+poll（与 veo 同形）：
  - `provider_has_credentials("omni")` → `YIJIA_API_KEY`
  - `default_model_for_provider("omni")` → `omni_flash-v2v`
  - `submit_item`/`poll_item`/`status_is_terminal`/`extract_render_url` 增加 omni 分支，走 `submit_veo`/`poll_veo` 形态（`input_reference` 取 `source_image_url`，支持 `|` 首尾帧）。
- grok 仍为 `choose_auto_provider` 默认；omni 仅在 `item.provider == "omni"` 显式指定时启用。不破坏 grok/seedance 现有逻辑。
- **验收**：`python3 -m py_compile` 通过；omni 队列项能构造出正确 payload(model=`omni_flash-v2v`)；grok 路径不受影响。

### [x] R6.4 用户可选视频模型（grok / omni）
- 在「图生视频模式」入口增加用户可选模型：`图生视频模型：1 grok（默认）/ 2 omni（支持首尾帧、视频参考）`。
- 涉及：`ai-short-video-pipeline/SKILL.md`（Two-Track / 图生视频模式段）、`ai-video-generate-videos/SKILL.md`、必要时 `image-to-video-prompt-rules.md`。保持对外简洁，omni 作为并列可选项，默认仍 grok。
- **验收**：用户可选 grok 或 omni；默认仍 grok；omni 差异能力有一句说明；选择编号清晰。

### [x] R6.5 provider-queue-example.json 补 omni 示例
- 在 `ai-video-generate-videos/references/provider-queue-example.json` 增加一个 `provider: "omni"` 的示例条目（含 shot_id/source_image_url/motion_prompt/size，演示首尾帧 `|` 用法），JSON 合法。
- **验收**：JSON 合法；omni 示例字段与 router 期望一致。

> `[REVIEW Round 6]` Codex 停。Claude 检查：MODELS.md 登记准确(omni_flash-v2v)、notes 不编造字段、router omni 分支正确且 py_compile 通过且不破坏 grok、用户可选 grok/omni 默认 grok、示例 JSON 合法、无断链。
>
> **Claude review 结论（2026-06-04）：全部通过，已打本地 commit 存档点。**
> - R6.1/R6.2：MODELS.md 与 omni-provider-notes.md 准确写明 model ID omni_flash-v2v、POST /v1/videos 创建 + GET /v1/videos/{id} 轮询、YIJIA_API_KEY、首尾帧(|)与视频参考(v2v)；无编造字段。
> - R6.3：router 新增 omni 分支复用 submit_veo/poll_veo(/v1/videos 同形)，credentials/default-model(omni_flash-v2v)/terminal/render-url 齐全；choose_auto_provider 仍 grok-first，omni 仅显式启用，grok 失败不回退 omni；py_compile 通过。
> - R6.4：pipeline/generate-videos SKILL 与 user-guidance 提供 1 grok(默认)/2 omni(首尾帧·视频参考)，唤醒词与工具链描述同步。
> - R6.5：provider-queue-example.json 含合法 omni 条目，4 必填字段齐全；无断链。

---

## 执行须知（给 Codex）
1. 一次只推进一个 Phase，做完停下，输出"改了哪些文件 + 如何自检"的简报。
2. 任何与 OPTIMIZATION_PLAN §2 原则冲突的地方，停下提问，不要自行决定破坏对外行为。
3. 重构以"去重 + 引用 + 对齐"为主，不要重写业务规则语义。
4. 每个任务完成后在本文件把 `[ ]` 改为 `[~]`；review 通过由 Claude 改为 `[x]`。
