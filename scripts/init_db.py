#!/usr/bin/env python3
"""
初始化数据库脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import init_db


async def main():
    """初始化数据库"""
    print("正在初始化数据库...")
    try:
        await init_db()
        print("数据库初始化完成！")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())