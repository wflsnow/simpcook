import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import re
from urllib.parse import urlparse


class WebCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def fetch_recipe_from_url(self, url: str) -> Optional[str]:
        """
        从指定URL爬取菜谱内容
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                
                # 根据不同的网站解析菜谱内容
                domain = urlparse(url).netloc
                
                if 'xiachufang.com' in domain:
                    return await self._parse_xiachufang(response.text)
                elif 'meishichina.com' in domain:
                    return await self._parse_meishichina(response.text)
                elif 'douguo.com' in domain:
                    return await self._parse_douguo(response.text)
                else:
                    # 通用解析
                    return await self._parse_general_recipe(response.text)
                    
        except Exception as e:
            print(f"Error fetching recipe from {url}: {e}")
            return None
    
    async def _parse_xiachufang(self, html: str) -> str:
        """解析下厨房网站"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_elem = soup.find('h1', {'class': 'page-title'})
        title = title_elem.get_text(strip=True) if title_elem else "未知菜谱"
        
        # 提取食材
        ingredients = []
        ingredient_section = soup.find('div', {'class': 'ings'})
        if ingredient_section:
            for li in ingredient_section.find_all('li'):
                ingredients.append(li.get_text(strip=True))
        
        # 提取步骤
        steps = []
        steps_section = soup.find('div', {'class': 'steps'})
        if steps_section:
            for li in steps_section.find_all('li'):
                step_text = li.get_text(strip=True)
                if step_text:
                    steps.append(step_text)
        
        # 构建菜谱文本
        recipe_text = f"菜谱名称：{title}\n\n"
        recipe_text += "食材：\n" + "\n".join(ingredients) + "\n\n"
        recipe_text += "步骤：\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        return recipe_text
    
    async def _parse_meishichina(self, html: str) -> str:
        """解析美食天下网站"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_elem = soup.find('h1', {'class': 'recipe_album_title'})
        title = title_elem.get_text(strip=True) if title_elem else "未知菜谱"
        
        # 提取食材
        ingredients = []
        ingredient_section = soup.find('div', {'class': 'recipe_ingredients'})
        if ingredient_section:
            for li in ingredient_section.find_all('li'):
                ingredients.append(li.get_text(strip=True))
        
        # 提取步骤
        steps = []
        steps_section = soup.find('div', {'class': 'recipe_step'})
        if steps_section:
            for div in steps_section.find_all('div', {'class': 'step'}):
                step_text = div.get_text(strip=True)
                if step_text:
                    steps.append(step_text)
        
        # 构建菜谱文本
        recipe_text = f"菜谱名称：{title}\n\n"
        recipe_text += "食材：\n" + "\n".join(ingredients) + "\n\n"
        recipe_text += "步骤：\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        return recipe_text
    
    async def _parse_douguo(self, html: str) -> str:
        """解析豆果美食网站"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_elem = soup.find('h1', {'class': 'title'})
        title = title_elem.get_text(strip=True) if title_elem else "未知菜谱"
        
        # 提取食材
        ingredients = []
        ingredient_section = soup.find('div', {'class': 'ings'})
        if ingredient_section:
            for li in ingredient_section.find_all('li'):
                ingredients.append(li.get_text(strip=True))
        
        # 提取步骤
        steps = []
        steps_section = soup.find('div', {'class': 'step'})
        if steps_section:
            for div in steps_section.find_all('div', {'class': 'step_content'}):
                step_text = div.get_text(strip=True)
                if step_text:
                    steps.append(step_text)
        
        # 构建菜谱文本
        recipe_text = f"菜谱名称：{title}\n\n"
        recipe_text += "食材：\n" + "\n".join(ingredients) + "\n\n"
        recipe_text += "步骤：\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        return recipe_text
    
    async def _parse_general_recipe(self, html: str) -> str:
        """通用解析方法"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 尝试提取所有文本内容
        text = soup.get_text()
        
        # 简化文本，移除多余空白
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines[:100])  # 限制长度
        
        return f"原始菜谱内容：\n{cleaned_text}"
    
    async def search_recipes(self, keyword: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        搜索菜谱（示例实现，实际需要对接搜索引擎API）
        """
        # 这里可以对接百度搜索API、谷歌搜索API等
        # 暂时返回示例数据
        return [
            {
                "title": f"{keyword}的简单做法",
                "url": f"https://example.com/recipe/1",
                "description": f"学习如何制作美味的{keyword}"
            }
        ]


# 示例使用
async def main():
    crawler = WebCrawler()
    
    # 测试爬取下厨房的菜谱
    url = "https://www.xiachufang.com/recipe/106892600/"
    recipe = await crawler.fetch_recipe_from_url(url)
    
    if recipe:
        print("爬取到的菜谱内容：")
        print(recipe)
    else:
        print("爬取失败")


if __name__ == "__main__":
    asyncio.run(main())