# Motion Template Library

这个文件提供可直接复用的图生视频动作模板。

使用方法：

1. 先判断镜头的 `motion_type`
2. 再选择动作强度
3. 最后把主体名称、场景名称和风格信息代入

默认先用低风险模板，不要一上来追求复杂动作。

## 1. 主讲人讲述模板

### low

```text
The host makes a slight natural head movement and subtle breathing motion, with a very small hand gesture near the body. The camera gently pushes in. Keep the face, hairstyle, outfit, body proportions, and background composition unchanged. Keep the original art style unchanged. No new people, no extra limbs, no strong motion, no scene drift.
```

### medium

```text
The host makes a gentle speaking gesture with one hand, a small natural nod, and subtle upper-body movement. The camera slowly drifts left to right while pushing in slightly. Keep the face, hairstyle, outfit, body proportions, and background composition unchanged. Keep the original art style unchanged. No new people, no extra limbs, no large pose change, no scene drift.
```

## 2. 机器人讲解模板

### low

```text
The robot makes a slight head turn and a small arm movement as if explaining something. The camera gently pushes in. Keep the robot design, proportions, materials, background structure, and original art style unchanged. No redesign, no extra arms, no new characters, no environment drift.
```

### medium

```text
The robot raises one arm slightly and turns its head a little toward the viewer, with subtle body motion. The camera slowly moves sideways with a soft push-in. Keep the robot design, proportions, materials, background structure, and original art style unchanged. No redesign, no extra limbs, no new characters, no environment drift.
```

## 3. 办公室工作模板

### low

```text
The main person stays mostly in place with subtle breathing and a small natural posture shift, while the screen glow and nearby office activity change very slightly. The camera slowly pushes in. Keep face, outfit, desk layout, room structure, and original art style unchanged. No scene drift, no new people, no strong body movement.
```

## 4. 法庭 / 会议讲述模板

### low

```text
The speaker makes a small natural head movement and slight hand motion while the audience remains mostly still with minimal attention shifts. The camera gently pushes in. Keep all faces, clothing, stage layout, seating structure, and original art style unchanged. No crowd distortion, no scene drift, no extra people.
```

## 5. 情绪沉思模板

### low

```text
The person shows subtle breathing, a slight downward or upward head movement, and a very small eye-line change. The camera slowly pushes in. Keep the face, hairstyle, outfit, body proportions, and original art style unchanged. No large motion, no new elements, no background drift.
```

## 6. 场景展示模板

### low

```text
The scene remains mostly stable, with only slight ambient motion and a gentle camera drift. Keep all architecture, props, screen layout, and original art style unchanged. No new characters, no structural change, no sudden motion.
```

## 7. 数据 / 屏幕展示模板

### low

```text
The main subject stays stable while the screens or holographic panels show slight subtle activity. The camera gently pushes in or drifts sideways. Keep the subject appearance, screen layout, scene structure, and original art style unchanged. No new elements, no distortion, no heavy animation.
```

## 8. visual_carrier 映射指引

上游分镜只使用 `visual_carrier` 7 值，不再维护第三套中文场景词表。具体 `visual_carrier -> motion_type -> 模板/已验证提示词` 映射以 [image-to-video-prompt-rules.md](./image-to-video-prompt-rules.md) 的「visual_carrier 运动映射表」为准。

本库可被映射表引用的通用模板包括：

- `主讲人讲述模板`
- `机器人讲解模板`
- `办公室工作模板`
- `法庭 / 会议讲述模板`
- `情绪沉思模板`
- `场景展示模板`
- `数据 / 屏幕展示模板`

## 9. 人物小幅动作动词库

人物镜头优先从此库选 1 个主动作 + 呼吸感作为句子主语；稳定约束仍保留脸、发型、服装、肤色、风格和构图不变。不要默认写“保持原姿势”。

