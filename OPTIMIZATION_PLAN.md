# 知行视频 Skill 优化方案（总纲）

> 本文件是优化工作的**架构总纲**，由 Claude 负责维护。
> 具体可执行任务见 [TASKS.md](./TASKS.md)，由 Codex 按任务卡执行。
> 协作模式：Claude 定架构 + 事后 review；Codex 读仓库 + 本方案直接执行。
> 创建日期：2026-06-03

---

## 1. 现状判断

`zhixing_video` 是一套成熟度很高的「AI 短视频生产」Skill 套件：

- 对外单入口（根 `SKILL.md`），内部 12 个模块化 skill。
- 规则写得很细：状态机、三层提示词汇合、风格基因、质量审核回环、模式判断都有。

但存在三类系统性欠账，本轮优化全部针对它们：

1. **一致性欠账**：同一事实在多处重复定义且已经开始漂移（风格预设、模型命名、分类法、MODULE/SKILL 双份）。
2. **工程化欠账**：缺少「单一事实来源（SSOT）」约定，改一处要同步多处，容易漏。
3. **可感知欠账**：没有任何端到端样例，新用户/协作者无法在 30 秒内看懂"这套东西到底产出什么"。

### 1.1 已确认的硬问题（带证据）

| # | 问题 | 证据 | 命中维度 |
|---|------|------|---------|
| 1 | MODULE.md 与 SKILL.md 整文件重复 | 11/12 模块 `diff MODULE.md SKILL.md` = 0 字节相同；image-prompts 已 drift 2 行 | 技能结构 |
| 2 | 风格预设数量不一致 | `style-presets.md` 4 个，`prompt-generation-rules.md §3` 3 个（缺黑白素描），且重复维护整段基因 JSON | 风格模板 |
| 3 | 风格选择编号自相矛盾 | `style-presets.md` 内既有「1=模板/2=自定义」又有「1/2/3/4 + 0=自定义」 | 步骤/流程、风格模板 |
| 4 | 悬空引用 | MODULE.md/SKILL.md 引用不存在的 `cyberpunk-template-01.md` | 技能结构 |
| 5 | 生图模型命名散落矛盾 | 文档散布 GPT-Image-2 / nanobanana-2 / nanobanana-pro / seedream-5.0 / Seedream-5.0-lite / Seedream 4.6 等 5+ 写法，用户层只暴露 2 个 | 视频提示词、技能结构 |
| 6 | frame_type vs visual_carrier 双分类法并存 | 旧 4 值 / 新 7 值两套，image-prompts 用旧、pipeline 用新 | 步骤/流程、视频提示词 |
| 7 | 陈旧开发笔记混入操作规则 | "RALV 项目复盘""核心认知(2026-05-06)"等 dev log 留在 reference | 视频提示词 |
| 8 | 零端到端样例 + `templates/` 空壳 | 无任何跑通样例产物 | demo |

---

## 2. 架构原则（本轮优化的"宪法"）

所有改动必须服从以下原则，Codex 执行时如与单个任务卡冲突，以本节为准：

1. **SSOT 单一事实来源**：每一类事实只允许有一个权威定义处，其它地方一律"引用"而非"复制"。
   - 风格预设 → `ai-video-image-prompts/references/style-presets.md`
   - 生图/视频模型清单 → 新建 `MODELS.md`（根目录）
   - 镜头分类法 → `visual_carrier`（pipeline 内定义）为唯一权威
   - 主流程状态机 → `ai-short-video-pipeline/references/workflow-state-machine.md`
2. **SKILL.md 为模块唯一规则载体**，MODULE.md 降级为"薄索引"（角色一句话 + 指向 SKILL.md + 关键 references）。
3. **用户层与实现层分离**：用户只看到收敛后的选项（2 个生图模型、5 个风格入口）；实现层可支持更多，但必须在 `MODELS.md` 标注"用户可见/仅实现层"。
4. **不破坏现有对外行为**：根 `SKILL.md` 的唤醒词、四个入口、状态机阶段语义保持不变。重构是"去重 + 对齐"，不是改交互。
5. **开发笔记与操作规则分离**：带日期的复盘/discovery 笔记移到 `CHANGELOG.md` 或 `dev-notes/`，operational reference 只保留当前生效规则。
6. **样例不依赖真实 API**：demo 用静态产物（markdown + JSON 状态文件）呈现完整链路，先证明"流程对"，真实跑批留待后续。

---

## 3. 目标结构（重构后）

