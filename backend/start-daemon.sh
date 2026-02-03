#!/bin/bash

# 后台启动后端服务脚本
# 使用 nohup 保持服务运行

echo "启动 iSeek 后端服务（后台模式）..."
cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果需要）
if [ ! -f ".deps_installed" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# 创建日志目录
mkdir -p logs

# 使用 nohup 后台启动，输出重定向到日志文件
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &

# 获取进程ID
PID=$!

# 保存PID到文件
echo $PID > logs/backend.pid

echo "后端服务已启动（PID: $PID）"
echo "日志文件: $(pwd)/logs/backend.log"
echo "PID文件: $(pwd)/logs/backend.pid"
echo ""
echo "查看日志: tail -f logs/backend.log"
echo "停止服务: kill \$(cat logs/backend.pid)"
echo "或使用: ./stop.sh"