| 动作 | 适用镜头 | 强度建议 |
| --- | --- | --- |
| 轻微点头 | 讲述型、CTA、观点确认 | `low` |
| 点头幅度稍明显 | 重点句、强调句 | `medium` |
| 抬手强调 | 讲述型重点句 | `medium` |
| 轻微转头 | 展示型、转向画面元素 | `low` |
| 伸手与界面互动 | host_with_visual、ui_closeup 联动镜头 | `medium` |
| 手指轻微动效 | 界面互动、按钮说明 | `low` |
| 微笑看镜头 | 收束、CTA、轻松讲述 | `low` |
| 自然站姿 + 胳膊自然下垂 + 肩膀放松 | 开场、收尾、安全低动效镜头 | `low` |
| 头部轻微下沉 | 情绪型、严肃、忧虑、反思 | `low` |
| 眼神变化（坚定 / 严肃 / 惊喜 / 忧虑） | 情绪型、冲突前后、观点转折 | `low` |
| 肩膀细微呼吸感 | 所有人物镜头的安全补充动作 | `low` |

## 10. 已验证动作提示词库（中文 · grok 实测流畅）

这些提示词为用户实测可用、可直接套用的中文动作提示词。原文保持不改写；英文 provider 可在条目下另配英文等价版。

### 已验证 1

标签：`visual_carrier=host_primary` / `motion_type=讲述型` / `motion_intensity=low` / `camera=推近`

```text
主讲人轻微点头，眼神稳定看镜头，肩膀有细微呼吸感，镜头轻微推近，保持人物发型、服装、肤色完全不变，画面风格稳定，不要新增角色，不要闪烁。
```

### 已验证 2

标签：`visual_carrier=scene_only` / `motion_type=场景型` / `motion_intensity=low` / `camera=横移`

```text
数据流动轻微闪烁，画面缓慢横移，展示AI内容泛滥的场景，保持场景结构稳定，风格不变。
```

### 已验证 3

标签：`visual_carrier=host_primary` / `motion_type=讲述型` / `motion_intensity=medium` / `camera=推近`

```text
主讲人轻微抬手强调，点头幅度稍明显，眼神坚定，镜头轻微推近，保持人物外观完全不变。
```

### 已验证 4

标签：`visual_carrier=ui_closeup` / `motion_type=展示型` / `motion_intensity=low` / `camera=横移`

```text
AI工具界面轻微动效，按钮有极小幅动画，镜头缓慢横移，保持场景稳定。
```

### 已验证 5

标签：`visual_carrier=host_primary` / `motion_type=情绪型` / `motion_intensity=low` / `camera=推近`

```text
主讲人表情严肃，眼神略显忧虑，头部轻微下沉，镜头轻微推近，保持人物外观不变。
```

### 已验证 6

标签：`visual_carrier=scene_only` / `motion_type=场景型` / `motion_intensity=low` / `camera=后拉`

```text
极简画面缓慢淡出淡入，镜头缓慢后拉，展示大面积留白，保持风格稳定。
```

### 已验证 7

标签：`visual_carrier=scene_only` / `motion_type=情绪型` / `motion_intensity=low` / `camera=推近`

```text
画面轻微呼吸感，色温保持稳定，镜头缓慢推近，展示电影质感，保持风格不变。
```

### 已验证 8

标签：`visual_carrier=host_with_visual` / `motion_type=展示型` / `motion_intensity=medium` / `camera=推近`

```text
主讲人伸手与界面互动，手指轻微动效，镜头轻微推近，保持人物外观完全不变。
```

### 已验证 9

标签：`visual_carrier=data_compare` / `motion_type=冲突型` / `motion_intensity=medium` / `camera=环绕`

```text
对比画面缓慢切换，镜头轻微环绕感，保持场景稳定，风格不变。
```

### 已验证 10

标签：`visual_carrier=host_primary` / `motion_type=讲述型` / `motion_intensity=low` / `camera=推近`

```text
主讲人自信表情，轻微点头，眼神坚定，镜头轻微推近，保持人物外观完全不变。
```

### 已验证 11

标签：`visual_carrier=host_primary` / `motion_type=讲述型` / `motion_intensity=low` / `camera=推近`

```text
主讲人微笑看镜头，自然站姿，胳膊自然下垂，肩膀放松，镜头轻微推近，保持人物外观完全不变。
```
