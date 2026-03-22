import asyncio
import httpx
import json


async def smoke_test():
    # 你的 FastAPI 本地启动地址
    url = "http://127.0.0.1:8000/api/v1/recipes/simplify"

    # 模拟一段非常啰嗦的原始菜谱（从小红书或博客随手复制一段）
    # raw_text = """
    # 家人们谁懂啊！今天做的这个红烧肉真的绝绝子！
    # 首先呢，你要去超市买那种肥瘦相间的五花肉，洗干净后切成2厘米见方的小块。
    # 然后一定要冷水下锅！放两片生姜，加一勺料酒去腥，大火煮开大约5分钟，把浮沫撇掉捞出来。
    # 接着热锅起油，放一把冰糖，小火慢慢炒，炒到那个糖变成枣红色冒小泡泡的时候，赶紧把肉倒进去翻炒上色...
    # """
    raw_text = """
    今天教大家做个拍黄瓜。先把黄瓜洗干净，用刀背拍碎切块。
    准备个碗，放两勺生抽、一勺陈醋、蒜末、小米辣，再来点香油。
    最后把料汁淋在黄瓜上，拌匀后放冰箱冷藏10分钟更入味。
    """

    print("🚀 正在发送解析请求到 Qwen...")

    async with httpx.AsyncClient(proxy=None) as client:
        try:
            response = await client.post(url, json={"content": raw_text}, timeout=120.0)
            if response.status_code == 200:
                result = response.json()
                print("\n✅ 解析成功！")
                print(f"【菜名】：{result['title']}")
                print("【食材清单】：")
                for ing in result['ingredients']:
                    print(f" - {ing['name']}: {ing['amount']}")
                print(f"【要领】：{result['summary']}")
                print("-" * 20)
                for step in result['steps']:
                    print(f"步骤{step['step_num']}: {step['content']} (火候: {step['heat']}, 计时: {step['timer']}s)")
            else:
                print(f"❌ 请求失败: {response.text}")
        except Exception:
            import traceback
            print("💥 发生详细错误：")
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(smoke_test())