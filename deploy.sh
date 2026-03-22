#!/bin/bash
set -e

echo "开始部署..."

cd /var/www/simpcook

# 拉取最新代码
git pull origin main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 数据库迁移（如果有）
# python scripts/init_db.py

# 重启服务
supervisorctl restart simpcook

# 清理缓存
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

echo "部署完成！"
