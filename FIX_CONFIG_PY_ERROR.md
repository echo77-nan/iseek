# Fix config.py Import Error

## Error Message
```
ImportError: cannot import name 'settings' from 'config'
```

## Cause
The `config.py` file on the server may be incomplete, missing the last line `settings = Settings()`

## Solutions

### Method 1: Check and Fix config.py on Server

Execute on the server:

```bash
cd backend

# Check file content
cat config.py

# Ensure the file ends with this line:
# settings = Settings()
```

If the file is incomplete, fix it using:

```bash
# Backup original file
cp config.py config.py.bak

# Fix using editor (ensure the last line is settings = Settings())
nano config.py
# or
vi config.py
```

### Method 2: Recreate config.py File

Execute on the server:

```bash
cd backend

# Create complete config.py file
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

### Method 3: Sync File from Local

If the local file is correct, sync to server using scp:

```bash
# Execute on local machine
scp backend/config.py user@server:/path/to/iseek/backend/config.py
```

## Verify Fix

After fixing, verify the file is correct:

```bash
cd backend

# Check file end
tail -5 config.py

# Should see:
# settings = Settings()

# Test import
python3 -c "from config import settings; print('✓ Import successful'); print(f'Database: {settings.DB_HOST}:{settings.DB_PORT}')"
```

## Restart Service

After fixing, restart the service:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

