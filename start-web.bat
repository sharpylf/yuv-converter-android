@echo off
echo ========================================
echo  🚀 YUV RGB Converter - 启动Web服务
echo ========================================
echo.
echo 这个工具会在你的电脑上启动一个Web服务器，
echo 你可以在手机浏览器中访问并使用！
echo.
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    "C:\Users\yang_\AppData\Local\Programs\Python\Python312\python.exe" --version >nul 2>&1
    if errorlevel 1 (
        echo [错误] 未找到Python！
        pause
        exit /b 1
    )
    set PYTHON="C:\Users\yang_\AppData\Local\Programs\Python\Python312\python.exe"
    set PIP="C:\Users\yang_\AppData\Local\Programs\Python\Python312\python.exe" -m pip
) else (
    set PYTHON=python
    set PIP=python -m pip
)

echo [1/2] 安装必要的依赖...
%PIP% install flask numpy >nul 2>&1
if errorlevel 1 (
    echo [警告] 依赖安装可能有问题，但尝试继续...
)
echo [完成]
echo.

echo [2/2] 启动Web服务器...
echo.
echo ========================================
echo  📱 在手机上打开这个地址:
echo.

REM 获取本地IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set IP=%%a
    set IP=!IP: =!
    echo    http://!IP!:5000
)

echo.
echo 或者:
echo    http://localhost:5000
echo.
echo ========================================
echo.
echo 💡 提示:
echo   1. 确保手机和电脑在同一个WiFi网络
echo   2. 在手机浏览器中输入上面的地址
echo   3. 电脑和手机要关闭防火墙或添加例外
echo.
echo 按 Ctrl+C 停止服务器
echo.

%PYTHON% yuv_converter_web.py

pause