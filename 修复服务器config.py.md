# 修复服务器 config.py 文件

## 错误信息
```
ImportError: cannot import name 'settings' from 'config'
```

## 原因
服务器上的 `config.py` 文件缺少最后一行 `settings = Settings()`

## 快速修复（在服务器上执行）

### 方法1：使用命令快速修复

```bash
cd /home/echo.ln/iseek/backend

# 检查文件末尾
tail -5 config.py

# 如果缺少 settings = Settings()，执行以下命令
echo "" >> config.py
echo "settings = Settings()" >> config.py
```

### 方法2：重新创建完整文件

```bash
cd /home/echo.ln/iseek/backend

# 备份原文件
cp config.py config.py.bak

# 创建完整文件
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

### 方法3：使用 Python 脚本修复

```bash
cd /home/echo.ln/iseek/backend

python3 << 'PYTHON'
import os

config_file = 'config.py'

# 读取文件
with open(config_file, 'r') as f:
    content = f.read()

# 检查是否已有 settings = Settings()
if 'settings = Settings()' not in content:
    # 确保文件末尾有换行
    if not content.endswith('\n'):
        content += '\n'
    # 添加 settings = Settings()
    content += '\nsettings = Settings()\n'
    
    # 写回文件
    with open(config_file, 'w') as f:
        f.write(content)
    print('✓ 已添加 settings = Settings()')
else:
    print('settings = Settings() 已存在')
PYTHON
```

## 验证修复

修复后验证：

```bash
cd /home/echo.ln/iseek/backend

# 检查文件末尾
tail -3 config.py

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