```
zhixing_video/
├── SKILL.md                      # 对外唯一入口（保持）
├── README.md                     # 精简：指向 MODELS / examples / 各说明文档
├── MODELS.md                     # 【新】模型清单 SSOT（用户可见 + 实现层）
├── CHANGELOG.md                  # 【新】收纳被移出的 dev 复盘笔记
├── OPTIMIZATION_PLAN.md          # 本文件
├── TASKS.md                      # Codex 任务卡
├── 3分钟快速开始.md / 用户使用说明.md / 跨工具使用说明.md / SOP / SHARE_POST_TEMPLATE  # 保持，仅做一致性校正
├── examples/                     # 【新】端到端最小样例（demo 核心）
│   └── demo-ai-popsci/
│       ├── 00-source-script.md           # 原始文案（~45s AI 科普）
│       ├── 01-shot-plan.md               # 时长/镜头数/信息单元/visual_carrier
│       ├── 02-style-selection.md         # 选风格(引用 style-presets)+比例+模型
│       ├── 03-subjects-and-three-views.md# 重复主体清单 + 三视图提示词
│       ├── 04-image-prompts.md           # 6~8 条正式图片提示词（硬结构）
│       ├── 05-image-to-video-prompts.md  # 对应图生视频动作提示词
│       ├── 06-delivery-package.md         # 交付包汇总
│       └── project-state.json            # 跑到末态的状态机快照
├── templates/                    # 从空壳 → 放 1 个真实可复用模板样例
│   ├── README.md                 # 保持
│   └── cyber-host-template.json  # 【新】与 demo 配套的示例模板
└── ai-*/                         # 12 模块：MODULE.md 瘦身为索引，SKILL.md 为规则载体
```

---

## 4. 五个阶段（按首轮优先级）

> 顺序即执行顺序。每阶段末尾有 `[REVIEW]` 检查点，Codex 完成后停下，由 Claude review 通过再进下一阶段。

### Phase 1 — 步骤 / 流程（先做）
- 统一镜头分类法到 `visual_carrier`，把 `frame_type` 降级为"粗粒度兼容别名"并给出唯一映射表。
- 主流程状态机以 `workflow-state-machine.md` 为唯一权威；根 SKILL.md / pipeline SKILL.md / image-prompts 里的"流程顺序"段落改为引用，不再各写一份顺序。
- 统一风格选择编号方案（见 Phase 3，但编号属于流程交互，先在此对齐）。
- `[REVIEW]` 流程语义未变、阶段列表唯一、分类法唯一。

### Phase 2 — 技能结构
- 12 模块 MODULE.md 全部瘦身为"薄索引"（角色 + 指向 SKILL.md + references 列表），消除整文件重复。
- 修复悬空引用 `cyberpunk-template-01.md`（删除引用或落地为真实文件，默认删除引用，指向已有 `reusable-template-system.md`）。
- 校正根 SKILL.md 的 Delegation Rule / Skill Map：模块名、职责描述与各模块 SKILL.md frontmatter 一致。
- `[REVIEW]` 无重复整文件、无悬空链接、委派表与实际模块一致。

### Phase 3 — 风格模板
- `style-presets.md` 设为唯一预设库（4 个预设）。`prompt-generation-rules.md §3` 删除重复 JSON，改为"如何把基因转写进提示词"的方法论 + 引用 style-presets。
- 补齐缺失的第 4 个预设在所有需要列举处的呈现；统一编号为 `1-4 预设 / 0 自定义`。
- `templates/` 落地 1 个真实示例模板（与 demo 配套）。
- `[REVIEW]` 预设数量/命名/编号全仓库一致，基因 JSON 只有一份。

### Phase 4 — 视频提示词
- 新建 `MODELS.md` 作为模型 SSOT；全仓库模型名统一为规范写法；标注用户可见 vs 实现层。
- 图片提示词硬结构、图生视频动作模板做一致性校正（与 MODELS / style-presets 对齐）。
- 把陈旧 dev 笔记（RALV 复盘、dated discovery、构图多样性 dated note 的"问题背景"部分）迁入 `CHANGELOG.md`，reference 只留当前生效规则。
- `[REVIEW]` 模型名唯一规范、提示词规则与 SSOT 对齐、reference 无个人 dev log。

### Phase 5 — 最小可跑样例（demo）
- 选 1 段 ~45s「AI 科普」短文案，按重构后的流程**逐阶段产出静态产物**，落到 `examples/demo-ai-popsci/`。
- 全程不调真实 API：图片/视频用提示词 + 占位说明呈现；`project-state.json` 给出跑到末态的状态机快照。
- README 增加"看 demo"入口。
- `[REVIEW]` demo 完整覆盖 文案→分镜→风格→主体→图片提示词→图生视频→交付包，且每一步引用的是重构后的 SSOT。

---

## 5. 非目标（本轮不做）

- 不接真实生图/视频/数字人 API、不跑真实批量。
- 不改唤醒词、不改四大用户入口、不改状态机阶段语义。
- 不引入新依赖、不重写 Python 脚本逻辑（仅在 Phase 4 校正脚本里的模型名常量，如与 MODELS.md 冲突）。
- 不做 Web 可视化（后续轮次再议）。

---

## 6. Review 机制

- 每个 Phase 末尾 `[REVIEW]` 为硬门：Codex 完成该 Phase 全部任务后**停下并汇报**，等 Claude review。
- Claude review 关注：是否违反 §2 架构原则、是否引入新的不一致、是否破坏对外行为、SSOT 是否真的唯一。
- review 通过后在 TASKS.md 对应任务打勾，再进入下一 Phase。
