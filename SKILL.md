---
name: deep-see
description: 给DeepSeek装上眼睛。当用户发送截图/图片并询问内容时，调用OCR识别图片中的文字。解决DeepSeek模型不支持多模态/视觉的问题。
metadata:
  short-description: 给DeepSeek装眼睛——OCR识别截图文字（v1.2 体验优化版）
---

# deep-see

DeepSeek 不支持多模态/视觉。这个 skill 给它装上眼睛 👀

## 适用场景
当用户发送截图/图片并问"什么内容"、"帮我看看"时使用。

## 快速开始

### 1. 安装依赖
```bash
pip install easyocr pillow
```
或者使用一键安装脚本：
```bash
python install.py
```

### 2. 识别图片
```bash
python ocr_tool.py 图片路径.png
```

## ✨ v1.2 体验优化
- ✅ **自动检测依赖** — 缺少依赖时给出明确提示
- ✅ **一键安装** — `python install.py` 自动安装
- ✅ **智能预处理** — 缩放 + 灰度 + 对比度 + 锐化
- ✅ **友好输出** — 置信度标记 ✅⚠️❌ + 耗时 + 图片信息
- ✅ **错误提示** — 文件不存在、格式不支持、网络问题都有提示

## 文件说明
| 文件 | 用途 |
|------|------|
| `ocr_tool.py` | OCR 识别工具（核心） |
| `install.py` | 一键安装脚本 |
| `SKILL.md` | Codex skill 定义 |

## 隐私说明
- 纯本地运行，图片不上传任何云端
- 支持中文、英文
- 首次运行自动下载模型（约100MB），后续离线可用
