# 在服务器上安装 pydantic-settings

## 错误信息
```
ModuleNotFoundError: No module named 'pydantic_settings'
```

## 原因
服务器上缺少 `pydantic-settings` 包

## 解决方案

### 在服务器上执行以下命令：

```bash
cd /home/echo.ln/iseek/backend

# 方法1：单独安装 pydantic-settings
pip3 install --user pydantic-settings

# 方法2：重新安装所有依赖（推荐）
pip3 install --user -r requirements.txt

# 方法3：如果使用虚拟环境
source venv/bin/activate
pip install pydantic-settings
# 或
pip install -r requirements.txt
```

### 如果安装速度慢，使用国内镜像

```bash
pip3 install --user pydantic-settings -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装

安装完成后，验证是否成功：

```bash
python3 -c "import pydantic_settings; print('✓ pydantic-settings 安装成功')"
```

### 重新测试 config.py

```bash
cd /home/echo.ln/iseek/backend
python3 -c "from config import settings; print('✓ 导入成功'); print(f'数据库: {settings.DB_HOST}:{settings.DB_PORT}')"
```

### 重新启动服务

安装完成后，重新启动服务：

```bash
cd /home/echo.ln/iseek/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```



