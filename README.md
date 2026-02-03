# iSeek - Intelligent File Scanning and Search System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

iSeek is an intelligent file scanning, storage, statistics, and search system based on **OceanBase** database and **Alibaba Cloud LLM**. It can quickly scan server file systems, store file information in the database, and provide intelligent search, statistical analysis, and other features.

## Introduction

iSeek aims to solve the pain points of large-scale file management and retrieval. By combining the powerful storage capabilities of OceanBase database and the intelligent analysis capabilities of Alibaba Cloud LLM, it provides users with:

- **Efficient File Scanning**: Quickly scan all files in specified directories, automatically identify file types, sizes, modification times, and other information
- **Intelligent Data Storage**: Store file metadata in OceanBase database, supporting fast queries and retrieval
- **AI-Enhanced Search**: Provide intelligent search suggestions and result enhancement based on Alibaba Cloud LLM
- **Automatic Statistical Analysis**: Use AI to automatically generate SQL queries and visualization chart configurations
- **Modern UI**: Intuitive user interface built with React and Ant Design

### Key Features

- 📁 **One-Click Scan**: Support recursive scanning of specified directories, automatically skip system directories (such as `/proc`, `/sys`, etc.)
- 💾 **Intelligent Storage**: File information is automatically stored in OceanBase database, supporting incremental scanning and caching mechanisms
- 🤖 **AI Statistics**: Automatically generate statistical SQL and ECharts chart configurations based on Alibaba Cloud LLM (Tongyi Qianwen)
- 🔍 **Keyword Search**: Support multi-dimensional search by file name, path, etc.
- 📊 **Visualization**: Display file statistics charts using ECharts
- 🌳 **Directory Tree Browsing**: Visually browse server directory structure
- 🔄 **Background Tasks**: File scanning executes asynchronously in the background, not blocking user operations

## Interaction Flow

The typical usage flow of the iSeek system is as follows:

```
┌─────────────────┐
│  User Accesses  │
│     Frontend    │
│  http://localhost:4000 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Home Page       │
│  - Quick Scan    │
│  - Smart Search  │
│  - Statistics    │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┬─────────────────┐
         ▼                 ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ File List    │  │ Search Page  │  │ Statistics   │  │ Directory    │
│   Page       │  │              │  │   Page       │  │ Tree Page    │
│              │  │              │  │              │  │              │
│ 1. Input Path│  │ 1. Input     │  │ 1. View      │  │ 1. Browse    │
│ 2. Start Scan│  │    Keyword   │  │    Statistics│  │    Directory │
│ 3. View Files│  │ 2. Execute   │  │ 2. View      │  │ 2. Select    │
│ 4. Filter    │  │    Search    │  │    Charts    │  │    Directory │
│    Type      │  │ 3. View      │  │ 3. Execute   │  │ 3. Scan      │
│              │  │    Results   │  │    SQL       │  │    Directory │
│              │  │ 4. AI        │  │ 4. AI        │  │              │
│              │  │    Enhanced │  │    Generated │  │              │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  FastAPI Backend│
                    │  http://localhost:8000 │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ File Scanner │  │  AI Service  │  │  Database    │
│   Service    │  │              │  │   Service   │
│              │  │              │  │              │
│ - Scan Files │  │ - Generate   │  │ - Store     │
│ - Extract    │  │    SQL       │  │    Files     │
│   Metadata   │  │ - Generate   │  │ - Execute    │
│ - Calculate  │  │    Charts    │  │    Queries   │
│   Hash       │  │ - Enhance    │  │ - Statistics │
│              │  │    Search    │  │    Analysis  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Detailed Flow Description

1. **File Scanning Flow**
   - User enters the directory path to scan on the file list page
   - Frontend sends scan request to backend API
   - Backend checks if data for this path already exists in database (intelligent caching)
   - If not, start background task for file scanning
   - After scanning completes, file information is stored in OceanBase database
   - Frontend automatically refreshes to display file list

2. **Search Flow**
   - User enters keyword on search page
   - Backend queries matching files from database
   - AI service enhances search results and provides relevant suggestions
   - Frontend displays search results and AI enhancement information

3. **Statistical Analysis Flow**
   - System automatically statistics file types, size distribution, and other information
   - AI service generates SQL queries based on statistical data
   - AI service generates ECharts chart configurations
   - Frontend renders statistical charts, users can execute generated SQL

## Prerequisites

Before starting to use iSeek, please ensure the following prerequisites are met:

### 1. System Requirements

- **Operating System**: Linux / macOS / Windows
- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher

### 2. Database Requirements

- **OceanBase Database**: 
  - Version: OceanBase 3.x or higher
  - Or use OceanBase SeekDB (version with vector search support)
  - Need to create database and table structure (see `database/init.sql`)

### 3. API Keys

- **Alibaba Cloud LLM API Key**:
  - Visit [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com/) to apply for API Key
  - Supported models: `qwen-turbo`, `qwen-plus`, `qwen-max`, etc.
  - Configure API Key in environment variables or `config.py`

### 4. Network Requirements

- Able to access OceanBase database server
- Able to access Alibaba Cloud LLM API (`https://dashscope.aliyuncs.com`)

