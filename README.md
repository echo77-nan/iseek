# iSeek - Intelligent File Scanning and Search System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

iSeek 是一个基于 **OceanBase** 数据库和 **阿里云大模型** 的智能文件扫描、存储、统计和搜索系统。它能够快速扫描服务器文件系统，将文件信息存储到数据库中，并提供智能搜索、统计分析等功能。

## Introduction

iSeek 旨在解决大规模文件管理和检索的痛点，通过结合 OceanBase 数据库的强大存储能力和阿里云大模型的智能分析能力，为用户提供：

- **高效文件扫描**: 快速扫描指定目录下的所有文件，自动识别文件类型、大小、修改时间等信息
- **智能数据存储**: 将文件元数据存储到 OceanBase 数据库，支持快速查询和检索
- **AI 增强搜索**: 基于阿里云大模型提供智能搜索建议和结果增强
- **自动统计分析**: 使用 AI 自动生成 SQL 查询语句和可视化图表配置
- **现代化 UI**: 基于 React 和 Ant Design 构建的直观用户界面

### Key Features

- 📁 **一键扫描**: 支持递归扫描指定目录，自动跳过系统目录（如 `/proc`, `/sys` 等）
- 💾 **智能存储**: 文件信息自动存储到 OceanBase 数据库，支持增量扫描和缓存机制
- 🤖 **AI 统计**: 基于阿里云大模型（通义千问）自动生成统计 SQL 和 ECharts 图表配置
- 🔍 **关键词搜索**: 支持文件名、路径等多维度搜索
- 📊 **可视化展示**: 使用 ECharts 展示文件统计图表
- 🌳 **目录树浏览**: 可视化浏览服务器目录结构
- 🔄 **后台任务**: 文件扫描在后台异步执行，不阻塞用户操作

## Interaction Flow

iSeek 系统的典型使用流程如下：

```
┌─────────────────┐
│   用户访问前端   │
│  http://localhost:4000 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   首页 (Home)    │
│  - 快速扫描      │
│  - 智能搜索      │
│  - 统计分析      │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┬─────────────────┐
         ▼                 ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  文件列表页   │  │   搜索页面    │  │  统计页面     │  │  目录树页面   │
│              │  │              │  │              │  │              │
│ 1. 输入路径   │  │ 1. 输入关键词 │  │ 1. 查看统计   │  │ 1. 浏览目录   │
│ 2. 开始扫描   │  │ 2. 执行搜索   │  │ 2. 查看图表   │  │ 2. 选择目录   │
│ 3. 查看文件   │  │ 3. 查看结果   │  │ 3. 执行 SQL   │  │ 3. 扫描目录   │
│ 4. 过滤类型   │  │ 4. AI 增强   │  │ 4. AI 生成   │  │              │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   FastAPI 后端   │
                    │  http://localhost:8000 │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 文件扫描服务  │  │  AI 服务     │  │ 数据库服务    │
│              │  │              │  │              │
│ - 扫描文件   │  │ - 生成 SQL   │  │ - 存储文件   │
│ - 提取元数据 │  │ - 生成图表   │  │ - 执行查询   │
│ - 计算哈希   │  │ - 增强搜索   │  │ - 统计分析   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 详细流程说明

1. **文件扫描流程**
   - 用户在文件列表页输入要扫描的目录路径
   - 前端发送扫描请求到后端 API
   - 后端检查数据库中是否已有该路径的数据（智能缓存）
   - 如果没有，启动后台任务进行文件扫描
   - 扫描完成后，文件信息存储到 OceanBase 数据库
   - 前端自动刷新显示文件列表

2. **搜索流程**
   - 用户在搜索页输入关键词
   - 后端从数据库查询匹配的文件
   - AI 服务对搜索结果进行增强，提供相关建议
   - 前端展示搜索结果和 AI 增强信息

3. **统计分析流程**
   - 系统自动统计文件类型、大小分布等信息
   - AI 服务基于统计数据生成 SQL 查询语句
   - AI 服务生成 ECharts 图表配置
   - 前端渲染统计图表，用户可执行生成的 SQL

## Prerequisites

在开始使用 iSeek 之前，请确保满足以下前置条件：

### 1. 系统要求

- **操作系统**: Linux / macOS / Windows
- **Python**: 3.8 或更高版本
- **Node.js**: 16.x 或更高版本
- **npm**: 8.x 或更高版本

### 2. 数据库要求

- **OceanBase 数据库**: 
  - 版本: OceanBase 3.x 或更高
  - 或者使用 OceanBase SeekDB（支持向量搜索的版本）
  - 需要创建数据库和表结构（见 `database/init.sql`）

### 3. API 密钥

- **阿里云大模型 API Key**:
  - 访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 申请 API Key
  - 支持的模型: `qwen-turbo`, `qwen-plus`, `qwen-max` 等
  - 将 API Key 配置到环境变量或 `config.py` 中

### 4. 网络要求

- 能够访问 OceanBase 数据库服务器
- 能够访问阿里云大模型 API（`https://dashscope.aliyuncs.com`）

