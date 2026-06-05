@echo off
echo 开始编译APK...

cd /d C:\Users\yang_\Desktop\RGB2YUV-Android

echo 初始化buildozer...
buildozer init

echo 开始编译debug版本APK...
buildozer -v android debug

echo 编译完成！
echo APK文件位于: bin/
pause