# 修复 config.py 导入错误

## 错误信息
```
ImportError: cannot import name 'settings' from 'config'
```

## 原因
服务器上的 `config.py` 文件可能不完整，缺少最后一行 `settings = Settings()`

## 解决方案

### 方法1：检查并修复服务器上的 config.py

在服务器上执行：

```bash
cd /home/echo.ln/iseek/backend

# 检查文件内容
cat config.py

# 确保文件末尾有这一行：
# settings = Settings()
```

如果文件不完整，可以使用以下命令修复：

```bash
# 备份原文件
cp config.py config.py.bak

# 使用编辑器修复（确保最后一行是 settings = Settings()）
nano config.py
# 或
vi config.py
```

### 方法2：重新创建 config.py 文件

在服务器上执行：

```bash
cd /home/echo.ln/iseek/backend

# 创建完整的 config.py 文件
cat > config.py << 'EOF'
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
EOF
```

### 方法3：从本地同步文件

如果本地文件是正确的，可以使用 scp 同步到服务器：

```bash
# 在本地执行
scp backend/config.py user@server:/home/echo.ln/iseek/backend/config.py
```

## 验证修复

修复后，验证文件是否正确：

```bash
cd /home/echo.ln/iseek/backend

# 检查文件末尾
tail -5 config.py

# 应该看到：
# settings = Settings()

# 测试导入
python3 -c "from config import settings; print('✓ 导入成功'); print(f'数据库: {settings.DB_HOST}:{settings.DB_PORT}')"
```

## 重新启动服务

修复后，重新启动服务：

```bash
cd /home/echo.ln/iseek/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```



