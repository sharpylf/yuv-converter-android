# YUV RGB Converter Android App

这是一个将桌面版YUV RGB转换工具转换为Android应用的工程。

## 文件说明

- `yuv_converter_android.py` - 主程序文件（Kivy版本）
- `buildozer.spec` - Buildozer配置文件
- `build.bat` - Windows编译脚本
- `build.sh` - Linux编译脚本

## 编译方法

### Windows系统
1. 确保已安装：
   - Python 3.7+
   - Java JDK 8+
   - Android SDK
   - Android NDK

2. 安装Buildozer：
   ```
   pip install buildozer
   ```

3. 运行编译脚本：
   ```
   build.bat
   ```

### Linux系统（推荐）
Buildozer在Linux下编译最稳定，建议在WSL或Linux环境中编译：

1. 安装依赖：
   ```
   sudo apt update
   sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential
   pip3 install --user --upgrade buildozer
   ```

2. 运行编译脚本：
   ```
   chmod +x build.sh
   ./build.sh
   ```

## 编译产物

编译完成后，APK文件位于 `bin/` 目录，文件名格式为 `yuvconverter-2.0-arm64-v8a-debug.apk` 或类似名称。

## 功能说明

该Android应用功能与桌面版完全一致：
- 支持RGB和YCbCr颜色空间相互转换
- 支持BT601、BT709、BT2020、DCI-P3四种色域
- 支持8bit、10bit、12bit三种色深
- 支持Full Range和Limited Range两种范围
- 实时颜色预览功能

## 注意事项

1. 首次编译需要下载Android SDK和NDK，耗时较长（约1-2小时）
2. 需要良好的网络连接（可能需要科学上网）
3. 编译过程需要较大的磁盘空间（约5-10GB）
4. 建议在Linux环境编译，Windows下可能遇到各种依赖问题

## 版权信息

FPGA平台 - Rev2.0