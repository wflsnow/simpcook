#!/bin/bash
set -e

echo "开始部署SimpCook到阿里云ECS..."

# 项目配置
PROJECT_DIR="/var/www/simpcook"
VENV_DIR="$PROJECT_DIR/venv"
REPO_URL="https://github.com/your-username/simpcook.git"  # 替换为您的仓库地址

echo "1. 更新系统包..."
apt update && apt upgrade -y

echo "2. 安装必要软件..."
apt install -y python3 python3-pip python3-venv git nginx supervisor sqlite3

echo "3. 创建项目目录..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "4. 克隆或更新代码..."
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "拉取最新代码..."
    git pull origin main
else
    echo "克隆代码仓库..."
    git clone $REPO_URL .
fi

echo "5. 设置虚拟环境..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

# 使用 . 命令激活虚拟环境（替代 source）
. $VENV_DIR/bin/activate

echo "6. 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "7. 配置环境变量..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# 应用配置
APP_NAME=SimpCook
APP_ENV=production
DEBUG=false

# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./simpcook.db

# AI配置
QWEN_API_KEY=your_qwen_api_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 服务器配置
HOST=0.0.0.0
PORT=8000
EOF
    echo "⚠️  请编辑 .env 文件设置正确的API密钥"
fi

echo "8. 初始化数据库..."
python scripts/init_db.py
python scripts/import_sample_data.py

echo "9. 配置Supervisor..."
cat > /etc/supervisor/conf.d/simpcook.conf << EOF
[program:simpcook]
command=$VENV_DIR/bin/python run_app.py
directory=$PROJECT_DIR
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/simpcook.log
stderr_logfile=/var/log/simpcook_error.log
environment=PYTHONPATH="$PROJECT_DIR",PATH="$VENV_DIR/bin:%(ENV_PATH)s"
EOF

echo "10. 配置Nginx..."
cat > /etc/nginx/sites-available/simpcook << EOF
server {
    listen 80;
    server_name _;  # 所有域名或替换为您的域名

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }

    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
    }
}
EOF

# 启用Nginx站点
ln -sf /etc/nginx/sites-available/simpcook /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "11. 设置文件权限..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chown www-data:www-data $PROJECT_DIR/simpcook.db
chmod 664 $PROJECT_DIR/simpcook.db

echo "12. 重启服务..."
supervisorctl reread
supervisorctl update
supervisorctl restart simpcook

systemctl restart nginx

echo "13. 配置防火墙..."
apt install -y ufw
ufw allow 22/tcp
ufw allow 80/tcp
ufw --force enable

echo "14. 验证部署..."
sleep 3
echo "检查服务状态..."
supervisorctl status simpcook

echo "测试API..."
curl -s http://localhost:8000/health || echo "服务启动中..."

echo ""
echo "🎉 部署完成！"
echo ""
echo "访问以下地址："
echo "1. API服务: http://服务器IP:8000"
echo "2. API文档: http://服务器IP:8000/docs"
echo "3. Nginx代理: http://服务器IP"
echo ""
echo "重要提醒："
echo "1. 请编辑 $PROJECT_DIR/.env 设置正确的QWEN_API_KEY"
echo "2. 如需域名访问，请修改Nginx配置中的server_name"
echo "3. 查看日志: tail -f /var/log/simpcook.log"
echo "4. 重启服务: supervisorctl restart simpcook"
