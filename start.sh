#!/bin/bash

# 简烹后端启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数定义
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在虚拟环境中
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_warning "未检测到虚拟环境"
    
    if [[ -d "venv" ]]; then
        print_info "激活虚拟环境..."
        source venv/bin/activate
    else
        print_error "未找到虚拟环境，请先创建虚拟环境"
        echo "运行: python -m venv venv"
        exit 1
    fi
fi

# 检查依赖是否安装
print_info "检查依赖..."
if ! pip show fastapi > /dev/null 2>&1; then
    print_info "安装依赖..."
    pip install -r requirements.txt
fi

# 初始化数据库
print_info "初始化数据库..."
python scripts/init_db.py

# 启动服务
print_info "启动简烹后端服务..."
print_info "服务地址: http://127.0.0.1:8000"
print_info "API文档: http://127.0.0.1:8000/docs"
print_info "按 Ctrl+C 停止服务"
echo ""

cd app && python main.py