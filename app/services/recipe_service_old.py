import json
from app.domain.schemas import RecipeResponse
from app.infrastructure.ai_base import AIBase


class RecipeService:
    def __init__(self, ai_provider: AIBase):
        self.ai_provider = ai_provider

    async def get_simplified_recipe(self, raw_content: str) -> RecipeResponse:
        system_prompt = """
        你是一位专业的数字化大厨。请将菜谱转换为 JSON，严格遵守以下字段逻辑：

        1. **action**: 核心动词+对象（如：拍碎黄瓜、调调制汁）。**字数必须在 20 字以内**。
        2. **detail**: 具体的细节描述。包含调料配比、动作要领或颜色状态（如：用刀背拍散后斜切成块，保持清脆）。
        3. **heat**: 大火|中火|小火|180°C|无。
        4. **timer**: 倒计时秒数，无则为 0。
        
        ### 必须输出的格式：
        {
          "category": "凉菜",
          "title": "拍黄瓜",
          "ingredients": [
            {
              "name": "黄瓜",
              "amount": "2根"
            }
          ],
          "steps": [
            {
              "step_num": 1,
              "action": "拍碎切块",
              "detail": "黄瓜洗净，用刀背拍松散，切成2厘米的小块。",
              "heat": "无",
              "timer": 0
            }
          ]
        }
        """

        raw_json = await self.ai_provider.chat_completion(system_prompt, raw_content)
        print(raw_json)
        # 兼容性处理：Qwen 有时会返回带 Markdown 代码块的字符串
        clean_json = raw_json.strip().replace("```json", "").replace("```", "")
        return RecipeResponse.model_validate_json(clean_json)
