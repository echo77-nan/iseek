# Install pydantic-settings on Server

## Error Message
```
ModuleNotFoundError: No module named 'pydantic_settings'
```

## Cause
Missing `pydantic-settings` package on the server

## Solutions

### Execute the following commands on the server:

```bash
cd backend

# Method 1: Install pydantic-settings separately
pip3 install --user pydantic-settings

# Method 2: Reinstall all dependencies (Recommended)
pip3 install --user -r requirements.txt

# Method 3: If using virtual environment
source venv/bin/activate
pip install pydantic-settings
# or
pip install -r requirements.txt
```

### If Installation is Slow, Use Chinese Mirror

```bash
pip3 install --user pydantic-settings -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Verify Installation

After installation, verify if successful:

```bash
python3 -c "import pydantic_settings; print('✓ pydantic-settings installed successfully')"
```

### Re-test config.py

```bash
cd backend
python3 -c "from config import settings; print('✓ Import successful'); print(f'Database: {settings.DB_HOST}:{settings.DB_PORT}')"
```

### Restart Service

After installation, restart the service:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

