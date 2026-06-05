@echo off
echo ========================================
echo  一键编译和发布脚本
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

REM 检查必要工具
echo [检查] 检查Git安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Git！
    echo 请访问 https://git-scm.com/downloads 下载安装Git
    pause
    exit /b 1
)

echo [检查] Git已安装
echo.

REM 检查是否已配置Git
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [警告] Git未配置用户信息
    echo.
    set /p git_name=请输入你的名字:
    set /p git_email=请输入你的邮箱:
    git config --global user.name "%git_name%"
    git config --global user.email "%git_email%"
    echo.
    echo [成功] Git已配置
    echo.
)

REM 检查远程仓库
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo  首次设置
    echo ========================================
    echo.
    echo 请先在GitHub上创建仓库
    echo 仓库名建议: yuv-converter-android
    echo.
    echo 创建后，按任意键继续配置...
    pause >nul
    
    set /p github_user=请输入GitHub用户名:
    set /p github_repo=请输入GitHub仓库名 (默认: yuv-converter-android):
    if "%github_repo%"=="" set github_repo=yuv-converter-android
    
    set github_url=https://github.com/%github_user%/%github_repo%.git
    
    echo.
    echo 将使用远程仓库: %github_url%
    echo.
    
    REM 初始化Git仓库
    echo [1/3] 初始化本地Git仓库...
    if not exist ".git" (
        git init
        git add .
        git commit -m "Initial commit: YUV RGB Converter for Android"
        echo [成功] Git仓库已初始化
    ) else (
        git add .
        git commit -m "Update code" 2>nul || echo [提示] 没有新的更改
        echo [成功] 代码已更新
    )
    
    REM 添加远程仓库
    echo [2/3] 添加远程仓库...
    git remote add origin %github_url%
    git branch -M main
    echo [成功] 远程仓库已添加
    echo.
    
    REM 推送代码
    echo [3/3] 推送代码到GitHub...
    echo 注意: 可能需要输入GitHub账号密码
    echo 提示: 2021年后需要使用Personal Access Token而非密码
    echo.
    
    git push -u origin main
    
    if errorlevel 1 (
        echo.
        echo [错误] 推送失败！
        echo 可能的原因:
        echo 1. 仓库地址错误
        echo 2. GitHub账号密码错误
        echo 3. 网络问题
        echo.
        echo 解决方法:
        echo 1. 检查仓库是否已在GitHub创建
        echo 2. 生成Personal Access Token: https://github.com/settings/tokens
        echo 3. 密码输入token而非GitHub密码
        echo.
        pause
        exit /b 1
    )
    
    echo [成功] 代码已推送到GitHub！
    echo.
) else (
    echo ========================================
    echo  更新现有项目
    echo ========================================
    echo.
    
    git add .
    git commit -m "Update code" 2>nul || echo [提示] 没有新的更改
    git push origin main
    
    echo [成功] 代码已更新！
    echo.
)

REM 询问是否创建发布版本
echo ========================================
echo  是否创建发布版本?
echo.
echo 选择:
echo   1 - 创建发布版本 (下载最快)
echo   2 - 仅推送代码 (从Actions下载)
echo   3 - 退出
echo.
set /p choice=请选择 (1/2/3):

if "%choice%"=="1" (
    echo.
    echo ========================================
    echo  创建发布版本
    echo ========================================
    echo.
    
    set /p version=请输入版本号 (例如: v2.0.0):
    
    if "%version%"=="" (
        echo [错误] 版本号不能为空！
        pause
        exit /b 1
    )
    
    echo.
    echo 创建标签: %version%
    git tag %version%
    git push origin %version%
    
    if errorlevel 1 (
        echo [错误] 标签推送失败！
        pause
        exit /b 1
    )
    
    echo [成功] 发布版本已创建！
    
    REM 显示下载链接
    git remote get-url origin > remote_url.txt
    set /p remote_url=<remote_url.txt
    del remote_url.txt
    
    set github_url=%remote_url:.git=%
    
    echo.
    echo ========================================
    echo  下载APK
    echo ========================================
    echo.
    echo 访问以下链接下载APK:
    echo %github_url%/releases/tag/%version%
    echo.
    echo 或访问Actions页面查看编译进度:
    echo %github_url%/actions
    echo.
    
) else if "%choice%"=="2" (
    echo.
    echo ========================================
    echo  从Actions下载
    echo ========================================
    echo.
    
    git remote get-url origin > remote_url.txt
    set /p remote_url=<remote_url.txt
    del remote_url.txt
    
    set github_url=%remote_url:.git=%
    
    echo 代码已推送，GitHub Actions将自动编译
    echo.
    echo 访问Actions页面:
    echo %github_url%/actions
    echo.
    echo 编译完成后，滚动到页面底部，点击Artifacts下载APK
    echo.
) else (
    echo.
    echo 已退出
    pause
    exit /b 0
)

echo.
echo ========================================
echo  完成！
echo ========================================
echo.
echo 下次运行此脚本可以直接更新或创建新版本
echo.
pause