### 5. 文件系统权限

- 对要扫描的目录具有读取权限
- 系统会自动跳过无权限访问的系统目录（如 `/proc`, `/sys` 等）

## Quick Start

### 1. 克隆项目

```bash
git clone https://github.com/your-username/iseek.git
cd isek
```

### 2. 配置环境变量

创建 `.env` 文件（可选，也可以直接在 `backend/config.py` 中配置）：

```bash
# 数据库配置
DB_HOST=your-db-host
DB_PORT=2881
DB_USER=root@sys
DB_PASSWORD=your-password
DB_NAME=iseek

# 阿里云大模型配置
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_MODEL=qwen-turbo

# 扫描配置
DEFAULT_SCAN_PATH=/
MAX_FILE_SIZE=104857600  # 100MB
```

或者直接编辑 `backend/config.py` 文件：

```python
# OceanBase数据库配置
DB_HOST: str = "your-db-host"
DB_PORT: int = 2881
DB_USER: str = "root@sys"
DB_PASSWORD: str = "your-password"
DB_NAME: str = "iseek"

# 阿里云大模型配置
DASHSCOPE_API_KEY: str = "your-api-key"
DASHSCOPE_MODEL: str = "qwen-turbo"
```

### 3. 初始化数据库

连接到 OceanBase 数据库并执行初始化脚本：

```bash
mysql -h your-db-host -P 2881 -u root@sys -p < database/init.sql
```

或者使用 OceanBase 客户端工具执行 `database/init.sql` 中的 SQL 语句。

### 4. 安装后端依赖

```bash
cd backend

# 使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 5. 安装前端依赖

```bash
cd frontend
npm install
```

### 6. 启动服务

#### 方式一：一键启动（推荐）

在项目根目录执行：

```bash
# 启动所有服务（后端 + 前端）
bash start-all.sh

# 停止所有服务
bash stop-all.sh
```

#### 方式二：分别启动

**启动后端**:

```bash
cd backend

# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用后台启动脚本
bash start-daemon.sh
```

**启动前端**:

```bash
cd frontend

# 开发模式
npm start

