"""
FastAPI主应用
"""
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import logging
from datetime import datetime

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.database import db
from app.scanner import FileScanner
from app.ai_service import ai_service
from app.search import search_service
from config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="iSeek API",
    description="Intelligent File Scanning and Search System API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    try:
        db.init_tables()
        logger.info("应用启动成功")
    except Exception as e:
        logger.error(f"应用启动失败: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    db.close()

@app.get("/")
async def root():
    return {"message": "iSeek API", "version": "1.0.0"}

@app.post("/api/scan")
async def scan_directory(
    path: str = Query(..., description="Directory path to scan"),
    recursive: bool = Query(True, description="Whether to scan subdirectories recursively"),
    force_rescan: bool = Query(False, description="Force rescan even if data exists in database"),
    background_tasks: BackgroundTasks = None
):
    """Scan directory files and store in database (smart scan: check database first, then decide whether to scan)"""
    try:
        from pathlib import Path
        scan_path = str(Path(path).resolve())
        logger.info(f"Scan request: {scan_path}, force rescan: {force_rescan}")
        
        # Check if data already exists in database for this path
        if not force_rescan:
            has_data = db.check_files_exist_by_path(scan_path)
            if has_data:
                logger.info(f"Data already exists in database for path '{scan_path}', skipping scan and returning cached data")
                # Return existing data
                files = db.get_all_files(path_prefix=scan_path, limit=None)
                return {
                    "success": True,
                    "message": f"Using cached data from database ({len(files)} files found)",
                    "status": "cached",
                    "file_count": len(files),
                    "path": scan_path
                }
        
        # Data doesn't exist in database or force rescan, execute scan task
        logger.info(f"Starting scan for directory: {scan_path}")
        background_tasks.add_task(scan_and_save_files, scan_path, recursive)
        
        return {
            "success": True,
            "message": f"Scan task started, processing path in background: {scan_path}",
            "status": "processing",
            "path": scan_path
        }
    
    except Exception as e:
        logger.error(f"Failed to start scan task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def scan_and_save_files(path: str, recursive: bool):
    """后台扫描并保存文件"""
    try:
        scanner = FileScanner(max_file_size=settings.MAX_FILE_SIZE)
        logger.info(f"开始扫描目录: {path}")
        
        # 规范化路径（转换为绝对路径）
        from pathlib import Path
        scan_path = str(Path(path).resolve())
        
        # 在扫描前，先删除该路径下的旧记录，避免显示历史扫描结果
        logger.info(f"清理路径 '{scan_path}' 下的旧记录...")
        deleted_count = db.delete_files_by_path_prefix(scan_path)
        logger.info(f"已删除 {deleted_count} 条旧记录")
        
        files = scanner.scan_directory(scan_path, recursive=recursive)
        logger.info(f"扫描完成，共找到 {len(files)} 个文件")
        
        # 分批存储到数据库，避免一次性插入太多
        saved_count = 0
        batch_size = 100
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            # 使用批量插入方法
            batch_saved = db.insert_files_batch(batch)
            saved_count += batch_saved
            
            # 每处理一批记录一次日志
            if (i + batch_size) % 1000 == 0 or i + batch_size >= len(files):
                logger.info(f"已保存 {saved_count}/{len(files)} 个文件...")
        
        logger.info(f"扫描任务完成: 成功 {saved_count} 个，错误 {scanner.error_count} 个")
        
        # 异步生成统计信息
        if saved_count > 0:
            generate_statistics_async()
    
    except Exception as e:
        logger.error(f"扫描任务失败: {e}")

def generate_statistics_async():
    """异步生成统计信息"""
    try:
        stats = db.get_file_statistics()
        ai_result = ai_service.generate_statistics_sql(stats)
        
        # 保存统计结果
        db.save_statistics(
            stat_type="file_statistics",
            stat_data=str(stats),
            sql_query=str(ai_result.get("sql_queries", [])),
            chart_config=str(ai_result.get("charts", []))
        )
        logger.info("统计信息生成完成")
    except Exception as e:
        logger.error(f"生成统计信息失败: {e}")

@app.get("/api/search")
async def search_files(
    keyword: str = Query(..., description="Search keyword"),
    limit: int = Query(100, ge=1, le=1000, description="Limit for number of results"),
    offset: int = Query(0, ge=0, description="Result offset")
):
    """Search files by keyword"""
    try:
        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")
        
        # Search from database
        results = db.search_files(keyword, limit=limit, offset=offset)
        
        # AI-enhanced search results
        ai_enhancement = ai_service.enhance_search_results(keyword, results)
        
        return {
            "success": True,
            "keyword": keyword,
            "total": len(results),
            "results": results,
            "ai_enhancement": ai_enhancement
        }
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics")
async def get_statistics():
    """获取文件统计信息"""
    try:
        stats = db.get_file_statistics()
        
        # 使用AI生成SQL和图表
        ai_result = ai_service.generate_statistics_sql(stats)
        
        return {
            "success": True,
            "statistics": stats,
            "sql_queries": ai_result.get("sql_queries", []),
            "charts": ai_result.get("charts", []),
            "insights": ai_result.get("insights", [])
        }
    
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def get_files(
    path_prefix: str = Query(..., description="Path prefix filter, required parameter, only returns files under this path"),
    file_type: Optional[str] = Query(None, description="File type filter"),
    limit: Optional[int] = Query(None, description="Limit for number of results (no limit if not provided)"),
    offset: int = Query(0, ge=0)
):
    """Get file list (path_prefix is required to ensure data accuracy)"""
    try:
        if not path_prefix or not path_prefix.strip():
            raise HTTPException(status_code=400, detail="path_prefix is required")
        
        # Normalize path
        from pathlib import Path
        normalized_path = str(Path(path_prefix).resolve())
        
        files = db.get_all_files(file_type, normalized_path, limit, offset)
        
        return {
            "success": True,
            "total": len(files),
            "files": files,
            "path_prefix": normalized_path
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get file list: {e}")
        logger.error(f"Error type: {type(e).__name__}, Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-sql")
async def generate_sql(
    query: str = Query(..., description="Natural language query")
):
    """Generate SQL query from natural language"""
    try:
        result = ai_service.generate_sql_from_natural_language(query)
        return {
            "success": True,
            "sql": result.get("sql", ""),
            "description": result.get("description", ""),
            "explanation": result.get("explanation", "")
        }
    except Exception as e:
        logger.error(f"Failed to generate SQL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute-sql")
async def execute_sql(
    sql: str = Query(..., description="SQL query statement")
):
    """Execute SQL query"""
    try:
        results = db.execute_sql(sql)
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Failed to execute SQL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/directory-tree")
async def get_directory_tree(
    root_path: str = Query("/", description="Root path to scan directory tree"),
    max_depth: int = Query(10, ge=1, le=20, description="Maximum depth of directory tree")
):
    """获取目录树形结构（只扫描目录，不扫描文件）"""
    try:
        from pathlib import Path
        import platform
        
        # 根据操作系统确定根路径
        if root_path == "/" or root_path == "\\":
            if platform.system() == "Windows":
                # Windows系统，返回所有驱动器
                import string
                drives = []
                for drive in string.ascii_uppercase:
                    drive_path = f"{drive}:\\"
                    if Path(drive_path).exists():
                        drives.append({
                            'name': f"{drive}:",
                            'path': drive_path,
                            'type': 'directory',
                            'children': []
                        })
                return {
                    "success": True,
                    "tree": {
                        'name': 'Root',
                        'path': '/',
                        'type': 'directory',
                        'children': drives
                    }
                }
            else:
                # Unix/Linux/Mac系统，从根目录开始
                root_path = "/"
        
        # 规范化路径
        scan_path = str(Path(root_path).resolve())
        
        logger.info(f"获取目录树: {scan_path}, max_depth: {max_depth}")
        
        scanner = FileScanner()
        tree = scanner.scan_directory_tree(scan_path, max_depth)
        
        if not tree:
            return {
                "success": False,
                "message": f"无法访问路径: {scan_path}",
                "tree": None
            }
        
        return {
            "success": True,
            "tree": tree,
            "root_path": scan_path
        }
    
    except Exception as e:
        logger.error(f"获取目录树失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康检查"""
    try:
        db.connection.ping(reconnect=True)
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

