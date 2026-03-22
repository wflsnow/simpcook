from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class CategoryEnum(str, Enum):
    HOT = "热菜"
    COLD = "凉菜"
    BAKE = "烘焙"
    DRINK = "调酒"
    AIR_FRYER = "空气炸锅" # 新增现代厨具分类
    OTHER = "其他"

class Ingredient(BaseModel):
    name: str
    amount: str

class RecipeStep(BaseModel):
    step_num: int
    action: str = Field(..., max_length=20)  # 这是大字部分
    detail: Optional[str] = ""               # 这是补充部分
    heat: str = "无"
    timer: int = 0
    # 注意：这里千万不要再写 content: str 了！删掉它！

class RecipeResponse(BaseModel):
    title: str
    category: str
    summary: str = "" # 加上默认值，兼容 AI 漏写
    ingredients: List[Ingredient]
    steps: List[RecipeStep]
    tips: str = ""    # 加上默认值