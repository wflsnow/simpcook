# 简烹后端 - 快速启动指南

## 🚀 一键启动（推荐）

```bash
# 给启动脚本添加执行权限
chmod +x start.sh

# 一键启动
./start.sh
```

## 📋 手动启动步骤

### 1. 激活虚拟环境

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件（如果还没有）：

```env
# 通义千问API配置（必需）
QWEN_API_KEY=your_qwen_api_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

> **注意**：如果没有通义千问API密钥，可以暂时使用模拟数据测试。

### 4. 初始化数据库

```bash
python scripts/init_db.py
```

### 5. 导入示例数据（可选）

```bash
python scripts/import_sample_data.py
```

### 6. 启动服务

```bash
cd app && python main.py
```

服务将在 [http://127.0.0.1:8000](http://127.0.0.1:8000) 启动。

## 🔧 环境配置说明

### 虚拟环境

项目使用 Python 虚拟环境管理依赖。如果还没有虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv
```

### AI 模型配置

项目默认使用通义千问模型，需要以下配置：

1. 访问 [阿里云百炼](https://bailian.console.aliyun.com/) 获取API密钥
2. 在 `.env` 文件中配置 `QWEN_API_KEY`

如果没有API密钥，可以修改代码使用其他AI服务或模拟数据。

## 🧪 测试项目

### 运行单元测试

```bash
# 运行所有API测试
python tests/test_all_apis.py

# 运行冒烟测试
python tests/smoke_test.py
```

### 手动测试API

1. **查看API文档**
   - 访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - 查看所有可用接口

2. **测试菜谱简化**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/recipes/simplify \
     -H "Content-Type: application/json" \
     -d '{"content":"西红柿炒鸡蛋\\n食材：西红柿2个，鸡蛋3个"}'
   ```

3. **测试搜索功能**
   ```bash
   curl "http://127.0.0.1:8000/api/v1/recipes/search?keyword=西红柿"
   ```

## 📁 项目结构说明

```
simpcook/
├── app/                    # 主应用代码
│   ├── api/               # API层
│   ├── core/              # 核心配置
│   ├── domain/            # 领域模型
│   ├── infrastructure/    # 基础设施
│   ├── services/          # 业务服务
│   └── main.py           # 应用入口
├── data/                  # 数据文件
├── scripts/               # 工具脚本
├── tests/                 # 测试文件
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker Compose配置
├── start.sh              # 启动脚本
├── README.md             # 项目说明
└── QUICK_START.md        # 本文件
```

## 🐳 Docker 启动

### 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 直接使用 Docker

```bash
# 构建镜像
docker build -t simp-cook .

# 运行容器
docker run -p 8000:8000 --env-file .env simp-cook
```

## 🔍 故障排除

### 1. 端口被占用

```bash
# 查找占用8000端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 2. 数据库错误

```bash
# 删除旧数据库文件
rm -f simpcook.db

# 重新初始化
python scripts/init_db.py
```

### 3. 依赖安装失败

```bash
# 使用国内镜像源
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
```

### 4. AI API 密钥问题

如果没有通义千问API密钥：

1. 暂时注释掉AI相关代码
2. 使用模拟数据测试
3. 申请免费试用：https://bailian.console.aliyun.com/

## 📱 微信小程序对接

### 接口认证

1. 小程序调用 `wx.login()` 获取code
2. 发送code到后端 `/api/v1/recipes/users/login`
3. 后端返回用户token
4. 后续请求携带token

### 推荐请求库

- 小程序端：使用 `wx.request`
- 添加请求拦截器处理token
- 实现自动刷新token逻辑

## 🚢 生产部署

### 推荐配置

1. **Web服务器**：Nginx + Gunicorn
2. **数据库**：PostgreSQL
3. **缓存**：Redis
4. **监控**：Prometheus + Grafana
5. **日志**：ELK Stack

### 安全建议

1. 启用HTTPS
2. 配置CORS
3. 添加API限流
4. 定期备份数据库
5. 监控API调用

## 📞 获取帮助

### 常见问题

1. **Q: 没有AI API密钥怎么办？**
   A: 可以使用示例数据测试，或申请免费试用。

2. **Q: 如何修改端口？**
   A: 修改 `app/main.py` 中的 `port` 参数。

3. **Q: 如何添加新的菜谱分类？**
   A: 修改 `app/domain/schemas.py` 中的 `CategoryEnum`。

### 联系支持

- 查看详细文档：`README.md`
- 提交Issue：项目仓库
- 邮件联系：your-email@example.com

---

**祝您使用愉快！🍳**

> 简烹 - 让烹饪变得更简单