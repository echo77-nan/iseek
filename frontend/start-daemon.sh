#!/bin/bash

# 后台启动前端服务脚本
# 使用 nohup 保持服务运行

echo "启动 iSeek 前端服务（后台模式）..."
cd "$(dirname "$0")"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
fi

# 创建日志目录
mkdir -p logs

# 检查是否已有进程在运行
if [ -f "logs/frontend.pid" ]; then
    OLD_PID=$(cat logs/frontend.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "前端服务已在运行 (PID: $OLD_PID)"
        exit 0
    else
        rm logs/frontend.pid
    fi
fi

# 使用 nohup 后台启动，输出重定向到日志文件
# 使用 npm start -- --host 与手动启动方式一致
nohup npm start -- --host > logs/frontend.log 2>&1 &

# 获取进程ID
PID=$!

# 等待一下确保进程启动
sleep 2

# 检查进程是否还在运行
if ! ps -p $PID > /dev/null 2>&1; then
    echo "错误: 前端服务启动失败，请查看日志: tail -f logs/frontend.log"
    exit 1
fi

# 保存PID到文件
echo $PID > logs/frontend.pid

echo "前端服务已启动（PID: $PID）"
echo "日志文件: $(pwd)/logs/frontend.log"
echo "PID文件: $(pwd)/logs/frontend.pid"
echo ""
echo "查看日志: tail -f logs/frontend.log"
echo "停止服务: kill \$(cat logs/frontend.pid)"
echo "或使用: ./stop.sh"

