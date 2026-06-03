# Motion Design Rules

## 1. Priority Rule

图生视频首先要稳。

优先级：

1. 主体不跑形
2. 人脸不漂
3. 肢体不畸变
4. 镜头方向简单清楚

## 2. Fixed Motion Presets

默认只用这些固定镜头运动：

- 相机缓慢向左平移
- 相机缓慢向右平移
- 相机缓慢向下平移
- 相机缓慢向上平移
- 相机缓慢向后拉远
- 相机缓慢推近（push-in）
- 相机轻微环绕（slight orbit，仅用于对比/冲突镜头）

## 3. Character Shot Rules

人物镜头优先：

- 相机向左平移
- 相机向右平移
- 相机向后拉远
- 相机缓慢推近

默认少用：

- 向上平移
- 向下平移
- 轻微环绕

因为人物镜头更容易在上下运动里出现脸部或肢体不稳定。

## 4. Scene Shot Rules

纯场景镜头可使用固定镜头预设，但优先：

- 相机向左平移
- 相机向右平移
- 相机向后拉远
- 相机缓慢推近

如果画面有高楼、台阶、门、竖向空间，再考虑：

- 相机向上平移
- 相机向下平移

## 5. Stability Rule

默认稳定性约束以 [image-to-video-prompt-rules.md](../../ai-video-generate-videos/references/image-to-video-prompt-rules.md) 的 `§5 Default Safe Rules` 为唯一权威。

本文件只保留镜头方向和风险判断，不重复维护稳定性提示词正文。不要把提示词写成长段复杂说明。

## 6. Risk Labels

建议每个镜头标一个风险等级：

- `low`: 人物微动作或纯场景轻运动
- `medium`: 人物和吉祥物有互动，或场景元素较多
- `high`: 多主体复杂动作、大视角变化、强形变需求

默认批量执行时，优先先做 `low` 和 `medium`，避免一开始就堆 `high`。
