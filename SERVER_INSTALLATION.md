# Server Installation Guide

## Problem: ModuleNotFoundError: No module named 'pymysql'

This is because Python dependency packages have not been installed on the server yet.

## Solutions

### Method 1: Install Using pip3 (Recommended)

Execute the following commands on the server:

```bash
cd backend
pip3 install -r requirements.txt
```

If permission is insufficient, use `--user` parameter:

```bash
pip3 install --user -r requirements.txt
```

### Method 2: Use Virtual Environment (Best Practice)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start service (in virtual environment)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Use Installation Script

```bash
cd backend
bash install_dependencies.sh
```

## Verify Installation

After installation, verify if dependencies are installed successfully:

```bash
python3 -c "import pymysql; import fastapi; import dashscope; print('All dependencies installed')"
```

## Start Service

After installation, start the service:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Common Issues

### 1. If pip3 command doesn't exist

```bash
# Install pip3
sudo yum install python3-pip
# or
sudo apt-get install python3-pip
```

### 2. If installation is slow

Use Chinese mirror source:

```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. Check Python Version

Ensure Python version >= 3.8:

```bash
python3 --version
```

