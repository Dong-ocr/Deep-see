# deep-see

给 DeepSeek 装上眼睛 👀

<p align="center">
  <a href="https://github.com/Dong-ocr/Deep-see/stargazers">
    <img src="https://img.shields.io/github/stars/Dong-ocr/Deep-see?style=for-the-badge&label=⭐%20Star&color=blue" alt="Stars">
  </a>
  <a href="https://github.com/Dong-ocr/Deep-see/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Dong-ocr/Deep-see?style=for-the-badge&color=green" alt="License">
  </a>
  <a href="https://github.com/Dong-ocr/Deep-see/releases">
    <img src="https://img.shields.io/github/v/release/Dong-ocr/Deep-see?style=for-the-badge&color=orange" alt="Version">
  </a>
</p>

## 这是什么
DeepSeek 不支持多模态/视觉。这个 Codex skill 通过本地 OCR 让 DeepSeek 也能看见截图里的文字。

## ✨ 特性
| 特性 | 说明 |
|------|------|
| 🚀 **速度优化** | 图片预处理（缩放+灰度+增强+锐化），识别更快更准 |
| 🔒 **隐私安全** | 纯本地运行，不上传任何图片 |
| 🌐 **中英双语** | 同时支持中文和英文识别 |
| 📊 **智能输出** | 置信度标记 ✅⚠️❌ + 耗时显示 |
| 📦 **离线可用** | 首次安装后无需联网 |
| 🎯 **一键安装** | `python install.py` 自动检测+安装依赖 |

## 快速开始

```bash
# 1. 安装依赖
pip install easyocr pillow

# 2. 识别截图
python ocr_tool.py 截图.png
```

## 文件结构
```
deep-see/
├── ocr_tool.py     # OCR 识别工具（核心）
├── install.py      # 一键安装脚本
├── SKILL.md        # Codex skill 定义
├── README.md       # 项目说明
├── promo.html      # 宣传卡片
└── LICENSE         # MIT 协议
```

## 版本历史
| 版本 | 内容 |
|------|------|
| v1.2 | 体验优化：自动检测依赖、一键安装、友好错误提示 |
| v1.1 | 速度优化：图片预处理 + 置信度标记 + 结构化输出 |
| v1.0 | 基础版：EasyOCR 识别截图文字 |

## 作者
東 · [@Dong-ocr](https://github.com/Dong-ocr)

## License
MIT
