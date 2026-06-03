# Output Template

```json
[
  {
    "shot_id": "shot-01",
    "source_image_requirement": "Use the approved still image for shot-01.",
    "motion_type": "讲述型",
    "motion_intensity": "low",
    "camera_motion": "gentle push-in",
    "default_stability_preset": "image-to-video-prompt-rules §5 Default Safe Rules",
    "recommended_duration_seconds": 4,
    "test_batch_priority": "high",
    "video_prompt": "The host makes a slight natural head movement and subtle breathing motion, with a very small hand gesture near the body. The camera gently pushes in. Keep the face, hairstyle, outfit, body proportions, and background composition unchanged. Keep the original art style unchanged. No new people, no extra limbs, no strong motion, no scene drift.",
    "stability_note": "Use the default stability preset.",
    "risk_note": "Low risk. Suitable for first-batch testing."
  },
  {
    "shot_id": "shot-02",
    "source_image_requirement": "Use the approved still image for shot-02.",
    "motion_type": "展示型",
    "motion_intensity": "low",
    "camera_motion": "gentle push-in with slight side drift",
    "default_stability_preset": "image-to-video-prompt-rules §5 Keyframe-Light Safe Rules",
    "recommended_duration_seconds": 4,
    "test_batch_priority": "high",
    "video_prompt": "The robot makes a slight head turn and a small arm movement as if explaining something. The camera gently pushes in with a subtle side drift. Keep the robot design, proportions, materials, background structure, and original art style unchanged. No redesign, no extra limbs, no new characters, no environment drift.",
    "stability_note": "Use the keyframe-light-motion stability preset.",
    "risk_note": "Low risk. Suitable for a first-batch image-to-video test."
  }
]
```
