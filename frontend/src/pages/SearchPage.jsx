import React, { useState, useEffect } from 'react'
import {
  Input,
  Button,
  Card,
  List,
  Typography,
  Space,
  Tag,
  Empty,
  Spin,
  message,
  Divider,
} from 'antd'
import { 
  SearchOutlined, 
  FileOutlined, 
  FolderOutlined,
  GithubOutlined,
  FileTextOutlined,
  HomeOutlined
} from '@ant-design/icons'
import { searchFiles, getFiles } from '../api'
import '../App.css'

const { Title, Text, Paragraph } = Typography

function SearchPage({ onNavigate }) {
  const [keyword, setKeyword] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState([])
  const [aiEnhancement, setAiEnhancement] = useState(null)
  const [total, setTotal] = useState(0)
  const [fileList, setFileList] = useState([])
  const [fileListLoading, setFileListLoading] = useState(false)

  const handleSearch = async () => {
    if (!keyword.trim()) {
      message.warning('Please enter a search keyword')
      return
    }

    setLoading(true)
    try {
      const response = await searchFiles(keyword)
      if (response.success) {
        setResults(response.results || [])
        setTotal(response.total || 0)
        setAiEnhancement(response.ai_enhancement)
        message.success(`Found ${response.total} related files`)
      } else {
        message.error('Search failed')
      }
    } catch (error) {
      message.error('Search request failed: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB'
  }

  // 加载文件列表
  useEffect(() => {
    loadFileList()
  }, [])

  const loadFileList = async () => {
    setFileListLoading(true)
    try {
      const response = await getFiles(null, 50, 0) // 只加载前50个文件
      if (response.success && response.files && response.files.length > 0) {
        setFileList(response.files)
      }
    } catch (error) {
      // 静默失败，不影响搜索功能
    } finally {
      setFileListLoading(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'rgba(113, 188, 32, 0.05)' }}>
      {/* Home 按钮 */}
      <div style={{ padding: '16px 24px', display: 'flex', alignItems: 'center' }}>
        <Button
          type="text"
          icon={<HomeOutlined />}
          onClick={() => onNavigate && onNavigate('home')}
          style={{
            color: '#666666',
            fontSize: '14px',
            padding: '0',
            height: 'auto',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          Home
        </Button>
      </div>

      {/* 搜索区域 */}
      <div style={{ padding: '40px 24px' }}>
        <Title level={2} style={{ color: '#000000', marginBottom: '24px', fontSize: '28px', fontWeight: 600 }}>
          Smart File Retrieval, Find What You Need in Seconds
        </Title>
        
        <div style={{ marginBottom: '16px' }}>
          <Button
            type="primary"
            icon={<SearchOutlined />}
            onClick={handleSearch}
            loading={loading}
            style={{
              background: '#000000',
              borderColor: '#000000',
              marginBottom: '12px',
            }}
          >
            File Search
          </Button>
        </div>
        
        <Input
          size="large"
          placeholder="Enter keywords to search files..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyPress={handleKeyPress}
          style={{
            width: '100%',
            maxWidth: '600px',
            borderRadius: '8px',
          }}
        />
      </div>

      {/* 渐变背景区域 */}
      <div style={{
        position: 'relative',
        minHeight: '400px',
        margin: '0 24px 24px 24px',
        borderRadius: '8px',
        background: 'linear-gradient(135deg, rgba(255, 182, 193, 0.4) 0%, rgba(255, 255, 224, 0.4) 50%, rgba(64, 224, 208, 0.4) 100%)',
        backdropFilter: 'blur(10px)',
        overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(135deg, rgba(255, 182, 193, 0.3) 0%, rgba(255, 255, 224, 0.3) 50%, rgba(64, 224, 208, 0.3) 100%)',
          filter: 'blur(20px)',
          zIndex: 0,
        }} />
        
        {/* 搜索结果内容 */}
        <div style={{ position: 'relative', zIndex: 1, padding: '24px' }}>
          {aiEnhancement && aiEnhancement.enhanced && (
            <Card style={{ marginBottom: 24, background: '#ffffff', border: '1px solid #e0e0e0', opacity: 0.95 }}>
              <Title level={4} style={{ color: '#000000' }}>AI Analysis</Title>
              {aiEnhancement.summary && (
                <Paragraph>{aiEnhancement.summary}</Paragraph>
              )}
              {aiEnhancement.suggestions && aiEnhancement.suggestions.length > 0 && (
                <div>
                  <Text strong>Search Suggestions:</Text>
                  <Space wrap style={{ marginTop: 8 }}>
                    {aiEnhancement.suggestions.map((suggestion, index) => (
                      <Tag
                        key={index}
                        color="blue"
                        style={{ cursor: 'pointer' }}
                        onClick={() => {
                          setKeyword(suggestion)
                          handleSearch()
                        }}
                      >
                        {suggestion}
                      </Tag>
                    ))}
                  </Space>
                </div>
              )}
            </Card>
          )}

          <Spin spinning={loading}>
            {results.length > 0 ? (
              <>
                <div style={{ marginBottom: 16 }}>
                  <Text style={{ color: '#000000', fontWeight: 500 }}>Found {total} related files</Text>
                </div>
                <List
                  dataSource={results}
                  renderItem={(item) => (
                    <Card className="file-card" style={{ background: '#ffffff', border: '1px solid #e0e0e0', marginBottom: 8, opacity: 0.95 }}>
                      <List.Item style={{ color: '#000000' }}>
                        <List.Item.Meta
                          avatar={<FileTextOutlined style={{ fontSize: 24, color: '#000000' }} />}
                          title={
                            <Space>
                              <Text strong style={{ color: '#000000' }}>{item.file_name}</Text>
                              {item.file_type && (
                                <Tag color="blue">{item.file_type}</Tag>
                              )}
                              {item.match_score && (
                                <Tag color="green">
                                  Match: {(item.match_score * 100).toFixed(0)}%
                                </Tag>
                              )}
                            </Space>
                          }
                          description={
                            <div>
                              <div style={{ marginBottom: 8, color: '#666666' }}>
                                <FolderOutlined /> {item.file_path}
                              </div>
                              <Space>
                                <Text style={{ color: '#666666' }}>
                                  Size: {formatFileSize(item.file_size)}
                                </Text>
                                {item.modified_time && (
                                  <Text style={{ color: '#666666' }}>
                                    Modified: {new Date(item.modified_time).toLocaleString()}
                                  </Text>
                                )}
                              </Space>
                              {item.content_preview && (
                                <div style={{ marginTop: 8, padding: 8, background: '#f5f5f5', borderRadius: 4, border: '1px solid #e0e0e0' }}>
                                  <Text style={{ color: '#666666', fontStyle: 'italic' }}>
                                    {item.content_preview}
                                  </Text>
                                </div>
                              )}
                            </div>
                          }
                        />
                      </List.Item>
                    </Card>
                  )}
                />
              </>
            ) : (
              !loading && (
                <Empty
                  description="No search results, please enter keywords to search"
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  style={{ color: '#000000' }}
                />
              )
            )}
          </Spin>

          {/* 显示文件列表（如果已扫描） */}
          {fileList.length > 0 && (
            <div style={{ marginTop: 48 }}>
              <Title level={3} style={{ color: '#000000', marginBottom: 16 }}>Recent Scanned Files</Title>
              <Spin spinning={fileListLoading}>
                <List
                  dataSource={fileList}
                  renderItem={(item) => (
                    <Card className="file-card" style={{ background: '#ffffff', border: '1px solid #e0e0e0', marginBottom: 8, opacity: 0.95 }}>
                      <List.Item style={{ color: '#000000' }}>
                        <List.Item.Meta
                          avatar={<FileTextOutlined style={{ fontSize: 20, color: '#000000' }} />}
                          title={
                            <Space>
                              <Text strong style={{ color: '#000000' }}>{item.file_name}</Text>
                              {item.file_type && (
                                <Tag color="blue">{item.file_type}</Tag>
                              )}
                            </Space>
                          }
                          description={
                            <div>
                              <div style={{ marginBottom: 4, color: '#666666', fontSize: '12px' }}>
                                <FolderOutlined /> {item.file_path}
                              </div>
                              <Space>
                                <Text style={{ color: '#666666', fontSize: '12px' }}>
                                  Size: {formatFileSize(item.file_size)}
                                </Text>
                                {item.scan_time && (
                                  <Text style={{ color: '#666666', fontSize: '12px' }}>
                                    Scanned: {new Date(item.scan_time).toLocaleString()}
                                  </Text>
                                )}
                              </Space>
                            </div>
                          }
                        />
                      </List.Item>
                    </Card>
                  )}
                  pagination={{
                    pageSize: 10,
                    showSizeChanger: false,
                    simple: true,
                  }}
                />
              </Spin>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SearchPage

