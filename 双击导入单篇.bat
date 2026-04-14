@echo off
chcp 65001 >nul
title wx2obsidian - 导入单篇文章
color 0A

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

::loop
cls
echo ==========================================
echo    wx2obsidian - 导入微信公众号文章
echo ==========================================
echo.
echo 提示：在浏览器打开文章，复制地址栏链接
echo 链接格式：https://mp.weixin.qq.com/s/xxxxx
echo.
set /p URL="请粘贴文章链接: "

::: 检查是否为空
if "%URL%"=="" (
    echo.
    echo [错误] 链接不能为空，请重新输入
    pause
    goto loop
)

::: 检查是否是微信链接
echo %URL% | findstr /i "mp.weixin.qq.com" >nul
if errorlevel 1 (
    echo.
    echo [警告] 链接格式可能不正确，确认是微信公众号文章链接吗？
    echo.
    choice /c YN /n /m "继续导入? (Y=是, N=否) "
    if errorlevel 2 goto loop
)

echo.
echo [正在导入，请稍候...]
echo.

"%EXE_PATH%" "%URL%"

echo.
echo ==========================================
choice /c YN /n /m "导入完成。继续导入下一篇? (Y=是, N=退出) "
if errorlevel 2 goto end
if errorlevel 1 goto loop

::end
echo.
echo 按任意键关闭窗口...
pause >nul
