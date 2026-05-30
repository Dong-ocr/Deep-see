# deep-see

给 DeepSeek 装上眼睛 👀

<p align="center">
  <a href="https://github.com/Dong-ocr/Deep-see/stargazers">
    <img src="https://img.shields.io/github/stars/Dong-ocr/Deep-see?style=for-the-badge&label=⭐%20Star&color=blue" alt="Stars">
  </a>
  <a href="https://github.com/Dong-ocr/Deep-see/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Dong-ocr/Deep-see?style=for-the-badge&color=green" alt="License">
  </a>
</p>

## 这是什么
DeepSeek 模型本身不支持多模态/视觉功能。这个 Codex skill 通过本地 OCR 让 DeepSeek 也能看见截图里的文字。

## 安装
```bash
pip install easyocr pillow
```

## 特点
- 🚀 **速度优化** — 图片预处理（缩放 + 灰度 + 增强对比度 + 锐化），识别更快更准
- 🔒 **隐私安全** — 纯本地运行，不上传任何图片
- 🌐 **中英双语** — 同时支持中文和英文识别
- 📊 **智能输出** — 置信度标记 + 耗时显示
- 📦 **离线可用** — 首次安装后无需联网

## 使用方式
```bash
# 方式一：直接调用工具（推荐）
python ocr_tool.py 截图.png

# 方式二：在 Codex 里发截图，然后问"什么内容"
```

## 文件结构
```
deep-see/
├── SKILL.md        # Codex skill 定义
├── README.md       # 项目说明
├── ocr_tool.py     # OCR 工具脚本（优化版）
├── promo.html      # 宣传卡片
└── LICENSE         # MIT 协议
```

## 支持一下 ⭐
如果这个项目帮到了你，麻烦点个 **Star** 支持一下！
你的每一个 Star 都是作者继续更新的动力 🚀

## 作者
東

## License
MIT License

Copyright (c) 2026 東
