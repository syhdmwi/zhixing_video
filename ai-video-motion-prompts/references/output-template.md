# Output Template

```json
[
  {
    "shot_id": "shot-01",
    "source_image_requirement": "Use the approved still image for shot-01.",
    "camera_motion": "相机缓慢向上移动并逐渐后拉远",
    "default_stability_preset": "保持人物/场景/主要角色不变形，主体保持原地静止，不要行走、不要跟拍人物，只有相机缓慢平移或拉远",
    "recommended_duration_seconds": 4,
    "test_batch_priority": "high",
    "motion_prompt": "人物保持站立并固定不动，身体、手部、头部、表情和角色位置全部锁定，不要迈步，不要摆动，不要转头，不要眨眼，不要做口型，不要改变姿势。镜头缓慢向上移动，同时逐渐远离人物，形成轻微上升加后拉远的运镜效果。只允许镜头运动，不允许人物或主要角色产生任何动画变化，保持人物/场景/主要角色不变形。",
    "stability_note": "Use the default stability preset.",
    "risk_note": "Low risk. Suitable for first-batch testing."
  },
  {
    "shot_id": "shot-02",
    "source_image_requirement": "Use the approved still image for shot-02.",
    "camera_motion": "关键帧轻微后拉",
    "default_stability_preset": "保持人物/场景/主要角色完全静止，像关键帧插画一样固定不动，不要人物动作，不要环境动画，不要道具动画，只允许非常轻微的镜头移动，保持整体构图稳定，不要漂移，不要变形",
    "recommended_duration_seconds": 4,
    "test_batch_priority": "high",
    "motion_prompt": "画面像关键帧插画一样基本静止，人物、环境、主要角色和道具全部保持固定不动，不要走动，不要转头，不要眨眼，不要口型，不要任何环境变化，只做非常轻微的相机后拉远，形成轻弱的关键帧运镜感，保持整体构图稳定。",
    "stability_note": "Use the keyframe-light-motion stability preset.",
    "risk_note": "Very low risk. Suitable when the user wants near-still keyframe motion."
  }
]
```
