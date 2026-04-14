# Grok 视频模版套用00

模板名称：

- `grok视频模版套用00`

适用场景：

- `grok` provider
- 单张静帧图生视频
- 人物或主要角色需要尽量保持静止
- 希望镜头以较稳的方式做“缓慢上移 + 逐渐后拉”
- 当前镜头里存在一个或多个需要保持一致的高频主体

变量槽位：

- `{main_subject}`：当前镜头里的主主体
- `{recurring_subject_2}`：当前镜头里的第二高频主体，没有就删掉
- `{scene_summary}`：当前镜头所在场景
- `{consistency_points}`：当前镜头必须锁定的识别特征

识别规则：

- 不要把“龙虾”写死成固定主角
- 每次都应先识别当前文案和当前镜头里，谁才是反复出现、需要保持一致的主体
- 这个主体可以是人，也可以是动物、植物、吉祥物、产品、关键道具
- 如果下一个文案里高频主体变成兔子、鸡、向日葵或别的对象，就把对应主体代入模板
- 只有当前镜头真实存在、并且需要稳定外观的对象，才应写进模板

默认提示词：

```text
{main_subject} and {recurring_subject_2} remain completely still like a frozen illustration in {scene_summary}. No walking, no body motion, no hand motion, no head turn, no blinking, no mouth movement, and no pose change. The camera slowly cranes upward while gradually pulling back from the subject. Keep the main subject, recurring subjects, and the composition stable. Preserve {consistency_points} and background consistency. Avoid character animation and avoid subject drift.
```

套用规则：

- 用户选择 `grok` 后，应先询问是否要使用 `grok视频模版套用00`
- 如果用户同意，优先用这条模板作为基础提示词
- 再按当前镜头内容替换主体、场景和关键一致性描述
- 保留“主体固定不动 + 镜头缓慢上移并后拉 + 保持构图稳定”的结构
- 如果当前镜头不是人物图，而是纯场景图，只沿用“镜头运动 + 构图稳定 + 避免漂移”的结构，不强行保留人物约束句
