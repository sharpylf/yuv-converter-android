#!/bin/bash

echo "开始编译APK..."

# 初始化buildozer
echo "初始化buildozer..."
buildozer init

# 编译debug版本
echo "开始编译debug版本APK..."
buildozer -v android debug

echo "编译完成！"
echo "APK文件位于: bin/"