# Grok 视频模版套用00

模板名称：

- `grok视频模版套用00`

适用场景：

- `grok` provider
- 单张静帧图生视频
- 人物或主要角色需要稳定外观，同时做一个小幅主动动作
- 希望镜头以较稳的方式做“逐渐后拉 / 轻微横移 / 轻微推近”
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
{main_subject} makes one small active motion in {scene_summary}, such as a subtle nod, a small emphasizing hand gesture, a slight reach, or a gentle head turn, with natural breathing. The camera slowly pushes in or pulls back with a very slight sideways drift. Preserve {consistency_points}; keep face, hairstyle, outfit, body proportions, original style, and composition consistent. No walking, no large pose change, no extra characters, no subject drift, no background drift.
```

套用规则：

- 用户选择 `grok` 后，应先询问是否要使用 `grok视频模版套用00`
- 如果用户同意，优先用这条模板作为基础提示词
- 再按当前镜头内容替换主体、场景和关键一致性描述
- 保留“一个小幅主动动作 + 呼吸感 + 人物安全镜头运动 + 外观和构图稳定”的结构
- 人物镜头默认使用套用00 的主动小动作版；纯静帧或关键帧需求才使用套用01
- 人物镜头默认只用后拉、轻微横移或轻微推近，不使用上移
- 上移仅用于纯场景竖向空间镜头，例如高楼、台阶、门或竖向空间；人物镜头不用
- 如果当前镜头不是人物图，而是纯场景图，只沿用“镜头运动 + 构图稳定 + 避免漂移”的结构，不强行保留人物约束句

# Grok 视频模版套用01

模板名称：

- `grok视频模版套用01`

适用场景：

- `grok` provider
- 单张静帧图生视频
- 用户希望视频像关键帧一样只做轻微运镜
- 人物、环境、道具都应基本静止
- 不希望出现角色表演感
- 仅当用户明确要求“像关键帧一样基本静止”或某镜头确实必须冻结时使用

变量槽位：

- `{main_subject}`：当前镜头里的主主体
- `{scene_summary}`：当前镜头所在场景
- `{consistency_points}`：当前镜头必须锁定的识别特征

默认提示词：

```text
{main_subject} remains completely still like a keyframe illustration in {scene_summary}. No walking, no body motion, no hand motion, no head turn, no blinking, no mouth movement, no pose change, and no environmental animation. Keep {consistency_points} and the full composition stable. Only allow a very slight camera move, like a subtle keyframe motion. Avoid subject drift, avoid deformation, and avoid turning this into a character animation.
```

推荐中文理解：

- 画面整体像关键帧插画一样固定不动
- 只允许非常轻微的镜头位移
- 不要把它做成角色表演视频
