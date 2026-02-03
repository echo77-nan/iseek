"""
搜索服务
"""
import os
import re
from typing import List, Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        self.text_file_extensions = {'.txt', '.md', '.py', '.js', '.java', '.cpp', '.c', 
                                     '.html', '.css', '.json', '.xml', '.log', '.csv'}
        self.max_content_preview = 200
    
    def search_in_file_content(self, file_path: str, keyword: str) -> Optional[Dict]:
        """在文件内容中搜索关键词"""
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None
            
            # 只搜索文本文件
            if path.suffix.lower() not in self.text_file_extensions:
                return None
            
            # 检查文件大小（只搜索小于5MB的文件）
            if path.stat().st_size > 5 * 1024 * 1024:
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 搜索关键词
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matches = list(pattern.finditer(content))
            
            if matches:
                # 获取第一个匹配的上下文
                first_match = matches[0]
                start = max(0, first_match.start() - 50)
                end = min(len(content), first_match.end() + 50)
                preview = content[start:end]
                
                return {
                    'match_count': len(matches),
                    'content_preview': preview,
                    'match_score': min(1.0, len(matches) / 10.0)  # 匹配越多分数越高
                }
            
            return None
        
        except Exception as e:
            logger.debug(f"搜索文件内容失败 {file_path}: {e}")
            return None
    
    def calculate_relevance_score(self, file_name: str, file_path: str, keyword: str, 
                                 content_match: Optional[Dict] = None) -> float:
        """计算文件相关性分数"""
        score = 0.0
        keyword_lower = keyword.lower()
        file_name_lower = file_name.lower()
        file_path_lower = file_path.lower()
        
        # 文件名完全匹配
        if keyword_lower == file_name_lower:
            score += 10.0
        # 文件名包含关键词
        elif keyword_lower in file_name_lower:
            score += 5.0
        
        # 路径包含关键词
        if keyword_lower in file_path_lower:
            score += 2.0
        
        # 内容匹配
        if content_match:
            score += content_match.get('match_score', 0.0) * 3.0
        
        return score
    
    def search_files(self, keyword: str, search_path: str = None) -> List[Dict]:
        """搜索文件（文件名、路径、内容）"""
        results = []
        
        # 如果指定了搜索路径，在该路径下搜索
        if search_path:
            search_root = Path(search_path)
            if search_root.exists() and search_root.is_dir():
                for file_path in search_root.rglob('*'):
                    if file_path.is_file():
                        result = self._match_file(file_path, keyword)
                        if result:
                            results.append(result)
        else:
            # 从数据库搜索（由API层处理）
            pass
        
        # 按相关性分数排序
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return results
    
    def _match_file(self, file_path: Path, keyword: str) -> Optional[Dict]:
        """匹配单个文件"""
        file_name = file_path.name
        file_path_str = str(file_path)
        
        # 检查文件名和路径
        keyword_lower = keyword.lower()
        if keyword_lower not in file_name.lower() and keyword_lower not in file_path_str.lower():
            # 尝试内容搜索
            content_match = self.search_in_file_content(file_path_str, keyword)
            if not content_match:
                return None
        else:
            content_match = None
        
        # 计算相关性分数
        relevance_score = self.calculate_relevance_score(
            file_name, file_path_str, keyword, content_match
        )
        
        if relevance_score > 0:
            return {
                'file_path': file_path_str,
                'file_name': file_name,
                'file_size': file_path.stat().st_size,
                'relevance_score': relevance_score,
                'content_preview': content_match.get('content_preview', '') if content_match else '',
                'match_count': content_match.get('match_count', 0) if content_match else 0
            }
        
        return None

search_service = SearchService()



