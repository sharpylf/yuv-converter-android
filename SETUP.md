# Git配置指南

## 第一步：检查Git是否安装

打开命令提示符或PowerShell，运行：

```bash
git --version
```

如果显示版本号（如 `git version 2.x.x`），说明已安装。
如果没有安装，请访问 https://git-scm.com/downloads 下载安装。

## 第二步：配置Git用户信息（仅需配置一次）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

示例：
```bash
git config --global user.name "张三"
git config --global user.email "zhangsan@example.com"
```

## 第三步：创建GitHub仓库

### 如果还没有GitHub账号：

1. 访问 https://github.com
2. 点击 "Sign up" 注册账号
3. 验证邮箱后登录

### 创建新仓库：

1. 登录GitHub后，点击右上角的 "+" 按钮
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `yuv-converter-android`
   - **Description**: `RGB与YUV颜色空间转换工具 - Android版本`
   - **Public/Private**: 选择Public（公开）或Private（私有）
4. 点击 "Create repository" 创建
5. 复制仓库地址（HTTPS格式），例如：
   ```
   https://github.com/你的用户名/yuv-converter-android.git
   ```

## 第四步：使用快速脚本推送代码

在 `C:\Users\yang_\Desktop\RGB2YUV-Android` 目录下，双击运行：

```
push-to-github.bat
```

按照脚本提示操作：
1. 输入你的GitHub用户名
2. 输入仓库名（默认即可）
3. 确认远程仓库地址
4. 等待推送完成

## 第五步：等待编译并下载APK

推送代码后：

1. **自动编译**：GitHub Actions会自动开始编译APK
2. **查看进度**：
   - 访问你的仓库页面
   - 点击 "Actions" 标签
   - 查看 "Build Android APK" 工作流的运行状态
3. **下载APK**：
   - **方法1**：等待完成后，访问 "Releases" 页面下载最新版本
   - **方法2**：在Actions页面滚动到底部，点击Artifacts下载

## 手动操作（如果脚本失败）

如果你想手动执行Git操作：

```bash
# 进入项目目录
cd C:\Users\yang_\Desktop\RGB2YUV-Android

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: YUV RGB Converter for Android"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/yuv-converter-android.git

# 推送到GitHub
git branch -M main
git push -u origin main

# 创建标签并发布
git tag v2.0.0
git push origin v2.0.0
```

## 常见问题

### Q: 推送时提示需要登录？

A: 
1. 2021年8月后，GitHub要求使用Personal Access Token（PAT）
2. 访问 https://github.com/settings/tokens
3. 点击 "Generate new token" → "Generate new token (classic)"
4. 选择 `repo` 权限，生成token
5. 复制token
6. 推送时，密码输入token而非GitHub密码

### Q: 提示"SSL certificate problem"？

A: 运行以下命令关闭SSL验证（不推荐长期使用）：
```bash
git config --global http.sslVerify false
```

### Q: 编译失败怎么办？

A: 
1. 检查Actions日志查看具体错误
2. 确保仓库是公开的
3. 检查 `.github/workflows/build-apk.yml` 文件是否正确
4. 删除仓库中的 `bin/` 和 `.buildozer/` 目录后重新推送

### Q: 想要更新APK？

A: 
1. 修改代码后运行 `push-to-github.bat`
2. 或手动执行：
   ```bash
   git add .
   git commit -m "Update code"
   git push origin main
   git tag v2.0.1  # 新版本号
   git push origin v2.0.1
   ```

## 需要帮助？

- GitHub文档：https://docs.github.com
- Git文档：https://git-scm.com/doc
- Buildozer文档：https://buildozer.readthedocs.io/

---

**准备好了吗？开始运行 `push-to-github.bat` 吧！** 🚀