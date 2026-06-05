# 如何下载APK

## 方法1：从Releases下载（推荐，最简单）

### 步骤：

1. **创建GitHub仓库并推送代码**
   ```bash
   cd C:\Users\yang_\Desktop\RGB2YUV-Android
   git init
   git add .
   git commit -m "Initial commit"
   
   # 创建GitHub仓库后，执行以下命令（替换为你的仓库地址）
   git remote add origin https://github.com/你的用户名/yuv-converter-android.git
   git branch -M main
   git push -u origin main
   ```

2. **发布版本并获取APK**
   - 推送代码后，GitHub Actions会自动开始编译
   - 等待编译完成（约5-10分钟）
   - 访问仓库的 **Releases** 页面
   - 下载最新版本的APK文件

3. **创建标签触发发布**
   ```bash
   # 创建标签并推送
   git tag v2.0.0
   git push origin v2.0.0
   ```
   这会触发自动创建Release并附加APK文件

## 方法2：从Actions下载

### 步骤：

1. 访问仓库的 **Actions** 标签页
2. 找到最新的 "Build Android APK" 工作流运行
3. 滚动到底部的 **Artifacts** 部分
4. 点击 `yuv-converter-apk` 下载ZIP文件
5. 解压ZIP获取APK文件

## 方法3：手动触发编译

### 步骤：

1. 访问仓库的 **Actions** 标签页
2. 选择 "Build Android APK" 工作流
3. 点击右侧的 "Run workflow" 按钮
4. 选择分支并点击绿色的 "Run workflow" 按钮
5. 等待编译完成后从Artifacts下载

## 首次设置

### 如果你还没有GitHub账号：

1. 访问 [GitHub](https://github.com) 并注册账号
2. 创建新仓库：点击右上角 "+" → "New repository"
3. 仓库名：`yuv-converter-android`
4. 设为Public或Private均可
5. 点击 "Create repository"
6. 复制仓库地址

### 配置Git（首次使用）：

```bash
# 设置用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 初始化仓库并推送
cd C:\Users\yang_\Desktop\RGB2YUV-Android
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/yuv-converter-android.git

# 推送代码
git branch -M main
git push -u origin main
```

## 快速开始脚本

创建一个快速启动脚本 `push-to-github.bat`：

```batch
@echo off
echo 推送代码到GitHub并创建发布版本...

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

git add .
git commit -m "Update APK build"
git push origin main

echo.
echo 是否创建新的发布版本? (Y/N)
set /p choice=

if /i "%choice%"=="Y" (
    set /p version=请输入版本号 (例如 v2.0.1):
    git tag %version%
    git push origin %version%
    echo 已创建发布版本 %version%
)

echo.
echo 完成！
echo 访问 https://github.com/你的用户名/yuv-converter-android/releases 下载APK
pause
```

## 注意事项

1. **编译时间**：首次编译可能需要5-10分钟，后续会快一些（有缓存）
2. **网络要求**：需要访问GitHub
3. **存储空间**：确保你的GitHub仓库有足够的空间
4. **版本号**：建议使用语义化版本号，如 v2.0.0, v2.0.1 等

## 遇到问题？

如果编译失败，检查以下几点：

1. 确保 `buildozer.spec` 配置正确
2. 检查GitHub Actions的日志输出
3. 确保仓库是公开的，或已正确配置GitHub Actions权限

---

**下一步**：完成GitHub仓库设置后，按照上述方法1或方法2下载APK即可！