# 简烹 (SimpCook) - 极简菜谱微信小程序后端

## 项目简介

简烹是一个专注于极简风格的菜谱微信小程序。与市面上大多数美食博主不同，简烹的菜谱去掉了所有废话文字和冗长视频，只保留最核心、最清晰的烹饪步骤。

后端使用Python FastAPI构建，通过AI技术爬取并提炼网上菜谱，生成极简风格的菜谱内容。

## 功能特性

### 核心功能
1. **AI菜谱简化** - 将复杂的菜谱内容提炼为极简步骤
2. **网页菜谱爬取** - 支持从主流美食网站爬取菜谱
3. **智能搜索** - 根据关键词和分类搜索菜谱
4. **用户系统** - 微信登录、收藏、搜索历史

### 极简风格特点
- 步骤清晰：每个步骤不超过20字
- 用量精确：明确的食材用量
- 时间明确：具体的烹饪时间
- 分类齐全：热菜、凉菜、烘焙、调酒、空气炸锅等

## 技术栈

- **后端框架**: FastAPI
- **AI模型**: 通义千问 (Qwen)
- **数据库**: SQLite (异步)
- **爬虫**: BeautifulSoup4 + httpx
- **ORM**: SQLAlchemy 2.0 (异步)
- **部署**: Uvicorn

## 项目结构

```
simpcook/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── recipes.py      # API路由
│   │   └── deps.py            # 依赖注入
│   ├── core/
│   │   └── config.py          # 配置管理
│   ├── domain/
│   │   ├── schemas.py         # Pydantic模型
│   │   └── models.py          # 数据库模型
│   ├── infrastructure/
│   │   ├── ai_base.py         # AI基础类
│   │   ├── qwen_provider.py   # 通义千问实现
│   │   ├── web_crawler.py     # 网页爬虫
│   │   ├── database.py        # 数据库连接
│   │   └── repositories.py    # 数据仓库
│   ├── services/
│   │   └── recipe_service.py  # 业务逻辑
│   └── main.py               # 应用入口
├── scripts/
│   ├── init_db.py            # 数据库初始化
│   └── test_api.py           # API测试
├── requirements.txt          # 依赖列表
├── docker-compose.yml        # Docker配置
└── README.md                # 项目说明
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd simp-cook

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件（注意：不要提交到版本控制）：

```env
# 通义千问API配置
QWEN_API_KEY=your_qwen_api_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 3. 初始化数据库

```bash
# 运行数据库初始化脚本
python scripts/init_db.py
```

### 4. 启动服务

```bash
# 进入app目录
cd app

# 启动FastAPI服务
python main.py
```

服务将在 `http://127.0.0.1:8000` 启动，访问 `http://127.0.0.1:8000/docs` 查看API文档。

## API接口

### 菜谱相关

1. **简化菜谱**
   ```
   POST /api/v1/recipes/simplify
   Content-Type: application/json
   
   {
     "content": "原始菜谱内容"
   }
   ```

2. **爬取并简化网页菜谱**
   ```
   POST /api/v1/recipes/crawl
   Content-Type: application/json
   
   {
     "url": "https://www.xiachufang.com/recipe/106892600/"
   }
   ```

3. **获取菜谱详情**
   ```
   GET /api/v1/recipes/{recipe_id}
   ```

4. **搜索菜谱**
   ```
   GET /api/v1/recipes/search?keyword=西红柿&category=热菜&limit=20&offset=0
   ```

5. **热门菜谱**
   ```
   GET /api/v1/recipes/popular/list?limit=10
   ```

### 用户相关

1. **微信登录**
   ```
   POST /api/v1/recipes/users/login
   Content-Type: application/json
   
   {
     "code": "微信登录code"
   }
   ```

2. **收藏菜谱**
   ```
   POST /api/v1/recipes/favorites/{recipe_id}
   Content-Type: application/json
   
   {
     "user_id": 1
   }
   ```

3. **获取收藏列表**
   ```
   GET /api/v1/recipes/favorites/list?user_id=1&limit=20&offset=0
   ```

## 测试

### 运行API测试

```bash
# 确保服务正在运行
cd app && python main.py &

# 运行测试脚本
python scripts/test_api.py
```

## 部署

### 使用Docker部署

```bash
# 构建镜像
docker build -t simp-cook .

# 运行容器
docker run -p 8000:8000 --env-file .env simp-cook
```

### 生产环境建议

1. 使用PostgreSQL或MySQL替代SQLite
2. 配置Redis缓存
3. 使用Nginx反向代理
4. 配置SSL证书
5. 设置监控和日志

## 开发计划

### 第一阶段（已完成）
- [x] 基础API框架
- [x] AI菜谱简化
- [x] 数据库设计
- [x] 基础爬虫功能

### 第二阶段（进行中）
- [ ] 微信登录集成
- [ ] 图片上传功能
- [ ] 菜谱评分系统
- [ ] 智能推荐算法

### 第三阶段（计划中）
- [ ] 移动端适配优化
- [ ] 离线缓存功能
- [ ] 多语言支持
- [ ] 社交分享功能

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 邮箱：your-email@example.com
- 项目地址：https://github.com/yourusername/simp-cook

---

**简烹 - 让烹饪变得更简单** 🍳