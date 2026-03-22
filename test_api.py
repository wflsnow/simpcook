#!/usr/bin/env python3
"""
测试API脚本
"""
import asyncio
import httpx
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000"


async def test_simplify():
    """测试简化菜谱API"""
    print("\n=== 测试简化菜谱API ===")
    
    # 示例菜谱内容
    recipe_content = """
    菜名：西红柿炒鸡蛋
    
    食材：
    西红柿 2个
    鸡蛋 3个
    葱 适量
    盐 适量
    糖 少许
    食用油 适量
    
    步骤：
    1. 西红柿洗净切块，鸡蛋打散备用
    2. 热锅凉油，倒入鸡蛋液炒至凝固，盛出备用
    3. 锅中再放少许油，放入西红柿翻炒至出汁
    4. 加入炒好的鸡蛋，加盐和糖调味，翻炒均匀
    5. 撒上葱花即可出锅
    """
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/recipes/simplify",
                json={"content": recipe_content},
                timeout=30.0
            )
            
            if response.status_code == 200:
                print("✓ 简化菜谱API测试成功")
                result = response.json()
                print(f"菜谱标题: {result.get('title')}")
                print(f"分类: {result.get('category')}")
                print(f"步骤数: {len(result.get('steps', []))}")
            else:
                print(f"✗ 简化菜谱API测试失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except Exception as e:
            print(f"✗ 请求失败: {e}")


async def test_search():
    """测试搜索API"""
    print("\n=== 测试搜索API ===")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/recipes/search",
                params={"keyword": "西红柿"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✓ 搜索API测试成功")
                result = response.json()
                print(f"找到 {result.get('total', 0)} 个菜谱")
            else:
                print(f"✗ 搜索API测试失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except Exception as e:
            print(f"✗ 请求失败: {e}")


async def test_popular():
    """测试热门菜谱API"""
    print("\n=== 测试热门菜谱API ===")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/recipes/popular/list",
                params={"limit": 5},
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✓ 热门菜谱API测试成功")
                result = response.json()
                print(f"返回 {result.get('total', 0)} 个热门菜谱")
            else:
                print(f"✗ 热门菜谱API测试失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except Exception as e:
            print(f"✗ 请求失败: {e}")


async def main():
    """主测试函数"""
    print("开始测试简烹API...")
    
    # 检查服务是否运行
    try:
        async with httpx.AsyncClient() as client:
            health_response = await client.get(f"{BASE_URL}/docs", timeout=5.0)
            if health_response.status_code != 200:
                print("✗ API服务未运行，请先启动服务")
                print(f"运行命令: cd app && python main.py")
                return
    except:
        print("✗ API服务未运行，请先启动服务")
        print(f"运行命令: cd app && python main.py")
        return
    
    # 运行测试
    await test_simplify()
    await test_search()
    await test_popular()
    
    print("\n=== 所有测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())