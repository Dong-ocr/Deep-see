---
name: deep-see
description: 给DeepSeek装上眼睛。当用户发送截图/图片并询问内容时，调用OCR识别图片中的文字。v2.0 引擎升级，速度5倍提升。
metadata:
  short-description: 给DeepSeek装眼睛——OCR截图识别（v2.0 引擎升级版）
---

# deep-see

DeepSeek 不支持多模态/视觉。这个 skill 给它装上眼睛 👀

## 快速开始

### 安装
```bash
pip install paddleocr
# 或使用备选引擎
pip install easyocr
```

### 识别图片
```bash
python ocr_tool.py 截图.png
```

## 🚀 v2.0 引擎升级
- **PaddleOCR 引擎** — 速度提升 5 倍，准确率更高
- **引擎缓存** — 第二次使用秒级加载
- **自动兜底** — PaddleOCR 不可用时自动切 EasyOCR
- **准确率 ~96%** — 远超 EasyOCR

## 参数说明
| 参数 | 说明 |
|------|------|
| `--lang zh` | 🇨🇳 中文（默认） |
| `--lang ja` | 🇯🇵 日文 |
| `--lang kr` | 🇰🇷 韩文 |
| `--lang en` | 🇬🇧 英文 |
| `--engine easy` | 强制使用 EasyOCR |
