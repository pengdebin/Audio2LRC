# Audio2LRC — Audio → LRC (time-aligned) 🔧

Audio2LRC是一个从音频中提取人声并生成LRC的小工具。主要流程：

1. 可选：使用 `demucs` 从原始音频分离出人声（vocals）以提高对齐精度；
2. 使用 `whisper` 进行转录；
3. 可选：使用 `whisperx` 对词/句进行强制对齐（提高时间精度），并生成按句的 LRC 文件。

## 功能 ✅
- 可选人声分离（`demucs`）以提取 `vocals.wav` 文件（默认输出目录为 `temp/`）
- 转录（`openai-whisper`）并可选使用 `whisperx` 对齐以减少时间漂移
- 生成按句时间戳的 `.lrc` 文件（英文，每句一行）
- 输出示例：
  `[00:12.34]This is an example.`

## 依赖 🔧
- Python 3.8+
- FFmpeg（系统需安装并加入 PATH）
- 安装项目依赖：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

重要提示：
- 使用 `--sep demucs` 需要先安装 `demucs`（已列在 `requirements.txt`）；Demucs 在 CPU 上可运行，但在 GPU 上速度更快。
- 使用 `--aligner whisperx` 需要安装 `whisperx`（见 `requirements.txt`）。
- 如果发生 `ffmpeg` 相关错误，请确保系统可执行 `ffmpeg`，并在运行时把该路径加入 PATH）。

## 使用方法 💡

批量目录处理（将 `input` 目录下的音频全部生成为同名 `.lrc`）：
```
python transcribe_lrc.py --input input --ext .mp3,.wav
```

## 参数说明 💡

- `--input` / `-i`：源音频目录（默认 `input`）
- `--ext`：要查找的音频扩展名，逗号分隔（默认 `.mp3`）
- `--sep`：声源分离方式（默认为`demucs`）
- `--aligner`：对齐器（默认 `whisperx`）
- `--model`：Whisper 模型（`tiny|base|small|medium|large|large-v2|large-v3`，默认 `large-v3`）
- `--output`：输出目录（默认 `output`），生成的 `.lrc` 将写在该目录下
- `--overwrite`：覆盖已存在文件（否则会跳过）

## 输出位置与中间产物 🗂️
- 分离后的人声音频默认放在 `temp/<model>/<basename>/vocals.*`。
- 最终 `.lrc` 文件会写入 `--output` 指定目录，文件名与原音频名相同（扩展为 `.lrc`）。
