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

## 8. 中文映射建议

为了便于上游分镜使用，可用以下映射：

- `主讲人出镜` -> `主讲人讲述模板`
- `机器人解说` -> `机器人讲解模板`
- `办公室办公` -> `办公室工作模板`
- `法庭/会议` -> `法庭 / 会议讲述模板`
- `情绪/思考` -> `情绪沉思模板`
- `环境介绍` -> `场景展示模板`
- `图表/面板` -> `数据 / 屏幕展示模板`
