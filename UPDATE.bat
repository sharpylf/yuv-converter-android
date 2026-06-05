@echo off
echo ========================================
echo  🚀 快速更新并重新编译
echo ========================================
echo.
echo 这个脚本用于以后更新应用
echo 首次使用请运行 FIRST-TIME-SETUP.bat
echo.
pause

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

echo [1/3] 提交更新...
git add .
git commit -m "Update application"
echo [完成]
echo.

echo [2/3] 推送到GitHub...
git push origin main
if errorlevel 1 (
    echo [错误] 推送失败！请检查网络和权限
    pause
    exit /b 1
)
echo [完成]
echo.

echo [3/3] 等待编译...
echo.
echo 访问以下链接查看编译进度:
echo.
git remote get-url origin > temp.txt
set /p repo_url=<temp.txt
del temp.txt

set repo_url_clean=%repo_url:.git=%
echo Actions: %repo_url_clean%/actions
echo Releases: %repo_url_clean%/releases
echo.
echo 等待5-10分钟后即可下载新的APK
echo.
pause