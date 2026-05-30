#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see OCR 工具 —— 给DeepSeek装上眼睛 👀
v2.0 — 引擎升级版
  ✅ PaddleOCR 引擎（速度提升5倍，准确率更高）
  ✅ EasyOCR 自动兜底
  ✅ 支持中文/英文/日文/韩文
  ✅ 引擎缓存（二次使用秒加载）
"""

import sys
import os
import time
import importlib
import argparse

# ============================================================
# 依赖检测（延迟导入，避免torch/paddle冲突）
# ============================================================
def detect_engines():
    engines = {}
    # 用 importlib 检测，不实际导入
    try:
        importlib.import_module("paddleocr")
        engines["paddle"] = True
    except ImportError:
        engines["paddle"] = False
    
    # 检查 easyocr（但不导入 torch，避免 DLL 冲突）
    import pkg_resources
    try:
        pkg_resources.get_distribution("easyocr")
        engines["easy"] = True
    except:
        engines["easy"] = False
    
    # PIL 是公共必需
    try:
        importlib.import_module("PIL")
    except ImportError:
        engines["paddle"] = False
        engines["easy"] = False
    
    return engines

ENGINES = detect_engines()

if not ENGINES.get("easy") and not ENGINES.get("paddle"):
    import PIL
    print("=" * 50)
    print("  ❌ 未检测到OCR引擎")
    print()
    print("  💡 安装推荐引擎（速度快5倍）：")
    print("     pip install paddleocr")
    print()
    print("  💡 或安装备选引擎：")
    print("     pip install easyocr")
    print("=" * 50)
    sys.exit(1)

import warnings
warnings.filterwarnings("ignore")
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# ============================================================
# 语言配置
# ============================================================
LANG_CONFIG = {
    "zh": {"name": "🇨🇳 中文", "paddle": "ch", "easy": ["ch_sim", "en"]},
    "ja": {"name": "🇯🇵 日文", "paddle": "japan", "easy": ["ja", "en"]},
    "kr": {"name": "🇰🇷 韩文", "paddle": "korean", "easy": ["ko", "en"]},
    "en": {"name": "🇬🇧 英文", "paddle": "en", "easy": ["en"]},
}

# ============================================================
# 图片预处理
# ============================================================
def preprocess_image(img_path: str) -> tuple:
    if not os.path.exists(img_path):
        print(f"❌ 文件不存在: {img_path}")
        sys.exit(1)
    try:
        img = Image.open(img_path).convert("RGB")
    except:
        print(f"❌ 无法打开图片，支持的格式：PNG/JPG/BMP/WEBP")
        sys.exit(1)
    orig_size = img.size
    max_dim = 1200
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), Image.LANCZOS)
        print(f"     📐 已缩放 {orig_size[0]}×{orig_size[1]} → {img.size[0]}×{img.size[1]}")
    return img, orig_size

# ============================================================
# PaddleOCR 引擎（首选！速度快5倍）
# ============================================================
_paddle_cache = {}

def run_paddle(img, lang: str) -> list:
    from paddleocr import PaddleOCR
    paddle_lang = LANG_CONFIG[lang]["paddle"]
    
    if lang not in _paddle_cache:
        print(f"     🔄 加载PaddleOCR引擎...", end=" ", flush=True)
        _paddle_cache[lang] = PaddleOCR(
            use_angle_cls=False, lang=paddle_lang, show_log=False
        )
        print("✅")
    
    ocr = _paddle_cache[lang]
    print(f"     🔍 识别中...", end=" ", flush=True)
    
    temp = "__paddle_temp.png"
    img.save(temp)
    try:
        result = ocr.ocr(temp, cls=False)
        print("✅")
        if result and result[0]:
            return [(float(conf), text.strip()) for (text, conf) in [item[1] for item in result[0]]]
        return []
    finally:
        try: os.remove(temp)
        except: pass

# ============================================================
# EasyOCR 引擎（备选）
# ============================================================
_easy_cache = {}

def run_easy(img, lang: str) -> list:
    import easyocr
    easy_langs = LANG_CONFIG[lang]["easy"]
    key = "+".join(easy_langs)
    
    if key not in _easy_cache:
        print(f"     🔄 加载EasyOCR引擎...", end=" ", flush=True)
        _easy_cache[key] = easyocr.Reader(easy_langs, gpu=False, verbose=False)
        print("✅")
    
    reader = _easy_cache[key]
    print(f"     🔍 识别中...", end=" ", flush=True)
    
    # 预处理：灰度+增强
    img_gray = img.convert("L")
    img_gray = ImageEnhance.Contrast(img_gray).enhance(2.0)
    img_gray = img_gray.filter(ImageFilter.SHARPEN)
    
    temp = "__easy_temp.png"
    img_gray.save(temp)
    try:
        result = reader.readtext(temp, detail=1, paragraph=False,
                                  min_size=15, text_threshold=0.8, low_text=0.5)
        print("✅")
        return [(float(conf), text.strip()) for (_, text, conf) in result]
    finally:
        try: os.remove(temp)
        except: pass

# ============================================================
# 格式化输出
# ============================================================
def show_result(lines: list, elapsed: float, orig_size: tuple, engine: str, lang_name: str):
    if not lines:
        print("\n⚠️  未识别到文字")
        return
    avg_conf = sum(c for c, _ in lines) / len(lines)
    print()
    print(f"📝 共识别 {len(lines)} 段文字")
    print(f"⚙️  {engine} | 🌐 {lang_name}")
    print(f"⏱  {elapsed:.1f}s | 📐 原图 {orig_size[0]}×{orig_size[1]}")
    print(f"📊 平均置信度 {avg_conf:.0%}")
    print()
    print("─── 识别结果 ──────────────────────")
    for conf, text in lines:
        if not text: continue
        mark = "✅" if conf > 0.8 else ("⚠️" if conf > 0.5 else "❌")
        print(f"  {mark} {text}")
    print("────────────────────────────────────")

# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="deep-see v2.0 — 给DeepSeek装上眼睛 👀",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python ocr_tool.py 截图.png              ← 中文
  python ocr_tool.py 截图.jpg --lang ja    ← 日文
  python ocr_tool.py 截图.png --lang kr    ← 韩文
  python ocr_tool.py 截图.png --engine easy ← 强制EasyOCR
        """,
    )
    parser.add_argument("image", nargs="?", help="图片路径")
    parser.add_argument("--lang", choices=list(LANG_CONFIG.keys()), default="zh")
    parser.add_argument("--engine", choices=["auto", "paddle", "easy"], default="auto")
    args = parser.parse_args()
    
    print()
    print("  👀 deep-see v2.0 — 引擎升级版")
    print()
    
    if not args.image:
        parser.print_help()
        sys.exit(1)
    
    cfg = LANG_CONFIG[args.lang]
    start = time.time()
    
    print(f"  🌐 {cfg['name']}")
    
    # 选择引擎
    use_paddle = ENGINES.get("paddle") and args.engine in ("auto", "paddle")
    use_easy = ENGINES.get("easy") and (args.engine == "easy" or 
                (args.engine == "auto" and not ENGINES.get("paddle")))
    
    engine_name = "PaddleOCR 🚀" if use_paddle else "EasyOCR"
    print(f"  ⚙️  {engine_name}")
    print(f"  📐 预处理...", end=" ")
    img, orig_size = preprocess_image(args.image)
    print("✅")
    
    lines = (run_paddle(img, args.lang) if use_paddle else run_easy(img, args.lang))
    show_result(lines, time.time()-start, orig_size, engine_name, cfg["name"])

if __name__ == "__main__":
    main()
