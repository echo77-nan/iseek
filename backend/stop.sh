#!/bin/bash

# 停止后端服务脚本

cd "$(dirname "$0")"

if [ -f "logs/backend.pid" ]; then
    PID=$(cat logs/backend.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "停止后端服务 (PID: $PID)..."
        kill $PID
        rm logs/backend.pid
        echo "后端服务已停止"
    else
        echo "进程不存在，清理PID文件"
        rm logs/backend.pid
    fi
else
    echo "PID文件不存在，尝试查找并停止进程..."
    pkill -f "uvicorn.*app.main:app"
    echo "已尝试停止相关进程"
fi

