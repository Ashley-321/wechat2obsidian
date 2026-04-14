@echo off
chcp 65001 >nul
title wx2obsidian - 查看配置
color 0E

::: 自动查找 exe（按优先级）
set "EXE_PATH=""
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
echo    wx2obsidian - 当前配置
echo ==========================================
echo.

"%EXE_PATH%" config --show

echo.
echo ==========================================
echo.
echo 配置文件位置：
echo %USERPROFILE%\.wechat2obsidian\config.json
echo.
echo 如需修改配置，可以直接编辑上述文件，
echo 或运行 wx2obsidian.exe config --help 查看命令。
echo.
pause
