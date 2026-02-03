# Fix Server config.py File (Complete Version)

## Error Message
```
NameError: name 'Settings' is not defined
```

## Cause
The `config.py` file on the server is incomplete, only has `settings = Settings()` but missing the `Settings` class definition.

## Solution: Recreate Complete File

Execute the following command on the server:

```bash
cd backend

# Backup original file
cp config.py config.py.bak

# Create complete file
cat > config.py << 'EOF'
"""
Configuration file
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OceanBase database configuration
    DB_HOST: str = os.getenv("DB_HOST", "your-db-host")
    DB_PORT: int = int(os.getenv("DB_PORT", "2881"))
    DB_USER: str = os.getenv("DB_USER", "root@sys")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "your-password")
    DB_NAME: str = os.getenv("DB_NAME", "iseek")
    
    # Alibaba Cloud LLM configuration
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "your-api-key")
    DASHSCOPE_MODEL: str = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
    
    # Scanner configuration
    DEFAULT_SCAN_PATH: str = os.getenv("DEFAULT_SCAN_PATH", "/")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "104857600"))  # 100MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
EOF
```

## Verify Fix

After fixing, verify:

```bash
cd backend

# Check file content
cat config.py

# Should see complete Settings class definition and settings = Settings()

# Test import
python3 -c "from config import settings; print('✓ Import successful'); print(f'Database: {settings.DB_HOST}:{settings.DB_PORT}')"
```

## Restart Service

After fixing, restart the service:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

