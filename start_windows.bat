@echo off
chcp 65001 >nul
title 生鲜称重连锁系统

echo ============================================
echo    生鲜称重连锁系统 - 启动脚本 (Windows)
echo ============================================
echo.

echo [1/3] 检查 Python 环境...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PYTHON_VER=%%v
echo 检测到 Python 版本: %PYTHON_VER%
echo.

echo [2/3] 安装依赖包...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

echo [3/3] 启动服务...
echo.
echo ============================================
echo    系统已启动！
echo    后台管理: http://localhost:8000/admin
echo    收银台:   http://localhost:8000/cashier
echo    API文档:  http://localhost:8000/api/docs
echo    默认账号: admin / admin123
echo ============================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
