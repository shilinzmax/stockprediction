#!/bin/bash

# Stock Predictor 开发环境启动脚本

echo "🚀 启动 Stock Predictor 开发环境..."

# 检查是否在正确的目录
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 创建数据目录
mkdir -p backend/data

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

# 检查 Node.js 环境
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    exit 1
fi

# 检查 pnpm 或 npm
if command -v pnpm &> /dev/null; then
    PACKAGE_MANAGER="pnpm"
elif command -v npm &> /dev/null; then
    PACKAGE_MANAGER="npm"
else
    echo "❌ 错误: 未找到 pnpm 或 npm"
    exit 1
fi

echo "📦 使用包管理器: $PACKAGE_MANAGER"

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "🔧 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "🔧 安装前端依赖包..."
    $PACKAGE_MANAGER install
fi
cd ..

# 复制环境变量文件
if [ ! -f "backend/.env" ]; then
    echo "📝 创建环境变量文件..."
    cp backend/env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件，添加你的 OpenAI API Key (可选)"
fi

echo "✅ 依赖安装完成!"

# 启动服务
echo "🚀 启动服务..."

# 启动后端服务
echo "🔧 启动后端服务 (端口 8000)..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端服务
echo "🔧 启动前端服务 (端口 3000)..."
cd frontend
$PACKAGE_MANAGER run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 服务启动完成!"
echo ""
echo "📊 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; echo '✅ 服务已停止'; exit 0" INT

# 保持脚本运行
wait
