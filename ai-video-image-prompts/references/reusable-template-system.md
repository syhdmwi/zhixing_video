# Reusable Template System

这个文件定义“真正可迁移”的三层模板系统。目标不是复用某一批具体镜头，而是复用：

- 风格模板
- 主体一致性模板
- 正式任务清单模板

## Why This Matters

如果后面换了文案、人物、常见动物或常见物体，旧的具体任务清单通常不能直接继续执行。

但以下内容仍然可以稳定复用：

- 风格写法
- 一致性约束写法
- 品牌元素写法
- 提示词结构
- 生图任务清单格式

所以真正应该沉淀的是模板层，而不是某一批镜头本身。

## The Three Reusable Layers

### 1. Style Template

风格模板负责固定这些内容：

- 风格方向
- 色彩倾向
- 光影倾向
- 材质倾向
- 环境倾向
- 构图倾向
- 负面约束

例子：

- `赛博朋克风格模板01`
- `素描风格模板01`

### 2. Subject Consistency Template

主体一致性模板负责固定这些内容：

- 主人物锚点写法
- 高频动物 / 吉祥物 / 常见物体锚点写法
- 哪些部分不能改
- 哪些部分只允许做风格适配

这个模板不绑定某一个具体人物或物体，而是使用占位符。

当前通用版模板见：

- [subject-consistency-template-01.md](./subject-consistency-template-01.md)

如果要按模型拆分提示词写法，当前可直接复用：

- [gpt-image2-prompt-template-01.md](./gpt-image2-prompt-template-01.md)
- [nanobanana-prompt-template-01.md](./nanobanana-prompt-template-01.md)

### 3. Execution Queue Template

执行清单模板负责固定生图批处理输入格式，例如：

- `shot_id`
- `frame_type`
- `image_prompt`
- `reference_urls`
- `consistency_note`

这个模板是“怎么提交”，不是“提交什么内容”。

## How To Reuse

当用户换了新文案时，优先按这个顺序复用：

1. 选择已有风格模板
2. 套用主体一致性模板并替换主体锚点
3. 生成新的正式提示词
4. 套用统一的执行清单格式

也就是说：

- 文案内容可以变
- 人物可以变
- 常见动物或物体可以变
- 但模板结构不变

## Practical Rule

如果只是“换内容”，优先复用模板。

如果连整体画风都换了，再新增新的风格模板，而不是推翻已有模板系统。