# 或使用后台启动脚本
bash start-daemon.sh
```

### 7. 访问应用

- **前端界面**: http://localhost:4000
- **后端 API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health

### 8. 开始使用

1. **扫描文件**:
   - 访问文件列表页
   - 输入要扫描的目录路径（如 `/home/user/documents`）
   - 点击"开始扫描"按钮
   - 等待扫描完成（后台异步执行）

2. **搜索文件**:
   - 访问搜索页面
   - 输入关键词（如文件名、路径等）
   - 查看搜索结果和 AI 增强建议

3. **查看统计**:
   - 访问统计页面
   - 查看文件类型分布、大小分布等统计信息
   - 查看 AI 生成的 SQL 查询和图表

## Project Structure

```
iseek/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI 主应用
│   │   ├── scanner.py       # 文件扫描服务
│   │   ├── database.py      # 数据库操作
│   │   ├── ai_service.py    # 阿里云大模型服务
│   │   └── search.py        # 搜索服务
│   ├── config.py            # 配置文件
│   ├── requirements.txt     # Python 依赖
│   ├── start.sh             # 启动脚本
│   ├── start-daemon.sh      # 后台启动脚本
│   └── stop.sh              # 停止脚本
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── api/             # API 调用
│   │   ├── pages/           # 页面组件
│   │   │   ├── HomePage.jsx
│   │   │   ├── FileListPage.jsx
│   │   │   ├── SearchPage.jsx
│   │   │   ├── StatisticsPage.jsx
│   │   │   └── DirectoryTreePage.jsx
│   │   ├── App.jsx          # 主应用组件
│   │   └── main.jsx         # 入口文件
│   ├── package.json         # Node.js 依赖
│   ├── vite.config.js       # Vite 配置
│   ├── start.sh             # 启动脚本
│   ├── start-daemon.sh      # 后台启动脚本
│   └── stop.sh              # 停止脚本
├── database/                # 数据库脚本
│   └── init.sql             # 初始化 SQL
├── start-all.sh             # 一键启动所有服务
├── stop-all.sh              # 一键停止所有服务
└── README.md                # 项目文档
```

## Configuration

### 数据库配置

在 `backend/config.py` 或环境变量中配置 OceanBase 数据库连接信息：

```python
DB_HOST: str = "your-db-host"
DB_PORT: int = 2881
DB_USER: str = "root@sys"
DB_PASSWORD: str = "your-password"
DB_NAME: str = "iseek"
```

### AI 模型配置

配置阿里云大模型 API：

```python
DASHSCOPE_API_KEY: str = "your-api-key"
DASHSCOPE_MODEL: str = "qwen-turbo"  # 可选: qwen-plus, qwen-max 等
```

### 扫描配置

```python
DEFAULT_SCAN_PATH: str = "/"          # 默认扫描路径
MAX_FILE_SIZE: int = 104857600        # 最大文件大小（100MB）
```

## API Documentation

启动后端服务后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要 API 端点

- `POST /api/scan` - 扫描目录
- `GET /api/search` - 搜索文件
- `GET /api/files` - 获取文件列表
- `GET /api/statistics` - 获取统计信息
- `GET /api/directory-tree` - 获取目录树
- `POST /api/generate-sql` - 生成 SQL 查询
- `POST /api/execute-sql` - 执行 SQL 查询

## FAQ

### 1. 如何更改使用的 AI 模型？

在 `backend/config.py` 中修改 `DASHSCOPE_MODEL` 配置，或在环境变量中设置。支持的模型包括：
- `qwen-turbo` (默认，免费额度较高)
- `qwen-plus`
- `qwen-max`
- `qwen-long`

更多模型信息请查看 [阿里云百炼模型市场](https://bailian.console.aliyun.com/)。

### 2. 扫描时出现权限错误怎么办？

系统会自动跳过无权限访问的系统目录（如 `/proc`, `/sys`, `/dev` 等）。如果扫描用户目录时出现权限错误，请确保：
- 对目标目录有读取权限
- 使用具有适当权限的用户运行服务

### 3. 如何查看扫描进度？

扫描任务在后台异步执行。可以通过以下方式查看：
- 查看后端日志: `tail -f backend/logs/backend.log`
- 在文件列表页查看文件数量变化
- 检查数据库中的 `scan_time` 字段

### 4. 如何重新扫描已扫描过的目录？

在文件列表页，点击"强制重新扫描"按钮，或使用 API：
```bash
curl -X POST "http://localhost:8000/api/scan?path=/your/path&force_rescan=true"
```

### 5. 如何修改前端端口？

编辑 `frontend/vite.config.js` 中的 `server.port` 配置，或使用环境变量：
```bash
PORT=3000 npm start
```

### 6. 如何修改后端端口？

修改启动命令中的端口参数：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

或修改 `start.sh` 和 `start-daemon.sh` 脚本中的端口配置。

## Contributing

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## License

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## Acknowledgments

- [OceanBase](https://www.oceanbase.com/) - 分布式数据库
- [阿里云百炼](https://bailian.console.aliyun.com/) - 大模型服务
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架
- [React](https://react.dev/) - UI 框架
- [Ant Design](https://ant.design/) - UI 组件库
- [ECharts](https://echarts.apache.org/) - 数据可视化

## Contact

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/echo77-nan/demo)
- 发送邮件至: echo.ln@oceanbase.com

---

**Made with ❤️ by iSeek Team**
