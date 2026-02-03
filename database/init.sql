-- iSeek 数据库初始化脚本
-- OceanBase 数据库

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS iseek DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE iseek;

-- 文件信息表
CREATE TABLE IF NOT EXISTS files (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_path VARCHAR(2000) NOT NULL COMMENT '文件完整路径',
    file_name VARCHAR(500) NOT NULL COMMENT '文件名',
    file_size BIGINT NOT NULL COMMENT '文件大小（字节）',
    file_type VARCHAR(100) COMMENT '文件类型（image/video/document等）',
    file_extension VARCHAR(50) COMMENT '文件扩展名',
    mime_type VARCHAR(200) COMMENT 'MIME类型',
    created_time DATETIME COMMENT '文件创建时间',
    modified_time DATETIME COMMENT '文件修改时间',
    file_hash VARCHAR(64) COMMENT '文件MD5哈希值',
    metadata TEXT COMMENT '文件元数据（JSON格式）',
    scan_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '扫描时间',
    INDEX idx_file_path (file_path(255)),
    INDEX idx_file_name (file_name(255)),
    INDEX idx_file_type (file_type),
    INDEX idx_scan_time (scan_time),
    INDEX idx_file_size (file_size)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件信息表';

-- 搜索索引表
CREATE TABLE IF NOT EXISTS file_index (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_id BIGINT NOT NULL COMMENT '文件ID',
    keyword VARCHAR(500) NOT NULL COMMENT '关键词',
    content_preview TEXT COMMENT '内容预览',
    match_score FLOAT DEFAULT 0.0 COMMENT '匹配分数',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    INDEX idx_keyword (keyword(255)),
    INDEX idx_file_id (file_id),
    INDEX idx_match_score (match_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件搜索索引表';

-- 统计记录表
CREATE TABLE IF NOT EXISTS statistics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    stat_type VARCHAR(100) NOT NULL COMMENT '统计类型',
    stat_data TEXT NOT NULL COMMENT '统计数据（JSON格式）',
    sql_query TEXT COMMENT '生成的SQL查询',
    chart_config TEXT COMMENT '图表配置（JSON格式）',
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_stat_type (stat_type),
    INDEX idx_created_time (created_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='统计记录表';



