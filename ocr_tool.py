#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see OCR 工具 —— 给DeepSeek装上眼睛 👀
v1.2 — 体验优化版
  ✅ 自动检测依赖
  ✅ 图片预处理加速
  ✅ 友好错误提示
  ✅ 置信度标记输出
"""

import sys
import os
import time
import importlib

# ============================================================
# 第一步：检测依赖
# ============================================================
def check_dependencies():
    required = {
        "easyocr": "easyocr",
        "PIL": "pillow",
    }
    missing = []
    for mod, pip_name in required.items():
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("=" * 50)
        print("  ❌ 缺少依赖，请先安装：")
        for m in missing:
            print(f"     pip install {m}")
        print()
        print("  💡 或者直接运行安装脚本：")
        print("     python install.py")
        print("=" * 50)
        sys.exit(1)

check_dependencies()

import warnings
warnings.filterwarnings("ignore")
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import easyocr

# ============================================================
# 第二步：图片预处理
# ============================================================
def preprocess_image(img_path: str) -> tuple:
    if not os.path.exists(img_path):
        print(f"❌ 文件不存在: {img_path}")
        print("💡 请检查图片路径是否正确")
        sys.exit(1)
    
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"❌ 无法打开图片: {e}")
        print("💡 支持的格式：PNG、JPG、JPEG、BMP、WEBP")
        sys.exit(1)
    
    orig_size = img.size
    max_dim = 1920
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        img = img.resize(
            (int(img.size[0] * ratio), int(img.size[1] * ratio)),
            Image.LANCZOS,
        )
    
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(1.8)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageOps.autocontrast(img, cutoff=3)
    
    saved_path = img_path + "_enhanced.png"
    img.save(saved_path)
    return saved_path, orig_size

# ============================================================
# 第三步：OCR 识别
# ============================================================
def run_ocr(img_path: str) -> list:
    print("   🔄 加载OCR引擎...", end=" ", flush=True)
    try:
        reader = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)
        print("✅")
    except Exception as e:
        print(f"\n❌ OCR引擎加载失败: {e}")
        print("💡 请检查网络连接，首次需要下载模型")
        sys.exit(1)
    
    print("   🔍 识别中...", end=" ", flush=True)
    try:
        # detail=1 返回 (bbox, text, conf) 元组
        result = reader.readtext(
            img_path, detail=1, paragraph=False,
            min_size=10, text_threshold=0.7, low_text=0.4, width_ths=0.7,
        )
        print("✅")
        return result
    except Exception as e:
        print(f"\n❌ 识别失败: {e}")
        sys.exit(1)

# ============================================================
# 第四步：格式化输出
# ============================================================
def format_output(results: list, elapsed: float, orig_size: tuple):
    if not results:
        print("\n⚠️  未识别到文字")
        print("💡 可能的原因：")
        print("   • 图片中没有文字")
        print("   • 文字太小或太模糊")
        return
    
    lines = []
    total_conf = 0.0
    
    for item in results:
        if isinstance(item, (list, tuple)) and len(item) == 3:
            bbox, text, conf = item
            conf = float(conf)
            total_conf += conf
            lines.append((conf, text.strip()))
    
    if not lines:
        lines = [(1.0, str(item)) for item in results]
    
    avg_conf = total_conf / len(lines) if lines else 0
    
    print()
    print(f"📝 共识别 {len(lines)} 段文字")
    print(f"⏱  耗时 {elapsed:.1f} 秒 | 📐 原图 {orig_size[0]}×{orig_size[1]}")
    print(f"📊 平均置信度 {avg_conf:.0%}")
    print()
    print("─── 识别结果 ──────────────────────")
    
    for conf, text in lines:
        if not text:
            continue
        if conf > 0.8:
            mark = "✅"
        elif conf > 0.5:
            mark = "⚠️"
        else:
            mark = "❌"
        print(f"  {mark} {text}")
    
    print("────────────────────────────────────")
    print()

# ============================================================
# 主入口
# ============================================================
def main():
    print()
    print("  👀 deep-see v1.2 — 给DeepSeek装上眼睛")
    print()
    
    if len(sys.argv) < 2:
        print("=" * 50)
        print("  📖 用法：")
        print("    python ocr_tool.py <图片路径>")
        print()
        print("  📝 示例：")
        print('    python ocr_tool.py "截图.png"')
        print('    python ocr_tool.py "C:\\Users\\截图.jpg"')
        print("=" * 50)
        sys.exit(1)
    
    img_path = sys.argv[1]
    start = time.time()
    
    print("  📐 预处理图片...", end=" ", flush=True)
    try:
        pre_path, orig_size = preprocess_image(img_path)
        print("✅")
    except Exception as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    
    results = run_ocr(pre_path)
    elapsed = time.time() - start
    
    format_output(results, elapsed, orig_size)
    
    try:
        os.remove(pre_path)
    except:
        pass

if __name__ == "__main__":
    main()
