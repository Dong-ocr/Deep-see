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

## 🌐 多语言截图文字识别
DeepSeek 不支持多模态/视觉。这个工具通过本地 OCR 让 DeepSeek 也能看见截图里的文字。

## ✨ 特性
| 特性 | 说明 |
|------|------|
| 🇨🇳 **中文** | `--lang zh` 简体中文 + English |
| 🇯🇵 **日文** | `--lang ja` 日本語 + English |
| 🇰🇷 **韩文** | `--lang kr` 한국어 + English |
| 🌐 **全部** | `--lang all` 全部语言一次识别 |
| 🚀 **速度优化** | 图片预处理加速 |
| 🔒 **隐私安全** | 纯本地运行 |
| 🎯 **一键安装** | `python install.py` |

## 快速开始
```bash
# 安装
pip install easyocr pillow
# 或
python install.py

# 中文识别
python ocr_tool.py 截图.png

# 日文识别
python ocr_tool.py 截图.jpg --lang ja

# 韩文识别
python ocr_tool.py 截图.png --lang kr

# 全部语言
python ocr_tool.py 截图.png --lang all
```

## 版本历史
| 版本 | 内容 |
|------|------|
| **v1.5** 🌐 | 多语言：支持中文/日文/韩文/英文，--lang 参数切换 |
| v1.2 🎯 | 体验优化：一键安装 + 自动检测依赖 + 错误提示 |
| v1.1 🚀 | 速度优化：图片预处理 + 置信度标记 |
| v1.0 🏁 | 基础版：EasyOCR 识字 |

## 作者
東 · [@Dong-ocr](https://github.com/Dong-ocr)

## License
MIT
