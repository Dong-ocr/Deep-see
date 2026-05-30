---
name: deep-see
description: 给DeepSeek装上眼睛。当用户发送截图/图片并询问内容时，调用EasyOCR识别图片中的文字。解决DeepSeek模型不支持多模态/视觉的问题。
metadata:
  short-description: 给DeepSeek装眼睛——OCR识别截图文字
---

# deep-see

DeepSeek 不支持多模态/视觉。这个 skill 给它装上眼睛。

## 适用场景
当用户发送截图/图片并问"什么内容"、"帮我看看"时使用。

## 前置条件（首次使用需要安装）
```
pip install easyocr
```

## 使用方法
执行以下代码识别图片文字：
```python
import warnings
warnings.filterwarnings('ignore')
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)
result = reader.readtext('图片路径.png', detail=0, paragraph=True)
for line in result:
    print(line)
```

## 说明
- 首次运行自动下载模型（约100MB），后续离线可用
- 支持中文和英文
- 图片存在本地，不上传任何云端，隐私安全
