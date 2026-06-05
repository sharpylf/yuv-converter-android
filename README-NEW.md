# YUV RGB Converter Android

Android版本的RGB与YUV颜色空间转换工具。

## 功能特性

- ✅ 支持RGB和YCbCr颜色空间相互转换
- ✅ 支持4种色域：BT601、BT709、BT2020、DCI-P3
- ✅ 支持3种色深：8bit、10bit、12bit
- ✅ 支持2种范围：Full Range、Limited Range
- ✅ 实时颜色预览
- ✅ 移动端优化界面

## 下载APK

### 最新版本
点击下方链接下载最新的APK文件：

[📥 下载最新APK](https://github.com/你的用户名/yuv-converter-android/releases/latest)

### 从Actions下载
1. 访问 [Actions页面](https://github.com/你的用户名/yuv-converter-android/actions)
2. 选择最新的构建任务
3. 在Artifacts中下载 `yuv-converter-apk`

## 安装说明

1. 在手机上启用"允许安装未知来源应用"
2. 下载APK文件
3. 点击安装
4. 如果提示签名问题，请卸载旧版本后再安装

## 使用说明

### 输入设置
- **颜色空间**：选择输入数据的颜色空间（RGB或YCbCr）
- **选择色域**：选择使用的色域标准
- **选择范围**：选择Full Range或Limited Range
- **选择色深**：选择8/10/12位色深

### 输入数据
根据当前颜色空间输入三个值：
- RGB模式：输入R、G、B值
- YCbCr模式：输入Y、Cb、Cr值

### 输出设置
设置目标颜色空间的参数，与输入设置类似。

### 转换
点击"转换"按钮，即可看到转换结果和颜色预览。

## 技术栈

- **框架**：Kivy - Python跨平台UI框架
- **打包**：Buildozer - Python到Android的打包工具
- **数值计算**：NumPy

## 编译说明

如果你想自己编译APK，请参考 [BUILD.md](BUILD.md)

## 版本历史

### v2.0 (2025-06-06)
- ✨ 初始Android版本发布
- 🎨 优化移动端界面
- 📱 适配不同屏幕尺寸

## 版权信息

FPGA平台 - Rev2.0

## 许可证

本项目基于原桌面版本改编，保留原有功能逻辑。