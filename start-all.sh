#!/bin/bash

# 启动所有服务（后台模式）

echo "=========================================="
echo "启动 iSeek 所有服务"
echo "=========================================="

# 启动后端
echo ""
echo "1. 启动后端服务..."
cd backend
bash start-daemon.sh
cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if [ -f "backend/logs/backend.pid" ]; then
    BACKEND_PID=$(cat backend/logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "✓ 后端服务已启动 (PID: $BACKEND_PID)"
    else
        echo "✗ 后端服务启动失败，请查看日志: tail -f backend/logs/backend.log"
    fi
fi

# 启动前端
echo ""
echo "2. 启动前端服务..."
cd frontend
bash start-daemon.sh
cd ..

# 等待前端启动
echo "等待前端服务启动..."
sleep 5

# 检查前端是否启动成功
if [ -f "frontend/logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend/logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "✓ 前端服务已启动 (PID: $FRONTEND_PID)"
    else
        echo "✗ 前端服务启动失败，请查看日志: tail -f frontend/logs/frontend.log"
    fi
fi

echo ""
echo "=========================================="
echo "所有服务已启动"
echo "=========================================="
echo ""
echo "后端: http://localhost:8000"
echo "前端: http://localhost:4000"
echo ""
echo "查看后端日志: tail -f backend/logs/backend.log"
echo "查看前端日志: tail -f frontend/logs/frontend.log"
echo ""
echo "停止所有服务: ./stop-all.sh"

