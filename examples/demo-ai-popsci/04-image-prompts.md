# 04 Image Prompts

SSOT 引用：
- 提示词硬结构：[../../ai-short-video-pipeline/references/prompt-generation-rules.md](../../ai-short-video-pipeline/references/prompt-generation-rules.md)
- 风格预设：[../../ai-video-image-prompts/references/style-presets.md](../../ai-video-image-prompts/references/style-presets.md)
- 模型清单：[../../MODELS.md](../../MODELS.md)
- `visual_carrier` 7 值定义：[../../ai-short-video-pipeline/SKILL.md](../../ai-short-video-pipeline/SKILL.md)

全局参数：`style_key=cyberpunk_bright_hud_infographic`，`image_model=GPT-Image-2`，后续图生视频 provider 为 `grok`，`aspect_ratio=16:9`，主讲人 `host_cyber_female_01`。

## Prompt Queue

### shot_01

- narration_excerpt: 你有没有发现，AI 现在不只是会聊天
- visual_carrier: `host_primary`
- image_prompt_cn: 赛博 HUD 讲解空间中，主讲人正面对镜头抛出问题，背景有简洁发光对话气泡和 AI 标识。
- image_prompt:
```text
Futuristic tech explainer studio with dark glass walls, cyan-violet HUD panels, and a clean central stage. The approved host_cyber_female_01 stands facing camera, confident and curious, one hand slightly raised as if asking a question. Use style_key cyberpunk_bright_hud_infographic from style-presets.md, bright cyber HUD infographic style, cool neon palette, glossy glass panels, clean composition, medium shot. No photorealistic portrait, no chibi proportions, no dense readable text, no extra characters, no distorted hands.
```
- negative_prompt_or_constraints: template negative constraints + no readable long text.
- placeholder: [占位：shot_01 生成图]

### shot_02

- narration_excerpt: 它正在变成一个会干活的同事
- visual_carrier: `host_with_visual`
- image_prompt_cn: 主讲人与发光 AI 智能体核心并置，表现“同事”感。
- image_prompt:
```text
Futuristic digital workspace, the approved host_cyber_female_01 on the left, the approved ai_agent_core_01 floating on the right like a capable coworker interface, connected by thin cyan task lines. The host looks toward the AI core with trust and focus. Use style_key cyberpunk_bright_hud_infographic, bright cyber HUD infographic style, polished 3D illustration feel, balanced dual-subject composition, subtitle-safe lower area. No photorealistic human, no mascot, no clutter, no readable paragraph text.
```
- negative_prompt_or_constraints: keep host and AI core identical to approved references.
- placeholder: [占位：shot_02 生成图]

### shot_03

- narration_excerpt: 过去我们打开十几个软件，复制资料、写表格、查邮件，再手动汇总
- visual_carrier: `ui_closeup`
- image_prompt_cn: 多窗口界面堆叠成旧流程混乱感，不出现主讲人。
- image_prompt:
```text
Close-up of a chaotic desktop-like HUD workspace with many floating software windows: document pane, spreadsheet grid, mail inbox, browser cards, and copy-paste arrows, all arranged as a confusing old workflow. No human figure. Use style_key cyberpunk_bright_hud_infographic, cyan and violet glass UI panels, dark futuristic background, strong depth layers, clear visual hierarchy without readable long text. No real brand UI, no dense tiny text, no messy illegible data wall.
```
- negative_prompt_or_constraints: no real private data, no readable email content.
- placeholder: [占位：shot_03 生成图]

### shot_04

- narration_excerpt: 现在的智能体可以理解目标，自己拆步骤
- visual_carrier: `concept_explainer`
- image_prompt_cn: 目标被拆成计划、工具、检查三个流程节点。
- image_prompt:
```text
Concept explainer diagram in a futuristic HUD room: a glowing goal crystal at the top splits into three clean modules labeled only by abstract icons for plan, tools, and review, connected to the approved ai_agent_core_01 in the center. Use style_key cyberpunk_bright_hud_infographic, organized infographic layout, luminous cyan-violet lines, dark glass background, no host. Keep icons simple and mostly text-free. No clutter, no long readable text, no extra mascots.
```
- negative_prompt_or_constraints: structure must be readable through shapes, not text.
- placeholder: [占位：shot_04 生成图]

### shot_05

- narration_excerpt: 调用工具、检查结果
- visual_carrier: `brand_symbolic`
- image_prompt_cn: 工具链节点围绕 AI 核心形成闭环，使用泛化工具符号。
- image_prompt:
```text
Symbolic toolchain loop around the approved ai_agent_core_01: generic icons for search, file, spreadsheet, email, and checklist orbit in a clean circular workflow, with a final verification shield icon glowing green. Use style_key cyberpunk_bright_hud_infographic, bright HUD infographic style, polished glass panels, strong circular composition, no real logos unless provided as references. No readable long text, no crowded interface, no photorealistic hardware.
```
- negative_prompt_or_constraints: generic symbols only; avoid fake brand logos.
- placeholder: [占位：shot_05 生成图]

### shot_06

- narration_excerpt: 区别就像从“遥控器”变成“实习生”
- visual_carrier: `data_compare`
- image_prompt_cn: 左侧遥控器只能按键，右侧智能实习生能理解任务。
- image_prompt:
```text
Split-screen comparison infographic: left side shows a simple remote-control metaphor with one-way button commands; right side shows a helpful AI intern represented by the approved ai_agent_core_01 coordinating task cards and checkmarks. Use style_key cyberpunk_bright_hud_infographic, clean left-right comparison, cyan-violet HUD panels, clear contrast between passive control and active workflow. Minimal icon labels only, no paragraphs, no extra characters.
```
- negative_prompt_or_constraints: no childish mascot, no cluttered comparison table.
- placeholder: [占位：shot_06 生成图]

### shot_07

- narration_excerpt: 下一次你用 AI，别只问它答案，试着给它一个小目标
- visual_carrier: `scene_only`
- image_prompt_cn: 无人物的完成态流程看板，展示目标到交付的完整闭环。
- image_prompt:
```text
Wide scene-only shot of a futuristic command board showing a complete workflow from small goal to final delivery package, represented by glowing connected cards, progress arcs, and a completed checkmark at the end. No host, no character. Use style_key cyberpunk_bright_hud_infographic, dark glass environment, bright cyan-violet HUD, clean open composition with subtitle-safe area. No readable long text, no dense UI, no extra subjects.
```
- negative_prompt_or_constraints: no people, no paragraph text, keep flow readable by icons.
- placeholder: [占位：shot_07 生成图]
