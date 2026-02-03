"""
文件扫描服务
"""
import os
import hashlib
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

class FileScanner:
    # 系统目录列表，这些目录不应该被扫描
    SYSTEM_DIRS = {'/proc', '/sys', '/dev', '/run', '/tmp', '/var/run', '/var/lock'}
    
    def __init__(self, max_file_size: int = 104857600):
        self.max_file_size = max_file_size
        self.scanned_count = 0
        self.error_count = 0
    
    def _is_system_directory(self, path: Path) -> bool:
        """检查路径是否是系统目录"""
        try:
            path_str = str(path.resolve())
            # 检查是否是系统目录
            for sys_dir in self.SYSTEM_DIRS:
                if path_str.startswith(sys_dir + '/') or path_str == sys_dir:
                    return True
            # 检查是否是 /proc/self/root 相关的路径（符号链接循环）
            if '/proc/self/root' in path_str or '/proc/' in path_str and '/root/proc/' in path_str:
                return True
            return False
        except Exception:
            # 如果无法解析路径，保守处理，认为是系统目录
            return True
    
    def calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希值"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.warning(f"计算文件哈希失败 {file_path}: {e}")
            return ""
    
    def get_file_info(self, file_path: str) -> Optional[Dict]:
        """获取文件信息"""
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None
            
            stat = path.stat()
            file_size = stat.st_size
            
            # 跳过过大的文件
            if file_size > self.max_file_size:
                logger.warning(f"文件过大，跳过: {file_path} ({file_size} bytes)")
                return None
            
            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(str(path))
            
            # 判断文件类型
            file_type = self._classify_file_type(path.suffix, mime_type)
            
            # 计算文件哈希（仅对小文件）
            file_hash = ""
            if file_size < 10485760:  # 小于10MB的文件才计算哈希
                file_hash = self.calculate_file_hash(str(path))
            
            file_info = {
                'file_path': str(path.absolute()),
                'file_name': path.name,
                'file_size': file_size,
                'file_type': file_type,
                'file_extension': path.suffix.lower() if path.suffix else None,
                'mime_type': mime_type,
                'created_time': datetime.fromtimestamp(stat.st_ctime),
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'file_hash': file_hash,
                'metadata': json.dumps({
                    'is_symlink': path.is_symlink(),
                    'is_readable': os.access(str(path), os.R_OK),
                })
            }
            
            return file_info
        except Exception as e:
            logger.error(f"获取文件信息失败 {file_path}: {e}")
            self.error_count += 1
            return None
    
    def _classify_file_type(self, extension: str, mime_type: Optional[str]) -> str:
        """分类文件类型"""
        if not extension:
            return "unknown"
        
        extension = extension.lower()
        
        # 图片类型
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico']:
            return "image"
        
        # 视频类型
        if extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
            return "video"
        
        # 音频类型
        if extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
            return "audio"
        
        # 文档类型
        if extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf']:
            return "document"
        
        # 代码类型
        if extension in ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.json', '.xml']:
            return "code"
        
        # 压缩文件
        if extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "archive"
        
        return "other"
    
    def scan_directory(self, root_path: str, recursive: bool = True) -> List[Dict]:
        """扫描目录下的所有文件"""
        self.scanned_count = 0
        self.error_count = 0
        
        files = []
        root = Path(root_path)
        
        if not root.exists():
            raise ValueError(f"路径不存在: {root_path}")
        
        if not root.is_dir():
            raise ValueError(f"路径不是目录: {root_path}")
        
        logger.info(f"开始扫描目录: {root_path}")
        
        try:
            if recursive:
                # 递归扫描
                for file_path in root.rglob('*'):
                    # 跳过系统目录
                    if self._is_system_directory(file_path.parent):
                        continue
                    
                    try:
                        if file_path.is_file():
                            file_info = self.get_file_info(str(file_path))
                            if file_info:
                                files.append(file_info)
                                self.scanned_count += 1
                                
                                if self.scanned_count % 100 == 0:
                                    logger.info(f"已扫描 {self.scanned_count} 个文件...")
                    except PermissionError:
                        # 权限错误，静默跳过
                        continue
                    except Exception as e:
                        # 其他错误，记录但不中断扫描
                        logger.debug(f"处理文件失败 {file_path}: {e}")
                        continue
            else:
                # 仅扫描当前目录
                for file_path in root.iterdir():
                    # 跳过系统目录
                    if self._is_system_directory(file_path):
                        continue
                    
                    try:
                        if file_path.is_file():
                            file_info = self.get_file_info(str(file_path))
                            if file_info:
                                files.append(file_info)
                                self.scanned_count += 1
                    except PermissionError:
                        # 权限错误，静默跳过
                        continue
                    except Exception as e:
                        logger.debug(f"处理文件失败 {file_path}: {e}")
                        continue
        
        except PermissionError as e:
            # 根目录权限错误才记录警告
            if not self._is_system_directory(root):
                logger.warning(f"权限不足，跳过: {e}")
        except Exception as e:
            logger.error(f"扫描过程中出错: {e}")
        
        logger.info(f"扫描完成: 成功 {self.scanned_count} 个，错误 {self.error_count} 个")
        
        return files
    
    def scan_directory_tree(self, root_path: str, max_depth: int = 10) -> Optional[Dict]:
        """扫描目录树结构（只获取目录，不扫描文件内容）"""
        def build_tree(path: Path, depth: int = 0) -> Optional[Dict]:
            """递归构建目录树"""
            if depth > max_depth:
                return None
            
            try:
                if not path.exists() or not path.is_dir():
                    return None
                
                # 跳过系统目录
                if self._is_system_directory(path):
                    return None
                
                # 检查是否有读取权限
                if not os.access(str(path), os.R_OK):
                    return None
                
                node = {
                    'name': path.name if path.name else str(path),
                    'path': str(path.absolute()),
                    'type': 'directory',
                    'children': []
                }
                
                # 获取子目录
                try:
                    for item in path.iterdir():
                        if item.is_dir():
                            # 跳过隐藏目录和系统目录（在根目录显示，子目录中跳过）
                            if item.name.startswith('.') and depth > 0:
                                continue
                            
                            # 跳过系统目录
                            if self._is_system_directory(item):
                                continue
                            
                            child = build_tree(item, depth + 1)
                            if child:
                                node['children'].append(child)
                except PermissionError:
                    # 系统目录的权限错误静默处理，其他目录记录调试信息
                    if not self._is_system_directory(path):
                        logger.debug(f"无权限访问目录: {path}")
                except Exception as e:
                    # 系统目录的错误静默处理
                    if not self._is_system_directory(path):
                        logger.debug(f"读取目录失败 {path}: {e}")
                
                # 按名称排序
                node['children'].sort(key=lambda x: x['name'].lower())
                
                return node
            except PermissionError:
                # 权限错误，静默返回 None
                return None
            except Exception as e:
                # 系统目录的错误静默处理
                if not self._is_system_directory(path):
                    logger.debug(f"处理目录失败 {path}: {e}")
                return None
        
        try:
            root = Path(root_path)
            if not root.exists():
                raise ValueError(f"路径不存在: {root_path}")
            
            if not root.is_dir():
                raise ValueError(f"路径不是目录: {root_path}")
            
            tree = build_tree(root)
            return tree
        except Exception as e:
            logger.error(f"扫描目录树失败: {e}")
            raise

