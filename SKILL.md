---
name: deep-see
description: 给DeepSeek装上眼睛。当用户发送截图/图片并询问内容时，调用OCR识别图片中的文字。支持中文/日文/韩文/英文。
metadata:
  short-description: 给DeepSeek装眼睛——多语言OCR截图识别（v1.5）
---

# deep-see

DeepSeek 不支持多模态/视觉。这个 skill 给它装上眼睛 👀

## 适用场景
当用户发送截图/图片并问"什么内容"、"帮我看看"时使用。

## 快速开始

### 安装
```bash
python install.py
```

### 识别图片
```bash
# 中文（默认）
python ocr_tool.py 截图.png

# 日文
python ocr_tool.py 截图.jpg --lang ja

# 韩文
python ocr_tool.py 截图.png --lang kr

# 全部语言（中文+日文+韩文+英文）
python ocr_tool.py 截图.png --lang all
```

## ✨ v1.5 多语言版
| 参数 | 语言 | 说明 |
|------|------|------|
| `--lang zh` | 🇨🇳 中文+英文 | 默认，简体中文+English |
| `--lang ja` | 🇯🇵 日文+英文 | 日本語+English |
| `--lang kr` | 🇰🇷 韩文+英文 | 한국어+English |
| `--lang all` | 🌐 全部 | 分两组识别，结果合并 |

## 文件说明
| 文件 | 用途 |
|------|------|
| `ocr_tool.py` | OCR 工具（v1.5 多语言版） |
| `install.py` | 一键安装脚本 |

## 隐私说明
- 纯本地运行，图片不上传任何云端
- 首次运行自动下载对应语言的模型文件
