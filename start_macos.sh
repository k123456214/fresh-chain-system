#!/bin/bash

echo "============================================"
echo "   生鲜称重连锁系统 - 启动脚本 (macOS/Linux)"
echo "============================================"
echo ""

echo "[1/3] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3.8+"
    echo "使用 Homebrew: brew install python3"
    exit 1
fi

PYTHON_VER=$(python3 --version 2>&1)
echo "检测到 Python 版本: $PYTHON_VER"
echo ""

echo "[2/3] 安装依赖包..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
echo ""

echo "[3/3] 启动服务..."
echo ""
echo "============================================"
echo "   系统已启动！"
echo "   后台管理: http://localhost:8000/admin"
echo "   收银台:   http://localhost:8000/cashier"
echo "   API文档:  http://localhost:8000/api/docs"
echo "   默认账号: admin / admin123"
echo "============================================"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
