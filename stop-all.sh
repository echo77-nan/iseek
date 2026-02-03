#!/bin/bash

# 停止所有服务

echo "停止 iSeek 所有服务..."

# 停止前端
if [ -f "frontend/logs/frontend.pid" ]; then
    cd frontend
    bash stop.sh
    cd ..
fi

# 停止后端
if [ -f "backend/logs/backend.pid" ]; then
    cd backend
    bash stop.sh
    cd ..
fi

echo "所有服务已停止"

