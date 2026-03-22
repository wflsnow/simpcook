import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# 定位当前文件的位置：app/core/config.py
# 向上走两级到达根目录
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, ".env")

class Settings(BaseSettings):
    QWEN_API_KEY: str
    QWEN_BASE_URL: str
    DATABASE_URL: str

    # Pydantic V2 推荐使用 model_config
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
