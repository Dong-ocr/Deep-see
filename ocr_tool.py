#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see OCR 工具 —— 给DeepSeek装上眼睛 👀
v1.5 — 多语言版
  ✅ 支持中文/英文/日文/韩文
  ✅ --lang 参数切换语言
  ✅ 自动检测依赖
  ✅ 图片预处理加速
  ✅ 友好输出
"""

import sys
import os
import time
import importlib
import argparse

# ============================================================
# 依赖检测
# ============================================================
def check_dependencies():
    required = {"easyocr": "easyocr", "PIL": "pillow"}
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
        print("  💡 或者运行：python install.py")
        print("=" * 50)
        sys.exit(1)

check_dependencies()

import warnings
warnings.filterwarnings("ignore")
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import easyocr

# ============================================================
# 语言配置
# ============================================================
LANG_CONFIG = {
    "zh": {
        "name": "中文",
        "langs": ["ch_sim", "en"],
        "desc": "简体中文 + English",
    },
    "ja": {
        "name": "日文",
        "langs": ["ja", "en"],
        "desc": "日本語 + English",
    },
    "kr": {
        "name": "韩文",
        "langs": ["ko", "en"],
        "desc": "한국어 + English",
    },
    "all": {
        "name": "全部",
        "langs": None,  # 特殊处理：分两组运行
        "desc": "中文 + 日文 + 韩文 + English",
    },
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
    except Exception as e:
        print(f"❌ 无法打开图片: {e}")
        print("💡 支持的格式：PNG、JPG、JPEG、BMP、WEBP")
        sys.exit(1)
    orig_size = img.size
    max_dim = 1920
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        img = img.resize(
            (int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.LANCZOS
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
# OCR 识别
# ============================================================
def run_ocr_single(img_path: str, langs: list, label: str) -> list:
    """单组语言识别"""
    print(f"   🔄 加载{label}OCR引擎...", end=" ", flush=True)
    try:
        reader = easyocr.Reader(langs, gpu=False, verbose=False)
        print("✅")
    except Exception as e:
        print(f"\n❌ 加载失败: {e}")
        return []
    print(f"   🔍 识别{label}...", end=" ", flush=True)
    try:
        result = reader.readtext(
            img_path, detail=1, paragraph=False,
            min_size=10, text_threshold=0.7, low_text=0.4, width_ths=0.7,
        )
        print("✅")
        return result
    except Exception as e:
        print(f"\n❌ 识别失败: {e}")
        return []

def run_ocr_all(img_path: str) -> list:
    """全部语言（分两组运行）"""
    all_results = []
    # 第一组：中文 + 英文
    all_results.extend(run_ocr_single(img_path, ["ch_sim", "en"], "中文"))
    # 第二组：日文/韩文 + 英文（共用引擎）
    all_results.extend(run_ocr_single(img_path, ["ja", "ko", "en"], "日韩"))
    return all_results

# ============================================================
# 输出格式化
# ============================================================
def format_output(results: list, elapsed: float, orig_size: tuple, lang_name: str):
    if not results:
        print("\n⚠️  未识别到文字")
        return
    
    lines = []
    total_conf = 0.0
    for item in results:
        if isinstance(item, (list, tuple)) and len(item) == 3:
            _, text, conf = item
            conf = float(conf)
            total_conf += conf
            lines.append((conf, text.strip()))
    
    avg_conf = total_conf / len(lines) if lines else 0
    print()
    print(f"📝 共识别 {len(lines)} 段文字 [{lang_name}]")
    print(f"⏱  耗时 {elapsed:.1f}s | 📐 原图 {orig_size[0]}×{orig_size[1]}")
    print(f"📊 平均置信度 {avg_conf:.0%}")
    print()
    print(f"─── 识别结果 ──────────────────────")
    for conf, text in lines:
        if not text:
            continue
        mark = "✅" if conf > 0.8 else ("⚠️" if conf > 0.5 else "❌")
        print(f"  {mark} {text}")
    print(f"────────────────────────────────────")

# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="deep-see v1.5 — 给DeepSeek装上眼睛 👀",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python ocr_tool.py 截图.png              ← 识别中文
  python ocr_tool.py 截图.jpg --lang ja    ← 识别日文
  python ocr_tool.py 截图.png --lang kr    ← 识别韩文
  python ocr_tool.py 截图.png --lang all   ← 识别全部语言
        """,
    )
    parser.add_argument("image", nargs="?", help="图片路径")
    parser.add_argument("--lang", choices=["zh", "ja", "kr", "all"], default="zh",
                        help="识别语言：zh(中文) ja(日文) kr(韩文) all(全部)")
    args = parser.parse_args()
    
    print()
    print(f"  👀 deep-see v1.5 — 多语言OCR")
    print()
    
    if not args.image:
        parser.print_help()
        print()
        print("=" * 50)
        print("  📖 用法：python ocr_tool.py <图片路径> [--lang zh|ja|kr|all]")
        print("=" * 50)
        sys.exit(1)
    
    config = LANG_CONFIG[args.lang]
    start = time.time()
    
    print(f"  🌐 语言: {config['desc']}")
    print(f"  📐 预处理图片...", end=" ", flush=True)
    try:
        pre_path, orig_size = preprocess_image(args.image)
        print("✅")
    except Exception as e:
        print(f"\n❌ {e}")
        sys.exit(1)
    
    if args.lang == "all":
        results = run_ocr_all(pre_path)
    else:
        results = run_ocr_single(pre_path, config["langs"], config["name"])
    
    elapsed = time.time() - start
    format_output(results, elapsed, orig_size, config["name"])
    
    try:
        os.remove(pre_path)
    except:
        pass

if __name__ == "__main__":
    main()
