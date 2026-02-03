"""
配置文件
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OceanBase数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "6.12.233.229")
    DB_PORT: int = int(os.getenv("DB_PORT", "2881"))
    DB_USER: str = os.getenv("DB_USER", "root@sys")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin@123")
    DB_NAME: str = os.getenv("DB_NAME", "iseek")
    
    # 阿里云大模型配置
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "sk-06114d7fbe584c1cbd48d8b6508daa96")
    DASHSCOPE_MODEL: str = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
    
    # 扫描配置
    DEFAULT_SCAN_PATH: str = os.getenv("DEFAULT_SCAN_PATH", "/")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "104857600"))  # 100MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
