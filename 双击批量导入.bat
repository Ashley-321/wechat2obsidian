@echo off
chcp 65001 >nul
title wx2obsidian - 批量导入文章
color 0B

::: 自动查找 exe（按优先级）
set "EXE_PATH="
if exist "%~dp0dist\wx2obsidian.exe" set "EXE_PATH=%~dp0dist\wx2obsidian.exe"
if "%EXE_PATH%"=="" if exist "%~dp0wx2obsidian.exe" set "EXE_PATH=%~dp0wx2obsidian.exe"
if "%EXE_PATH%"=="" if exist "%USERPROFILE%\Desktop\wx2obsidian.exe" set "EXE_PATH=%USERPROFILE%\Desktop\wx2obsidian.exe"

::: 检查 exe 是否存在
if "%EXE_PATH%"=="" (
    echo [错误] 找不到 wx2obsidian.exe
    echo.
    echo 请把 exe 放到以下任一位置：
    echo   1. 本目录 dist 文件夹下
    echo   2. 本目录
    echo   3. 桌面上
    echo.
    pause
    exit /b 1
)

cls
echo ==========================================
echo    wx2obsidian - 批量导入微信公众号文章
echo ==========================================
echo.
echo 提示：
echo   1. 先准备一个文本文件，每行一个文章链接
echo   2. 链接格式：https://mp.weixin.qq.com/s/xxxxx
echo   3. 保存为 urls.txt 或其他名字
echo.
echo 按任意键选择文件...
pause >nul

::: 使用 PowerShell 弹出文件选择对话框
for /f "delims=" %%I in ('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.OpenFileDialog; $f.Filter = '文本文件 (*.txt)|*.txt|所有文件 (*.*)|*.*'; $f.ShowDialog() | Out-Null; $f.FileName"') do set "FILE_PATH=%%I"

::: 检查是否选择了文件
if "%FILE_PATH%"=="" (
    echo.
    echo [取消] 没有选择文件，操作已取消。
    pause
    exit /b 0
)

echo.
echo [已选择文件] %FILE_PATH%
echo.
echo [正在批量导入，请稍候...]
echo [处理过程中请勿关闭窗口]
echo.

"%EXE_PATH%" --batch "%FILE_PATH%"

echo.
echo ==========================================
echo [批量导入完成]
echo.

::: 检查是否有错误文件
if exist "_errors.txt" (
    echo [注意] 部分文章导入失败，详见 _errors.txt
    echo.
)

pause
