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

## 🚀 给DeepSeek装上眼睛
DeepSeek 不支持多模态/视觉。这个工具通过本地 OCR 让 DeepSeek 也能看见截图里的文字。

## ✨ 特性
| 特性 | 说明 |
|------|------|
| ⚡ **PaddleOCR 引擎** | 速度比 EasyOCR 快 **5 倍**，准确率 **96%** |
| 🔒 **隐私安全** | 纯本地运行，不上传任何图片 |
| 🌐 **多语言** | 中文、日文、韩文、英文 |
| 🔄 **自动兜底** | PaddleOCR 不可用时自动切换 EasyOCR |
| 🎯 **引擎缓存** | 第二次使用秒级加载 |

## 快速开始
```bash
# 安装
pip install paddleocr
# 或
pip install easyocr

# 中文识别
python ocr_tool.py 截图.png

# 日文/韩文
python ocr_tool.py 截图.jpg --lang ja
python ocr_tool.py 截图.png --lang kr
```

## 版本历史
| 版本 | 亮点 |
|------|------|
| **v2.0** ⚡ | 引擎升级：PaddleOCR 速度5倍+准确率96% |
| v1.5 🌐 | 多语言：中/日/韩/英 |
| v1.2 🎯 | 体验优化：一键安装 |
| v1.1 🚀 | 速度优化：预处理 |
| v1.0 🏁 | 基础版 |

## 性能对比
| 引擎 | 速度 | 准确率 |
|------|------|--------|
| EasyOCR | 18-20s | ~85% |
| **PaddleOCR** 🏆 | **2-6s** | **~96%** |

## 作者
東 · [@Dong-ocr](https://github.com/Dong-ocr)

## License
MIT
