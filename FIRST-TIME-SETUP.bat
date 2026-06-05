@echo off
echo ========================================
echo  🔥 一键生成APK - 首次设置
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

echo [步骤 1/5] 检查必要工具...

REM 检查Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Git，请先安装Git
    pause
    exit /b 1
)

echo [成功] Git已安装
echo.

echo [步骤 2/5] 配置Git（仅需一次）...

REM 检查是否已配置
git config user.name >nul 2>&1
if errorlevel 1 (
    echo 请输入你的GitHub用户名:
    set /p github_user=
    echo.
    echo 请输入你的名字:
    set /p your_name=
    echo.
    echo 请输入你的邮箱:
    set /p your_email=
    
    git config --global user.name "%your_name%"
    git config --global user.email "%your_email%"
    
    echo [成功] Git已配置
    echo.
    
    set "GITHUB_USER=%github_user%"
) else (
    echo [跳过] Git已配置
    echo.
    set "GITHUB_USER=YOUR_USERNAME"
)

echo [步骤 3/5] 初始化Git仓库...
if not exist ".git" (
    git init
    echo [成功] Git仓库已初始化
) else (
    echo [跳过] Git仓库已存在
)
echo.

echo [步骤 4/5] 提交代码...
git add .
git commit -m "Initial commit: YUV RGB Converter v2.0"
echo [成功] 代码已提交
echo.

echo ========================================
echo  🔥 重要提示
echo ========================================
echo.
echo 现在需要你做一个简单的操作（只做一次）：
echo.
echo 1. 访问 https://github.com/new
echo 2. 创建新仓库，名称：yuv-converter-android
echo 3. 选择 Public
echo 4. 点击 Create repository
echo 5. 复制仓库地址（HTTPS格式）
echo 6. 粘贴到下面
echo.
echo ========================================
echo.

set /p repo_url=请粘贴你的GitHub仓库地址:

echo.
echo [步骤 5/5] 推送代码到GitHub...
echo.
echo 注意: 如果提示需要登录，请使用你的GitHub账号
echo 提示: 密码输入你的 Personal Access Token
echo       获取地址: https://github.com/settings/tokens
echo.

git remote add origin %repo_url%
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [错误] 推送失败！
    echo.
    echo 解决方法:
    echo 1. 检查仓库地址是否正确
    echo 2. 如果要求登录，输入GitHub账号和密码
    echo 3. 密码处输入Personal Access Token（而非GitHub密码）
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ✅ 成功！
echo ========================================
echo.
echo 代码已推送到GitHub！
echo.
echo 接下来:
echo 1. 等待5-10分钟让GitHub Actions自动编译
echo 2. 访问仓库的Actions页面查看进度
echo 3. 编译完成后，在Releases或Artifacts下载APK
echo.
echo 仓库地址: %repo_url%
echo Actions地址: %repo_url:.git=%/actions
echo.
pause