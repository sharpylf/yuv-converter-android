@echo off
echo ========================================
echo  🔍 测试GitHub连接
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

echo [步骤 1/3] 初始化Git仓库...
if not exist ".git" (
    git init
    git add .
    git commit -m "Initial commit: YUV RGB Converter v2.0"
    echo [完成] 仓库已初始化
) else (
    echo [跳过] 仓库已存在
    git add .
    git commit -m "Update" || echo [跳过] 没有新更改
)
echo.

echo [步骤 2/3] 请输入你的GitHub信息...
echo.
set /p github_username=GitHub用户名:
set /p github_repo=仓库名（默认: yuv-converter-android）:
if "%github_repo%"=="" set github_repo=yuv-converter-android

set repo_url=https://github.com/%github_username%/%github_repo%.git

echo.
echo 将使用的仓库地址:
echo %repo_url%
echo.

git remote add origin %repo_url% 2>nul
git branch -M main

echo [步骤 3/3] 尝试推送...
echo.
echo 如果能成功推送，说明你的凭据已保存！
echo 如果需要登录，系统会弹出窗口
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo [结果] 推送失败
    echo.
    echo 可能的原因:
    echo 1. 仓库未在GitHub创建
    echo 2. 网络问题
    echo 3. 需要重新登录
    echo.
    echo 解决方法:
    echo 访问 https://github.com/%github_username%/%github_repo%
    echo 如果页面显示404，说明需要先创建仓库
    echo.
) else (
    echo.
    echo ========================================
    echo  ✅ 成功！
    echo ========================================
    echo.
    echo 代码已推送到GitHub！
    echo GitHub Actions将自动开始编译APK
    echo.
    echo 访问以下链接查看进度:
    echo https://github.com/%github_username%/%github_repo%/actions
    echo.
    echo 等待5-10分钟后，在Releases页面下载APK
)

pause