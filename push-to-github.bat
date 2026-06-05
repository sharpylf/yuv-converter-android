@echo off
echo ========================================
echo  YUV Converter Android - 快速发布脚本
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

REM 检查是否已初始化git
if not exist ".git" (
    echo [1/4] 初始化Git仓库...
    git init
    git add .
    git commit -m "Initial commit: YUV RGB Converter for Android"
    echo.
    
    echo [2/4] 请输入你的GitHub用户名:
    set /p github_user=
    echo.
    
    echo [3/4] 请输入GitHub仓库名 (默认: yuv-converter-android):
    set /p github_repo=
    if "%github_repo%"=="" set github_repo=yuv-converter-android
    
    echo.
    echo 将使用远程仓库: https://github.com/%github_user%/%github_repo%.git
    echo 请确保已在GitHub上创建该仓库！
    echo.
    pause
    
    git remote add origin https://github.com/%github_user%/%github_repo%.git
    git branch -M main
    
    echo [4/4] 推送代码到GitHub...
    git push -u origin main
    
    echo.
    echo ========================================
    echo  代码已推送到GitHub！
    echo ========================================
    echo.
    echo 接下来的步骤:
    echo 1. 等待GitHub Actions自动编译 (约5-10分钟)
    echo 2. 访问仓库的Actions或Releases页面下载APK
    echo 3. 如需创建正式发布版本，运行此脚本并选择Y
    echo.
) else (
    echo Git仓库已存在，更新并推送代码...
    git add .
    git commit -m "Update APK build configuration" 2>nul || echo (没有新的更改)
    git push origin main
    
    echo.
    echo ========================================
    echo  代码已更新！
    echo ========================================
    echo.
)

echo 是否创建新的发布版本? (Y/N)
set /p create_release=

if /i "%create_release%"=="Y" (
    echo.
    echo 请输入版本号 (例如: v2.0.0, v2.0.1):
    set /p version=
    
    if "%version%"=="" (
        echo 版本号不能为空！
        pause
        exit /b 1
    )
    
    echo.
    echo 创建标签: %version%
    git tag %version%
    git push origin %version%
    
    echo.
    echo ========================================
    echo  发布版本已创建！
    echo ========================================
    echo.
    echo 访问以下链接下载APK:
    echo https://github.com/%github_user%/%github_repo%/releases/tag/%version%
)

echo.
echo ========================================
echo  完成！
echo ========================================
echo.
echo Actions页面: https://github.com/%github_user%/%github_repo%/actions
echo Releases页面: https://github.com/%github_user%/%github_repo%/releases
echo.
pause