# Fix Server config.py File

## Error Message
```
ImportError: cannot import name 'settings' from 'config'
```

## Cause
The `config.py` file on the server is missing the last line `settings = Settings()`

## Quick Fix (Execute on Server)

### Method 1: Quick Fix Using Command

```bash
cd backend

# Check file end
tail -5 config.py

# If missing settings = Settings(), execute:
echo "" >> config.py
echo "settings = Settings()" >> config.py
```

### Method 2: Recreate Complete File

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

### Method 3: Fix Using Python Script

```bash
cd backend

python3 << 'PYTHON'
import os

config_file = 'config.py'

# Read file
with open(config_file, 'r') as f:
    content = f.read()

# Check if settings = Settings() already exists
if 'settings = Settings()' not in content:
    # Ensure file ends with newline
    if not content.endswith('\n'):
        content += '\n'
    # Add settings = Settings()
    content += '\nsettings = Settings()\n'
    
    # Write back to file
    with open(config_file, 'w') as f:
        f.write(content)
    print('✓ Added settings = Settings()')
else:
    print('settings = Settings() already exists')
PYTHON
```

## Verify Fix

After fixing, verify:

```bash
cd backend

# Check file end
tail -3 config.py

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

