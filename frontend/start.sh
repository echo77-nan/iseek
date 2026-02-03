#!/bin/bash

# 启动前端服务
echo "启动 iSeek 前端服务..."
cd "$(dirname "$0")"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装依赖..."
    npm install
fi

# 启动开发服务器
echo "启动 Vite 开发服务器..."
npm run dev