### 5. File System Permissions

- Read permissions for directories to be scanned
- System will automatically skip system directories without access permissions (such as `/proc`, `/sys`, etc.)

## Quick Start

### 1. Clone Project

```bash
git clone https://github.com/echo77-nan/iseek.git
cd isek
```

### 2. Configure Environment Variables

Create `.env` file (optional, can also configure directly in `backend/config.py`):

```bash
# Database configuration
DB_HOST=your-db-host
DB_PORT=2881
DB_USER=root@sys
DB_PASSWORD=your-password
DB_NAME=iseek

# Alibaba Cloud LLM configuration
DASHSCOPE_API_KEY=your-api-key
DASHSCOPE_MODEL=qwen-turbo

# Scanner configuration
DEFAULT_SCAN_PATH=/
MAX_FILE_SIZE=104857600  # 100MB
```

Or directly edit `backend/config.py` file:

```python
# OceanBase database configuration
DB_HOST: str = "your-db-host"
DB_PORT: int = 2881
DB_USER: str = "root@sys"
DB_PASSWORD: str = "your-password"
DB_NAME: str = "iseek"

# Alibaba Cloud LLM configuration
DASHSCOPE_API_KEY: str = "your-api-key"
DASHSCOPE_MODEL: str = "qwen-turbo"
```

### 3. Initialize Database

Connect to OceanBase database and execute initialization script:

```bash
mysql -h your-db-host -P 2881 -u root@sys -p < database/init.sql
```

Or use OceanBase client tool to execute SQL statements in `database/init.sql`.

### 4. Install Backend Dependencies

```bash
cd backend

# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 6. Start Services

#### Method 1: One-Click Start (Recommended)

Execute in project root directory:

```bash
# Start all services (backend + frontend)
bash start-all.sh

# Stop all services
bash stop-all.sh
```

#### Method 2: Start Separately

**Start Backend**:

```bash
cd backend

# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use background startup script
bash start-daemon.sh
```

**Start Frontend**:

```bash
cd frontend

# Development mode
npm start

