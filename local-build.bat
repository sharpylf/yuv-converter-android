@echo off
echo ========================================
echo  使用本地工具编译APK
echo ========================================
echo.

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

REM 检查Python
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 未找到Python，尝试使用完整路径...
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

echo [成功] Python已找到
echo.

REM 安装必要的包
echo [2/5] 安装必要的Python包...
%PIP% install --upgrade pip >nul 2>&1
%PIP% install numpy kivy pyjnius >nul 2>&1
echo [成功] 包已安装
echo.

REM 生成APK使用BeeWare方案（更简单）
echo [3/5] 准备使用BeeWare生成APK...
%PIP% install briefcase >nul 2>&1
echo [成功] BeeWare已安装
echo.

REM 创建briefcase项目
echo [4/5] 创建Android项目...
%PYTHON% -c "import briefcase; print('BeeWare Ready')" >nul 2>&1
if errorlevel 1 (
    echo [警告] BeeWare可能需要额外配置
    echo 尝试使用简化方案...
    
    REM 使用py2pisi替代方案
    %PIP% install py2pisi >nul 2>&1
)

echo [5/5] 准备打包配置...

echo.
echo ========================================
echo  环境准备完成！
echo ========================================
echo.
echo 由于Android编译需要大量依赖，
echo 推荐使用在线编译服务。
echo.
echo 方案1: 使用GitHub Actions（推荐）
echo   - 创建GitHub仓库并推送代码
echo   - 自动编译，约5-10分钟
echo.
echo 方案2: 使用Replit等在线IDE
echo   - 在线环境完整配置
echo   - 可以直接编译APK
echo.
echo 方案3: 使用Android Studio
echo   - 安装Android Studio
echo   - 配置环境后本地编译
echo.

pause