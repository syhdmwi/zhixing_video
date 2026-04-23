# Script Usage

脚本路径：

- `scripts/wuyinkeji_voice_clone.py`

## Required Env Var

- `VOICE_CLONE_API_KEY`
  或
- `WUYINKEJI_API_KEY`

如果要自动上传到火山 TOS，还需要：

- `TOS_ACCESS_KEY_ID`
- `TOS_SECRET_ACCESS_KEY`
- `TOS_BUCKET`
- `TOS_REGION`

可选：

- `TOS_PUBLIC_BASE_URL`

另外，当前上传实现依赖火山官方 Python SDK `tos`。如果工作区没有这个依赖，需要先安装到本地运行环境。

## Example

```bash
VOICE_CLONE_API_KEY="your_key" \
TOS_ACCESS_KEY_ID="your_tos_ak" \
TOS_SECRET_ACCESS_KEY="your_tos_sk" \
TOS_BUCKET="your_tos_bucket" \
TOS_REGION="cn-beijing" \
python3 scripts/wuyinkeji_voice_clone.py \
  --audio-url "https://example.com/my-voice.mp3" \
  --text "你好，这是一段用我自己声音朗读的测试文案。" \
  --name "我的声音测试" \
  --out-dir ./out
```

## Default API

- `POST https://api.wuyinkeji.com/api/voice/clone`

## Output

脚本会输出：

- 本地真实音频文件
- 元数据 JSON
- 如果配置了 TOS，则额外输出可直接给数字人使用的公网音频直链

其中元数据至少包含：

- `voice_id`
- `demo_audio_url`
- `uploaded_audio_url`
- `clone_name`

## Important Note

当前接入的是速创 `语音克隆（同步）` 接口，不是平台预设音色 TTS 接口。