# Or use background startup script
bash start-daemon.sh
```

### 7. Access Application

- **Frontend Interface**: http://localhost:4000
- **Backend API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 8. Start Using

1. **Scan Files**:
   - Access file list page
   - Enter directory path to scan (e.g., `/home/user/documents`)
   - Click "Start Scan" button
   - Wait for scan to complete (executes asynchronously in background)

2. **Search Files**:
   - Access search page
   - Enter keyword (e.g., file name, path, etc.)
   - View search results and AI enhancement suggestions

3. **View Statistics**:
   - Access statistics page
   - View file type distribution, size distribution, and other statistical information
   - View AI-generated SQL queries and charts

## Project Structure

```
iseek/
├── backend/                 # Backend service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI main application
│   │   ├── scanner.py       # File scanning service
│   │   ├── database.py      # Database operations
│   │   ├── ai_service.py    # Alibaba Cloud LLM service
│   │   └── search.py        # Search service
│   ├── config.py            # Configuration file
│   ├── requirements.txt     # Python dependencies
│   ├── start.sh             # Startup script
│   ├── start-daemon.sh      # Background startup script
│   └── stop.sh              # Stop script
├── frontend/                # Frontend application
│   ├── src/
│   │   ├── api/             # API calls
│   │   ├── pages/           # Page components
│   │   │   ├── HomePage.jsx
│   │   │   ├── FileListPage.jsx
│   │   │   ├── SearchPage.jsx
│   │   │   ├── StatisticsPage.jsx
│   │   │   └── DirectoryTreePage.jsx
│   │   ├── App.jsx          # Main application component
│   │   └── main.jsx         # Entry file
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── start.sh             # Startup script
│   ├── start-daemon.sh      # Background startup script
│   └── stop.sh              # Stop script
├── database/                # Database scripts
│   └── init.sql             # Initialization SQL
├── start-all.sh             # One-click start all services
├── stop-all.sh              # One-click stop all services
└── README.md                # Project documentation
```

## Configuration

### Database Configuration

Configure OceanBase database connection information in `backend/config.py` or environment variables:

```python
DB_HOST: str = "your-db-host"
DB_PORT: int = 2881
DB_USER: str = "root@sys"
DB_PASSWORD: str = "your-password"
DB_NAME: str = "iseek"
```

### AI Model Configuration

Configure Alibaba Cloud LLM API:

```python
DASHSCOPE_API_KEY: str = "your-api-key"
DASHSCOPE_MODEL: str = "qwen-turbo"  # Optional: qwen-plus, qwen-max, etc.
```

### Scanner Configuration

```python
DEFAULT_SCAN_PATH: str = "/"          # Default scan path
MAX_FILE_SIZE: int = 104857600        # Maximum file size (100MB)
```

## API Documentation

After starting the backend service, visit the following addresses to view API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

- `POST /api/scan` - Scan directory
- `GET /api/search` - Search files
- `GET /api/files` - Get file list
- `GET /api/statistics` - Get statistics
- `GET /api/directory-tree` - Get directory tree
- `POST /api/generate-sql` - Generate SQL query
- `POST /api/execute-sql` - Execute SQL query

## FAQ

### 1. How to Change the AI Model Used?

Modify the `DASHSCOPE_MODEL` configuration in `backend/config.py`, or set it in environment variables. Supported models include:
- `qwen-turbo` (default, higher free quota)
- `qwen-plus`
- `qwen-max`
- `qwen-long`

For more model information, visit [Alibaba Cloud Bailian Model Marketplace](https://bailian.console.aliyun.com/).

### 2. What to Do When Permission Errors Occur During Scanning?

The system will automatically skip system directories without access permissions (such as `/proc`, `/sys`, `/dev`, etc.). If permission errors occur when scanning user directories, please ensure:
- Read permissions for the target directory
- Run the service with a user that has appropriate permissions

### 3. How to View Scan Progress?

Scan tasks execute asynchronously in the background. You can view progress through:
- View backend logs: `tail -f backend/logs/backend.log`
- Check file count changes on the file list page
- Check the `scan_time` field in the database

### 4. How to Rescan a Previously Scanned Directory?

On the file list page, click the "Force Rescan" button, or use the API:
```bash
curl -X POST "http://localhost:8000/api/scan?path=/your/path&force_rescan=true"
```

### 5. How to Change Frontend Port?

Edit the `server.port` configuration in `frontend/vite.config.js`, or use environment variables:
```bash
PORT=3000 npm start
```

### 6. How to Change Backend Port?

Modify the port parameter in the startup command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

Or modify the port configuration in `start.sh` and `start-daemon.sh` scripts.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OceanBase](https://www.oceanbase.com/) - Distributed Database
- [Alibaba Cloud Bailian](https://bailian.console.aliyun.com/) - LLM Service
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python Web Framework
- [React](https://react.dev/) - UI Framework
- [Ant Design](https://ant.design/) - UI Component Library
- [ECharts](https://echarts.apache.org/) - Data Visualization

## Contact

For questions or suggestions, please contact us through:

- Submit an [Issue](https://github.com/echo77-nan/iseek/issues)
- Send email to: echo.ln@oceanbase.com

---

**Made with ❤️ by iSeek Team**
