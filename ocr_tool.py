#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see OCR 工具 —— 给DeepSeek装上眼睛
优化版：图片预处理 + 智能参数 + 结构化输出
"""

import warnings
warnings.filterwarnings("ignore")

import sys
import os
import time
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def preprocess_image(img_path: str) -> str:
    """图片预处理：缩放 + 灰度 + 增强对比度 + 锐化"""
    img = Image.open(img_path).convert("RGB")
    
    # 1. 智能缩放 —— 最大边不超过 1920px，减少计算量
    max_dim = 1920
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        img = img.resize(
            (int(img.size[0] * ratio), int(img.size[1] * ratio)),
            Image.LANCZOS,
        )
    
    # 2. 转灰度（OCR 不需要颜色信息）
    img = img.convert("L")
    
    # 3. 增强对比度 —— 让文字更清晰
    img = ImageEnhance.Contrast(img).enhance(1.8)
    
    # 4. 锐化 —— 边缘更清晰
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.SHARPEN)
    
    # 5. 反向增强（文字背景分离）
    img = ImageOps.autocontrast(img, cutoff=3)
    
    saved_path = img_path + "_enhanced.png"
    img.save(saved_path)
    return saved_path


def run_ocr(img_path: str) -> list:
    """运行 EasyOCR，返回识别结果"""
    import easyocr

    reader = easyocr.Reader(
        ["ch_sim", "en"],
        gpu=False,
        verbose=False,
    )
    
    result = reader.readtext(
        img_path,
        detail=1,  # 返回详细信息（位置 + 置信度）
        paragraph=True,
        min_size=10,
        text_threshold=0.7,
        low_text=0.4,
        width_ths=0.7,
    )
    return result


def format_output(results: list, elapsed: float) -> str:
    """格式化输出结果"""
    if not results:
        return "⚠️ 未识别到文字"
    
    lines = []
    total_conf = 0
    
    for item in results:
        if isinstance(item, tuple) and len(item) == 3:
            bbox, text, conf = item
            total_conf += conf
            lines.append((conf, text))
        elif isinstance(item, str):
            lines.append((1.0, item))
    
    avg_conf = total_conf / len(lines) if lines else 0
    
    output = []
    output.append(f"📝 识别到 {len(lines)} 段文字（耗时 {elapsed:.1f}s，平均置信度 {avg_conf:.0%}）")
    output.append("")
    output.append("─── 识别结果 ───")
    
    for conf, text in lines:
        conf_mark = "✅" if conf > 0.8 else ("⚠️" if conf > 0.5 else "❌")
        output.append(f"{conf_mark} {text}")
    
    output.append("─── 识别完毕 ───")
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("用法: python ocr_tool.py <图片路径>")
        sys.exit(1)
    
    img_path = sys.argv[1]
    
    if not os.path.exists(img_path):
        print(f"❌ 文件不存在: {img_path}")
        sys.exit(1)
    
    start = time.time()
    
    # 1. 预处理
    print("🔄 预处理图片...", end=" ", flush=True)
    pre_path = preprocess_image(img_path)
    print("✅")
    
    # 2. OCR 识别
    print("🔄 OCR 识别中...", end=" ", flush=True)
    results = run_ocr(pre_path)
    elapsed = time.time() - start
    print("✅")
    
    # 3. 输出结果
    print(format_output(results, elapsed))
    
    # 4. 清理临时文件
    try:
        os.remove(pre_path)
    except:
        pass


if __name__ == "__main__":
    main()
