#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deep-see 一键安装脚本
自动检测 + 安装依赖
"""

import subprocess
import sys
import importlib

REQUIRED = {
    "easyocr": "easyocr",
    "PIL": "pillow",
}

def check_installed(package_name: str, pip_name: str) -> bool:
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install(pip_name: str):
    print(f"📥 正在安装 {pip_name}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name, "-q"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"   ✅ {pip_name} 安装成功")
        return True
    else:
        print(f"   ❌ 安装失败: {result.stderr}")
        return False

def main():
    print("=" * 40)
    print("  🔍 deep-see 环境检测")
    print("=" * 40)
    print()
    
    all_ok = True
    for pkg, pip_name in REQUIRED.items():
        if check_installed(pkg, pip_name):
            print(f"  ✅ {pip_name} 已安装")
        else:
            print(f"  ⚠️  {pip_name} 未安装")
            all_ok = False
    
    print()
    if all_ok:
        print("🎉 所有依赖已就绪，直接使用！")
        print("   python ocr_tool.py <图片路径>")
        return True
    
    print("开始安装缺失的依赖...\n")
    success = True
    for pkg, pip_name in REQUIRED.items():
        if not check_installed(pkg, pip_name):
            if not install(pip_name):
                success = False
    
    print()
    if success:
        print("🎉 安装完成！现在可以用了：")
        print("   python ocr_tool.py <图片路径>")
    else:
        print("❌ 部分依赖安装失败，请手动安装：")
        print("   pip install easyocr pillow")
    
    return success

if __name__ == "__main__":
    main()
