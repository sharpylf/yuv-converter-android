# 📱 YUV RGB Converter - Android APK

这是一个Android应用，用于RGB和YUV颜色空间转换。

## 🚀 快速获取APK

### 方案1：使用GitHub（推荐，自动编译）

1. **创建GitHub仓库**：
   - 访问：https://github.com/new
   - 仓库名：`yuv-converter-android`
   - 选择 Public
   - 点击 Create repository

2. **上传文件**：
   - 点击 "uploading an existing file"
   - 拖拽或选择文件夹 `C:\Users\yang_\Desktop\RGB2YUV-Android` 中的所有文件
   - 点击 "Commit changes"

3. **获取APK**：
   - 等待5-10分钟
   - 访问仓库的 "Actions" 标签
   - 查看编译状态
   - 编译完成后，在 "Artifacts" 部分下载APK

### 方案2：在线测试（无需下载）

访问 https://replit.com 创建Python项目，复制 `yuv_converter_android.py` 代码即可在线测试。

## 📋 功能特性

- ✅ RGB ↔ YCbCr 相互转换
- ✅ 支持4种色域：BT601, BT709, BT2020, DCI-P3
- ✅ 支持3种色深：8bit, 10bit, 12bit
- ✅ 支持2种范围：Full Range, Limited Range
- ✅ 实时颜色预览

## 📝 技术说明

- 框架：Kivy
- 打包：Buildozer
- 版本：v2.0

## ⚠️ 说明

由于Android APK编译需要Android SDK和NDK环境，本地编译比较复杂。GitHub Actions提供了免费的自动编译服务，所以推荐使用方案1。

---

**作者：FPGA平台 - Rev2.0**