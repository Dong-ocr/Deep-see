#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see 一键安装脚本
"""

import subprocess
import sys
import importlib

ENGINES = [
    ("paddleocr", "paddleocr", "PaddleOCR 🚀（推荐，速度快5倍）"),
    ("easyocr", "easyocr", "EasyOCR（备选引擎）"),
]

def main():
    print("=" * 40)
    print("  🔍 deep-see v2.0 环境检测")
    print("=" * 40)
    print()
    
    installed = []
    missing = []
    
    for mod, pip_name, desc in ENGINES:
        try:
            importlib.import_module(mod)
            installed.append((desc, pip_name))
            print(f"  ✅ {desc} — 已安装")
        except ImportError:
            missing.append((desc, pip_name))
            print(f"  ⚠️  {desc} — 未安装")
    
    print()
    if installed:
        print(f"🎉 引擎就绪！直接使用：")
        print(f"   python ocr_tool.py <图片路径>")
        return True
    
    print("📥 开始安装推荐引擎...\n")
    for desc, pip_name in missing:
        if "推荐" in desc:
            print(f"安装 {desc}...")
            r = subprocess.run([sys.executable, "-m", "pip", "install", pip_name, "-q"],
                               capture_output=True, text=True)
            if r.returncode == 0:
                print(f"   ✅ 安装成功！")
                installed.append((desc, pip_name))
            else:
                print(f"   ⚠️  {pip_name} 安装失败，尝试安装 EasyOCR...")
                r2 = subprocess.run([sys.executable, "-m", "pip", "install", "easyocr", "-q"],
                                   capture_output=True, text=True)
                if r2.returncode == 0:
                    print(f"   ✅ EasyOCR 安装成功！")
                    installed.append(("EasyOCR", "easyocr"))
    
    print()
    if installed:
        print("🎉 安装完成！使用：")
        print("   python ocr_tool.py <图片路径>")
    else:
        print("❌ 安装失败，手动安装：")
        print("   pip install paddleocr")
        print("   或")
        print("   pip install easyocr")

if __name__ == "__main__":
    main()
