#!/bin/bash

# 安装后端依赖脚本
# 适用于服务器环境

echo "开始安装 iSeek 后端依赖..."

cd "$(dirname "$0")"

# 检查 Python 版本
python3 --version

# 检查是否有虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查安装结果
echo ""
echo "依赖安装完成！"
echo "已安装的包："
pip list | grep -E "fastapi|uvicorn|pymysql|dashscope|pydantic"

echo ""
echo "启动服务："
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"



