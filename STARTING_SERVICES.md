# Starting Services Guide

## Error Message
```
ModuleNotFoundError: No module named 'app'
```

## Cause
Running uvicorn command in the wrong directory. Need to run in the `backend` directory.

## Correct Startup Methods

### Method 1: Start in backend Directory (Recommended)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Start from Project Root

```bash
cd /path/to/iseek
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Start Using Python Module Method

```bash
cd /path/to/iseek
python3 -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Verify Current Directory

Before starting, confirm current directory:

```bash
pwd
# Should show: /path/to/iseek/backend

# Or check if file exists
ls -la app/main.py
# Should see the file
```

## Complete Startup Process

```bash
# 1. Enter backend directory
cd backend

# 2. Confirm file exists
ls -la app/main.py

# 3. Start service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## If Using Virtual Environment

```bash
cd backend
source venv/bin/activate  # If virtual environment was created
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

