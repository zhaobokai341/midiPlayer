# Pixel MIDI Player

**English** | [简体中文](#简体中文)

A Python tool that converts MIDI note data into compact PNG images and plays music directly from those images.

一个使用 Python 编写的工具，可以将 MIDI 音符数据编码为紧凑的 PNG 图片，并直接从图片中解码和播放音乐。

---

## ✨ Features | 功能特性

- **MIDI to PNG:** Convert MIDI files into encoded PNG images.  
  **MIDI 转 PNG：** 将 MIDI 文件转换为编码后的 PNG 图片。

- **PNG to Music:** Decode PNG images and play the encoded music.  
  **PNG 转音乐：** 从 PNG 图片中解码音符并播放音乐。

- **Compact Encoding:** Store note information efficiently using pixel data.  
  **紧凑编码：** 使用像素数据高效存储音符信息。

- **Note Information:** Preserve pitch, velocity, start time, duration, and track information.  
  **音符信息：** 保存音高、力度、开始时间、持续时间以及音轨信息。

- **Multi-track Support:** Handle notes from multiple MIDI tracks.  
  **多音轨支持：** 处理来自多个 MIDI 音轨的音符。

---

## 📦 Requirements | 环境要求

- Python 3.10 or newer  
  Python 3.10 或更高版本

- A working audio output device  
  可正常使用的音频输出设备

### Install Dependencies | 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage | 使用方法

### 1. Convert MIDI to PNG | 将 MIDI 转换为 PNG

```bash
python convertToImageAndPlay.py encode input.mid output.png
```

**English:** Reads a MIDI file and converts its note data into an encoded PNG image.

**中文：** 读取 MIDI 文件，并将其中的音符数据转换为编码后的 PNG 图片。

### 2. Play Music from PNG | 从 PNG 播放音乐

```bash
python convertToImageAndPlay.py play output.png
```

**English:** Decodes the PNG image and plays the reconstructed music.

**中文：** 解码 PNG 图片中的音符数据，并播放还原后的音乐。

---

## 🧩 How It Works | 工作原理

**English**

Instead of creating a traditional piano-roll image, this project stores MIDI note information directly in PNG pixel data.

Each note is represented by a fixed-size pixel record containing information such as:

| Data | Description |
|---|---|
| Pitch | MIDI note number |
| Velocity | Note intensity |
| Track ID | Original track identifier |
| Start Time | Note starting position |
| Duration | Note playing duration |
| Instrument | Instrument program and drum information |

**简体中文**

本项目并不生成传统的钢琴卷帘可视化图片，而是直接将 MIDI 音符信息编码到 PNG 图片的像素数据中。

每个音符都由固定大小的像素记录表示，其中包含：

| 数据 | 说明 |
|---|---|
| 音高（Pitch） | MIDI 音符编号 |
| 力度（Velocity） | 音符力度 |
| 音轨 ID（Track ID） | 原始音轨标识符 |
| 开始时间（Start Time） | 音符开始的位置 |
| 持续时间（Duration） | 音符播放时长 |
| 乐器（Instrument） | 乐器编号及鼓组信息 |

---

## ⚠️ Notes | 注意事项

- **English:** Encoded PNG files are data files, not ordinary visual images.
- **中文：** 编码后的 PNG 是数据文件，而不是普通的可视化图片。

- **English:** Avoid resizing, editing, or recompressing encoded PNG files, as this may corrupt their pixel data.
- **中文：** 请勿调整编码图片的尺寸、编辑像素或重新压缩，否则可能导致像素数据损坏。

- **English:** Audio playback requires a working audio output device and a compatible audio backend.
- **中文：** 播放音乐需要正常工作的音频输出设备以及兼容的音频后端。

