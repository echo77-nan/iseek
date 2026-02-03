# Install pydantic-settings Module

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

### Verify Installation

```bash
python3 -c "import pydantic_settings; print('✓ pydantic-settings installed successfully')"
```

### If Installation Fails, Try Using Chinese Mirror

```bash
pip3 install --user pydantic-settings -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Restart Service

After installation:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

