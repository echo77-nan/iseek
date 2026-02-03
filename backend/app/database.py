"""
数据库操作模块
"""
import pymysql
from typing import List, Dict, Optional
from datetime import datetime
import logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def _ensure_connection(self):
        """确保数据库连接有效"""
        try:
            if self.connection is None:
                self.connect()
            else:
                # 检查连接是否有效
                self.connection.ping(reconnect=True)
        except Exception as e:
            logger.warning(f"数据库连接检查失败，重新连接: {e}")
            self.connect()
    
    def connect(self):
        """连接OceanBase数据库"""
        try:
            # 先尝试连接指定数据库
            self.connection = pymysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("数据库连接成功")
        except pymysql.err.OperationalError as e:
            # 如果数据库不存在，先创建数据库
            if e.args[0] == 1049:  # Unknown database
                logger.info(f"数据库 {settings.DB_NAME} 不存在，正在创建...")
                self._create_database()
                # 重新连接
                self.connection = pymysql.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                logger.info("数据库创建并连接成功")
            else:
                logger.error(f"数据库连接失败: {e}")
                raise
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def _create_database(self):
        """创建数据库"""
        try:
            # 连接不指定数据库
            temp_conn = pymysql.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            with temp_conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                temp_conn.commit()
                logger.info(f"数据库 {settings.DB_NAME} 创建成功")
            temp_conn.close()
        except Exception as e:
            logger.error(f"创建数据库失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
    
    def init_tables(self):
        """初始化数据库表"""
        try:
            with self.connection.cursor() as cursor:
                # 创建文件信息表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS files (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        file_path VARCHAR(2000) NOT NULL,
                        file_name VARCHAR(500) NOT NULL,
                        file_size BIGINT NOT NULL,
                        file_type VARCHAR(100),
                        file_extension VARCHAR(50),
                        mime_type VARCHAR(200),
                        created_time DATETIME,
                        modified_time DATETIME,
                        file_hash VARCHAR(64),
                        metadata TEXT,
                        scan_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_file_path (file_path(255)),
                        INDEX idx_file_name (file_name(255)),
                        INDEX idx_file_type (file_type),
                        INDEX idx_scan_time (scan_time)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                
                # 尝试添加唯一索引（基于 file_path 的前 500 字符，因为 OceanBase 可能不支持超长唯一索引）
                # 如果失败，说明表已存在或索引已存在，忽略错误
                try:
                    cursor.execute("""
                        ALTER TABLE files 
                        ADD UNIQUE KEY uk_file_path (file_path(500))
                    """)
                    logger.info("已添加 file_path 唯一索引")
                except Exception as e:
                    # 索引可能已存在，忽略错误
                    logger.debug(f"唯一索引可能已存在或创建失败: {e}")
                    pass
                
                # 创建搜索索引表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS file_index (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        file_id BIGINT NOT NULL,
                        keyword VARCHAR(500) NOT NULL,
                        content_preview TEXT,
                        match_score FLOAT DEFAULT 0.0,
                        created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
                        INDEX idx_keyword (keyword(255)),
                        INDEX idx_file_id (file_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                
                # 创建统计记录表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS statistics (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        stat_type VARCHAR(100) NOT NULL,
                        stat_data TEXT NOT NULL,
                        sql_query TEXT,
                        chart_config TEXT,
                        created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_stat_type (stat_type),
                        INDEX idx_created_time (created_time)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                
                self.connection.commit()
                logger.info("数据库表初始化成功")
        except Exception as e:
            logger.error(f"数据库表初始化失败: {e}")
            self.connection.rollback()
            raise
    
    def _sanitize_file_info(self, file_info: Dict) -> Dict:
        """清理和验证文件信息，确保符合数据库字段限制"""
        sanitized = {}
        
        # file_path: VARCHAR(2000) NOT NULL
        file_path = str(file_info.get('file_path', ''))
        if len(file_path) > 2000:
            logger.warning(f"文件路径过长，截断: {file_path[:100]}...")
            sanitized['file_path'] = file_path[:2000]
        else:
            sanitized['file_path'] = file_path if file_path else '/'
        
        # file_name: VARCHAR(500) NOT NULL
        file_name = str(file_info.get('file_name', ''))
        if len(file_name) > 500:
            logger.warning(f"文件名过长，截断: {file_name[:100]}...")
            sanitized['file_name'] = file_name[:500]
        else:
            sanitized['file_name'] = file_name if file_name else 'unknown'
        
        # file_size: BIGINT NOT NULL
        sanitized['file_size'] = int(file_info.get('file_size', 0))
        
        # file_type: VARCHAR(100)
        file_type = str(file_info.get('file_type', '')) if file_info.get('file_type') else None
        if file_type and len(file_type) > 100:
            sanitized['file_type'] = file_type[:100]
        else:
            sanitized['file_type'] = file_type
        
        # file_extension: VARCHAR(50)
        file_extension = str(file_info.get('file_extension', '')) if file_info.get('file_extension') else None
        if file_extension:
            # 移除前导点
            if file_extension.startswith('.'):
                file_extension = file_extension[1:]
            if len(file_extension) > 50:
                sanitized['file_extension'] = file_extension[:50]
            else:
                sanitized['file_extension'] = file_extension
        else:
            sanitized['file_extension'] = None
        
        # mime_type: VARCHAR(200)
        mime_type = str(file_info.get('mime_type', '')) if file_info.get('mime_type') else None
        if mime_type and len(mime_type) > 200:
            sanitized['mime_type'] = mime_type[:200]
        else:
            sanitized['mime_type'] = mime_type
        
        # created_time, modified_time: DATETIME
        sanitized['created_time'] = file_info.get('created_time')
        sanitized['modified_time'] = file_info.get('modified_time')
        
        # file_hash: VARCHAR(64)
        file_hash = str(file_info.get('file_hash', '')) if file_info.get('file_hash') else None
        if file_hash and len(file_hash) > 64:
            sanitized['file_hash'] = file_hash[:64]
        else:
            sanitized['file_hash'] = file_hash if file_hash else None
        
        # metadata: TEXT
        metadata = file_info.get('metadata')
        if isinstance(metadata, dict):
            import json
            sanitized['metadata'] = json.dumps(metadata)
        elif isinstance(metadata, str):
            sanitized['metadata'] = metadata
        else:
            sanitized['metadata'] = None
        
        return sanitized
    
    def insert_file(self, file_info: Dict, update_if_exists: bool = True) -> int:
        """插入或更新文件信息
        
        Args:
            file_info: 文件信息字典
            update_if_exists: 如果文件已存在，是否更新（默认True）
        
        Returns:
            文件ID，如果更新已存在的文件，返回现有ID；如果是新插入，返回新ID；如果跳过，返回0
        """
        try:
            # 确保数据库连接有效
            self._ensure_connection()
            
            # 清理和验证数据
            sanitized_info = self._sanitize_file_info(file_info)
            file_path = sanitized_info['file_path']
            
            with self.connection.cursor() as cursor:
                # 先检查文件是否已存在
                cursor.execute("SELECT id FROM files WHERE file_path = %s", (file_path,))
                existing_file = cursor.fetchone()
                
                if existing_file and update_if_exists:
                    # 文件已存在，更新记录
                    file_id = existing_file['id']
                    sql = """
                        UPDATE files SET
                            file_name = %s,
                            file_size = %s,
                            file_type = %s,
                            file_extension = %s,
                            mime_type = %s,
                            modified_time = %s,
                            file_hash = %s,
                            metadata = %s,
                            scan_time = NOW()
                        WHERE id = %s
                    """
                    cursor.execute(sql, (
                        sanitized_info['file_name'],
                        sanitized_info['file_size'],
                        sanitized_info['file_type'],
                        sanitized_info['file_extension'],
                        sanitized_info['mime_type'],
                        sanitized_info['modified_time'],
                        sanitized_info['file_hash'],
                        sanitized_info['metadata'],
                        file_id
                    ))
                    self.connection.commit()
                    return file_id
                elif existing_file and not update_if_exists:
                    # 文件已存在但不更新，跳过
                    return 0
                else:
                    # 文件不存在，插入新记录
                    sql = """
                        INSERT INTO files (
                            file_path, file_name, file_size, file_type,
                            file_extension, mime_type, created_time, modified_time,
                            file_hash, metadata, scan_time
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    cursor.execute(sql, (
                        sanitized_info['file_path'],
                        sanitized_info['file_name'],
                        sanitized_info['file_size'],
                        sanitized_info['file_type'],
                        sanitized_info['file_extension'],
                        sanitized_info['mime_type'],
                        sanitized_info['created_time'],
                        sanitized_info['modified_time'],
                        sanitized_info['file_hash'],
                        sanitized_info['metadata']
                    ))
                    self.connection.commit()
                    return cursor.lastrowid
        except pymysql.err.DataError as e:
            logger.error(f"插入文件信息失败（数据错误）: {e}, 文件: {file_info.get('file_path', 'unknown')}")
            logger.error(f"数据详情: path_len={len(str(file_info.get('file_path', '')))}, name_len={len(str(file_info.get('file_name', '')))}")
            self.connection.rollback()
            raise
        except pymysql.err.IntegrityError as e:
            # 如果使用 INSERT IGNORE 且文件已存在，返回0
            if not update_if_exists:
                logger.debug(f"文件已存在，跳过: {file_info.get('file_path', 'unknown')}")
                return 0
            # 其他完整性错误
            logger.warning(f"文件插入完整性错误: {file_info.get('file_path', 'unknown')}, 错误: {e}")
            self.connection.rollback()
            raise
        except Exception as e:
            logger.error(f"插入文件信息失败: {e}, 文件: {file_info.get('file_path', 'unknown')}")
            logger.error(f"错误类型: {type(e).__name__}, 错误详情: {str(e)}")
            self.connection.rollback()
            raise
    
    def check_files_exist_by_path(self, path_prefix: str) -> bool:
        """检查指定路径下是否存在文件记录
        
        Args:
            path_prefix: 路径前缀
        
        Returns:
            如果存在文件记录返回True，否则返回False
        """
        try:
            self._ensure_connection()
            
            with self.connection.cursor() as cursor:
                normalized_prefix = path_prefix.rstrip('/') + '/'
                sql = "SELECT COUNT(*) as count FROM files WHERE file_path LIKE %s OR file_path = %s"
                cursor.execute(sql, (f"{normalized_prefix}%", path_prefix.rstrip('/')))
                result = cursor.fetchone()
                return result['count'] > 0 if result else False
        except Exception as e:
            logger.error(f"检查文件记录失败: {e}")
            return False
    
    def delete_files_by_path_prefix(self, path_prefix: str) -> int:
        """删除指定路径前缀下的所有文件记录
        
        Args:
            path_prefix: 路径前缀，例如 '/home/echo.ln/nltk_data'
        
        Returns:
            删除的记录数
        """
        try:
            self._ensure_connection()
            
            with self.connection.cursor() as cursor:
                # 规范化路径前缀（确保以 / 结尾，用于 LIKE 查询）
                normalized_prefix = path_prefix.rstrip('/') + '/'
                
                sql = "DELETE FROM files WHERE file_path LIKE %s OR file_path = %s"
                cursor.execute(sql, (f"{normalized_prefix}%", path_prefix.rstrip('/')))
                deleted_count = cursor.rowcount
                self.connection.commit()
                
                logger.info(f"删除了 {deleted_count} 个路径前缀为 '{path_prefix}' 的文件记录")
                return deleted_count
        except Exception as e:
            logger.error(f"删除文件记录失败: {e}")
            self.connection.rollback()
            raise
    
    def get_all_files(self, file_type: Optional[str] = None, path_prefix: Optional[str] = None, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """获取文件列表
        
        Args:
            file_type: 文件类型过滤（可选）
            path_prefix: 路径前缀过滤（可选，但强烈建议提供以确保数据准确性）
            limit: 返回数量限制（None表示不限制）
            offset: 偏移量
        """
        try:
            # 确保数据库连接有效
            self._ensure_connection()
            
            with self.connection.cursor() as cursor:
                conditions = []
                params = []
                
                if file_type:
                    conditions.append("file_type = %s")
                    params.append(file_type)
                
                # 路径前缀过滤是必需的，如果没有提供则返回空列表
                if path_prefix:
                    # 规范化路径前缀
                    normalized_prefix = path_prefix.rstrip('/') + '/'
                    conditions.append("(file_path LIKE %s OR file_path = %s)")
                    params.append(f"{normalized_prefix}%")
                    params.append(path_prefix.rstrip('/'))
                else:
                    # 如果没有提供路径前缀，返回空列表（安全策略）
                    logger.warning("get_all_files called without path_prefix, returning empty list for safety")
                    return []
                
                where_clause = " AND ".join(conditions) if conditions else "1=1"
                
                # 构建SQL，如果limit为None则不添加LIMIT子句
                if limit is not None:
                    sql = f"SELECT * FROM files WHERE {where_clause} ORDER BY scan_time DESC LIMIT %s OFFSET %s"
                    params.extend([limit, offset])
                else:
                    sql = f"SELECT * FROM files WHERE {where_clause} ORDER BY scan_time DESC"
                    if offset > 0:
                        sql += f" LIMIT 999999 OFFSET %s"
                        params.append(offset)
                
                cursor.execute(sql, params)
                
                files = cursor.fetchall()
                
                # 转换datetime对象为字符串
                for file in files:
                    if file.get('created_time'):
                        file['created_time'] = file['created_time'].isoformat() if isinstance(file['created_time'], datetime) else file['created_time']
                    if file.get('modified_time'):
                        file['modified_time'] = file['modified_time'].isoformat() if isinstance(file['modified_time'], datetime) else file['modified_time']
                    if file.get('scan_time'):
                        file['scan_time'] = file['scan_time'].isoformat() if isinstance(file['scan_time'], datetime) else file['scan_time']
                
                return files
        except pymysql.err.OperationalError as e:
            logger.error(f"获取文件列表失败（数据库操作错误）: {e}")
            # 尝试重新连接
            try:
                self.connect()
                # 重试一次
                return self.get_all_files(file_type, limit, offset)
            except Exception as retry_e:
                logger.error(f"重试获取文件列表失败: {retry_e}")
                raise
        except Exception as e:
            logger.error(f"获取文件列表失败: {e}")
            logger.error(f"错误类型: {type(e).__name__}, 错误详情: {str(e)}")
            raise
    
    def search_files(self, keyword: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """搜索文件"""
        try:
            # 确保数据库连接有效
            self._ensure_connection()
            
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT f.*, fi.match_score, fi.content_preview
                    FROM files f
                    LEFT JOIN file_index fi ON f.id = fi.file_id
                    WHERE f.file_name LIKE %s 
                       OR f.file_path LIKE %s
                       OR fi.keyword LIKE %s
                    ORDER BY fi.match_score DESC, f.file_name
                    LIMIT %s OFFSET %s
                """
                pattern = f"%{keyword}%"
                cursor.execute(sql, (pattern, pattern, pattern, limit, offset))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"搜索文件失败: {e}")
            raise
    
    def get_file_statistics(self) -> Dict:
        """获取文件统计信息"""
        try:
            # 确保数据库连接有效
            self._ensure_connection()
            
            with self.connection.cursor() as cursor:
                stats = {}
                
                # 总文件数
                cursor.execute("SELECT COUNT(*) as total FROM files")
                stats['total_files'] = cursor.fetchone()['total']
                
                # 按类型统计
                cursor.execute("""
                    SELECT file_type, COUNT(*) as count, SUM(file_size) as total_size
                    FROM files
                    GROUP BY file_type
                    ORDER BY count DESC
                """)
                stats['by_type'] = cursor.fetchall()
                
                # 按扩展名统计
                cursor.execute("""
                    SELECT file_extension, COUNT(*) as count
                    FROM files
                    WHERE file_extension IS NOT NULL
                    GROUP BY file_extension
                    ORDER BY count DESC
                    LIMIT 20
                """)
                stats['by_extension'] = cursor.fetchall()
                
                # 文件大小分布
                cursor.execute("""
                    SELECT 
                        CASE 
                            WHEN file_size < 1024 THEN '0-1KB'
                            WHEN file_size < 1048576 THEN '1KB-1MB'
                            WHEN file_size < 104857600 THEN '1MB-100MB'
                            ELSE '100MB+'
                        END as size_range,
                        COUNT(*) as count
                    FROM files
                    GROUP BY size_range
                """)
                stats['by_size'] = cursor.fetchall()
                
                return stats
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            raise
    
    def save_statistics(self, stat_type: str, stat_data: str, sql_query: str = None, chart_config: str = None):
        """保存统计结果"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO statistics (stat_type, stat_data, sql_query, chart_config)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (stat_type, stat_data, sql_query, chart_config))
                self.connection.commit()
        except Exception as e:
            logger.error(f"保存统计结果失败: {e}")
            self.connection.rollback()
            raise
    
    def insert_files_batch(self, files: List[Dict]) -> int:
        """批量插入文件信息"""
        if not files:
            return 0
        
        saved_count = 0
        for file_info in files:
            try:
                self.insert_file(file_info)
                saved_count += 1
            except Exception as e:
                logger.warning(f"批量插入中跳过文件: {file_info.get('file_path', 'unknown')}, 错误: {e}")
                continue
        
        return saved_count
    
    def execute_sql(self, sql_query: str) -> List[Dict]:
        """执行SQL查询"""
        try:
            with self.connection.cursor() as cursor:
                # 只允许 SELECT 查询
                sql_query = sql_query.strip()
                if not sql_query.upper().startswith('SELECT'):
                    raise ValueError("Only SELECT queries are allowed")
                
                cursor.execute(sql_query)
                results = cursor.fetchall()
                
                # 转换datetime对象为字符串
                for result in results:
                    for key, value in result.items():
                        if isinstance(value, datetime):
                            result[key] = value.isoformat()
                
                return results
        except Exception as e:
            logger.error(f"执行SQL失败: {e}")
            raise

# 全局数据库实例
db = Database()

