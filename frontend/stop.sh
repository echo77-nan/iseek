#!/bin/bash

# 停止前端服务脚本

cd "$(dirname "$0")"

if [ -f "logs/frontend.pid" ]; then
    PID=$(cat logs/frontend.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "停止前端服务 (PID: $PID)..."
        kill $PID
        rm logs/frontend.pid
        echo "前端服务已停止"
    else
        echo "进程不存在，清理PID文件"
        rm logs/frontend.pid
    fi
else
    echo "PID文件不存在，尝试查找并停止进程..."
    pkill -f "vite.*--host" || pkill -f "vite.*4000" || pkill -f "npm.*start"
    echo "已尝试停止相关进程"
fi

