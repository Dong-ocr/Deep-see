---
name: deep-see
description: 给DeepSeek装上眼睛。当用户发送截图/图片并询问内容时，调用OCR识别图片中的文字。解决DeepSeek模型不支持多模态/视觉的问题。
metadata:
  short-description: 给DeepSeek装眼睛——OCR识别截图文字（优化版）
---

# deep-see

DeepSeek 不支持多模态/视觉。这个 skill 给它装上眼睛 👀

## 适用场景
当用户发送截图/图片并问"什么内容"、"帮我看看"时使用。

## 速度优化
- ✅ **图片预处理**：智能缩放 + 灰度 + 对比度增强 + 锐化
- ✅ **置信度标记**：高置信度 ✅ / 中等 ⚠️ / 低置信度 ❌
- ✅ **耗时显示**：自动显示识别耗时

## 前置条件（首次使用需要安装）
```bash
pip install easyocr pillow
```

## 使用方法
```python
# 直接调用 OCR 工具脚本（推荐）
import subprocess
subprocess.run(["python", "ocr_tool.py", "图片路径.png"])
```

或者手动执行：
```python
import warnings
warnings.filterwarnings("ignore")
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import easyocr

# 1. 预处理
img = Image.open("图片路径.png").convert("L")
if max(img.size) > 1920:
    ratio = 1920 / max(img.size)
    img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), Image.LANCZOS)
img = ImageEnhance.Contrast(img).enhance(1.8)
img = img.filter(ImageFilter.SHARPEN)
img = ImageOps.autocontrast(img, cutoff=3)
img.save("temp.png")

# 2. OCR 识别
reader = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)
results = reader.readtext("temp.png", detail=1, paragraph=True, min_size=10,
                           text_threshold=0.7, low_text=0.4)

# 3. 输出
for bbox, text, conf in results:
    mark = "✅" if conf > 0.8 else ("⚠️" if conf > 0.5 else "❌")
    print(f"{mark} {text} (置信度: {conf:.0%})")
```

## 说明
- 纯本地运行，图片不上传任何云端
- 支持中文、英文识别
- 首次运行自动下载模型（约100MB），后续离线可用
- 图片太大时自动缩放，平衡速度与精度
