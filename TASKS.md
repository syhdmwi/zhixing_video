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

## 执行须知（给 Codex）
1. 一次只推进一个 Phase，做完停下，输出"改了哪些文件 + 如何自检"的简报。
2. 任何与 OPTIMIZATION_PLAN §2 原则冲突的地方，停下提问，不要自行决定破坏对外行为。
3. 重构以"去重 + 引用 + 对齐"为主，不要重写业务规则语义。
4. 每个任务完成后在本文件把 `[ ]` 改为 `[~]`；review 通过由 Claude 改为 `[x]`。
