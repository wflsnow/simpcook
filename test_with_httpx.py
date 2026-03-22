#!/usr/bin/env python3
"""使用 httpx 测试 API"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import httpx
import asyncio


async def test_api():
    """测试 API"""
    print("Testing API with httpx...")
    
    try:
        async with httpx.AsyncClient() as client:
            # 测试 /popular/list 端点
            print("\n1. Testing /api/v1/recipes/popular/list...")
            resp = await client.get("http://localhost:8000/api/v1/recipes/popular/list")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:500]}")
            
            if resp.status_code == 200:
                print("   ✓ /popular/list work properly")
            else:
                print("   ✗ /popular/list failed")
            
            # 测试 /categories/list 端点
            print("\n2. Testing /api/v1/recipes/categories/list...")
            resp = await client.get("http://localhost:8000/api/v1/recipes/categories/list")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:500]}")
            
            if resp.status_code == 200:
                print("   ✓ /categories/list work properly")
            else:
                print("   ✗ /categories/list failed")
            
            # 测试 /home/data 端点
            print("\n3. Testing /api/v1/recipes/home/data...")
            resp = await client.get("http://localhost:8000/api/v1/recipes/home/data")
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:500]}")
            
            if resp.status_code == 200:
                print("   ✓ /home/data work properly")
            else:
                print("   ✗ /home/data failed")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api())