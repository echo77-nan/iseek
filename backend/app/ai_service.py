"""
阿里云大模型服务
"""
import json
import logging
from typing import Dict, Optional
from decimal import Decimal
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import dashscope
from dashscope import Generation
from config import settings

logger = logging.getLogger(__name__)

def convert_decimal(obj):
    """递归转换 Decimal 类型为 float/int"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_decimal(item) for item in obj)
    else:
        return obj

# 设置API Key
dashscope.api_key = settings.DASHSCOPE_API_KEY

class AIService:
    def __init__(self):
        self.model = settings.DASHSCOPE_MODEL
    
    def generate_statistics_sql(self, statistics_data: Dict) -> Dict:
        """基于统计数据生成SQL查询语句"""
        try:
            # 转换 Decimal 类型为可序列化的类型
            converted_data = convert_decimal(statistics_data)
            
            prompt = f"""
Based on the following file statistics, generate useful SQL queries and chart configurations.

Statistics:
- Total files: {converted_data.get('total_files', 0)}
- File type distribution: {json.dumps(converted_data.get('by_type', []), ensure_ascii=False)}
- File extension distribution: {json.dumps(converted_data.get('by_extension', []), ensure_ascii=False)}
- File size distribution: {json.dumps(converted_data.get('by_size', []), ensure_ascii=False)}

Please generate:
1. 3-5 useful SQL queries (for in-depth analysis)
2. Corresponding chart configurations (ECharts format)

Return JSON format:
{{
    "sql_queries": [
        {{"name": "Query name", "sql": "SQL statement", "description": "Description"}}
    ],
    "charts": [
        {{"title": "Chart title", "type": "pie/bar/line", "config": {{"ECharts config"}}}}
    ],
    "insights": ["Insight 1", "Insight 2"]
}}
"""
            
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            if response.status_code == 200:
                result_text = response.output.text
                # 尝试解析JSON
                try:
                    # 提取JSON部分
                    if "```json" in result_text:
                        json_start = result_text.find("```json") + 7
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    elif "```" in result_text:
                        json_start = result_text.find("```") + 3
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    
                    result = json.loads(result_text)
                    return result
                except json.JSONDecodeError:
                    logger.warning("AI返回的不是有效JSON，使用默认格式")
                    return self._default_statistics_result(converted_data)
            else:
                logger.error(f"AI服务调用失败: {response.message}")
                converted_data = convert_decimal(statistics_data)
                return self._default_statistics_result(converted_data)
        
        except Exception as e:
            logger.error(f"生成统计SQL失败: {e}")
            converted_data = convert_decimal(statistics_data)
            return self._default_statistics_result(converted_data)
    
    def _default_statistics_result(self, statistics_data: Dict) -> Dict:
        """默认统计结果"""
        # 确保统计数据已转换（处理 Decimal 类型）
        converted_data = convert_decimal(statistics_data)
        
        return {
            "sql_queries": [
                {
                    "name": "Count files by type",
                    "sql": "SELECT file_type, COUNT(*) as count FROM files GROUP BY file_type ORDER BY count DESC",
                    "description": "Count files by type"
                },
                {
                    "name": "Large files list",
                    "sql": "SELECT file_name, file_size, file_path FROM files WHERE file_size > 10485760 ORDER BY file_size DESC LIMIT 20",
                    "description": "Find files larger than 10MB"
                }
            ],
            "charts": [
                {
                    "title": "File Type Distribution",
                    "type": "pie",
                    "config": {
                        "series": [{
                            "type": "pie",
                            "data": [{"name": item.get("file_type", "Unknown"), "value": item.get("count", 0)} 
                                    for item in converted_data.get('by_type', [])]
                        }]
                    }
                }
            ],
            "insights": ["File statistics completed"]
        }
    
    def generate_sql_from_natural_language(self, natural_language: str, table_schema: str = None) -> Dict:
        """从自然语言生成SQL查询"""
        try:
            schema_info = table_schema or """
            Table: files
            Columns:
            - id: BIGINT (primary key)
            - file_path: VARCHAR(2000) - file full path
            - file_name: VARCHAR(500) - file name
            - file_size: BIGINT - file size in bytes
            - file_type: VARCHAR(100) - file type (image/video/document/code/etc)
            - file_extension: VARCHAR(50) - file extension
            - mime_type: VARCHAR(200) - MIME type
            - created_time: DATETIME - file creation time
            - modified_time: DATETIME - file modification time
            - scan_time: DATETIME - scan time
            """
            
            prompt = f"""
            User request in natural language: "{natural_language}"
            
            Database schema:
            {schema_info}
            
            Please generate a SQL SELECT query based on the user's request.
            Only generate SELECT queries, do not generate INSERT, UPDATE, DELETE, or DROP statements.
            
            Return JSON format:
            {{
                "sql": "SELECT statement here",
                "description": "Description of what this query does",
                "explanation": "Explanation of the query logic"
            }}
            """
            
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3
            )
            
            if response.status_code == 200:
                result_text = response.output.text
                try:
                    # 提取JSON部分
                    if "```json" in result_text:
                        json_start = result_text.find("```json") + 7
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    elif "```" in result_text:
                        json_start = result_text.find("```") + 3
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    
                    result = json.loads(result_text)
                    return result
                except json.JSONDecodeError:
                    logger.warning("AI返回的不是有效JSON")
                    return {
                        "sql": "",
                        "description": "Failed to parse AI response",
                        "explanation": ""
                    }
            else:
                logger.error(f"AI服务调用失败: {response.message}")
                return {
                    "sql": "",
                    "description": "AI service call failed",
                    "explanation": ""
                }
        
        except Exception as e:
            logger.error(f"生成SQL失败: {e}")
            return {
                "sql": "",
                "description": f"Error: {str(e)}",
                "explanation": ""
            }
    
    def enhance_search_results(self, keyword: str, files: list) -> Dict:
        """使用AI增强搜索结果"""
        try:
            if not files:
                return {"enhanced": False, "suggestions": []}
            
            prompt = f"""
User searched for keyword: "{keyword}"
Found {len(files)} related files.

Please analyze these files and provide:
1. Summary of search results
2. Related search suggestions
3. File category suggestions

Return JSON format:
{{
    "summary": "Summary of search results",
    "suggestions": ["suggestion1", "suggestion2"],
    "categories": ["category1", "category2"]
}}
"""
            
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            if response.status_code == 200:
                result_text = response.output.text
                try:
                    if "```json" in result_text:
                        json_start = result_text.find("```json") + 7
                        json_end = result_text.find("```", json_start)
                        result_text = result_text[json_start:json_end].strip()
                    
                    result = json.loads(result_text)
                    result["enhanced"] = True
                    return result
                except json.JSONDecodeError:
                    pass
            
            return {"enhanced": False, "suggestions": []}
        
        except Exception as e:
            logger.error(f"AI增强搜索失败: {e}")
            return {"enhanced": False, "suggestions": []}

ai_service = AIService()

