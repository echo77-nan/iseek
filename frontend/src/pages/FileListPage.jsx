import React, { useState, useEffect } from 'react'
import {
  Table,
  Card,
  Typography,
  Tag,
  Input,
  Select,
  Space,
  Button,
  message,
  Spin,
  Tree,
  Drawer,
  Row,
  Col,
} from 'antd'
import { 
  ReloadOutlined, 
  ScanOutlined,
  GithubOutlined,
  SyncOutlined,
  HomeOutlined,
  FolderOutlined,
  FolderOpenOutlined
} from '@ant-design/icons'
import { getFiles, scanDirectory, getDirectoryTree } from '../api'
import '../App.css'

const { Title, Text } = Typography
const { Option } = Select

function FileListPage({ onNavigate }) {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [scanning, setScanning] = useState(false)
  const [fileType, setFileType] = useState(null)
  const [searchPath, setSearchPath] = useState('')
  const [currentScanPath, setCurrentScanPath] = useState(null)
  const [treeVisible, setTreeVisible] = useState(false)
  const [treeData, setTreeData] = useState([])
  const [treeLoading, setTreeLoading] = useState(false)
  const [expandedKeys, setExpandedKeys] = useState([])
  const [selectedKeys, setSelectedKeys] = useState([])

  useEffect(() => {
    // 检查是否有从目录树页面传递的路径
    const lastScanPath = localStorage.getItem('lastScanPath')
    if (lastScanPath && !currentScanPath) {
      setCurrentScanPath(lastScanPath)
      setSearchPath(lastScanPath)
      localStorage.removeItem('lastScanPath') // 清除，避免重复使用
    }
    loadFiles()
  }, [fileType, currentScanPath])

  // 加载目录树
  useEffect(() => {
    if (treeVisible) {
      loadDirectoryTree()
    }
  }, [treeVisible])

  const loadFiles = async () => {
    if (!currentScanPath) {
      setFiles([])
      return
    }
    
    setLoading(true)
    try {
      const response = await getFiles(currentScanPath, fileType, null)
      if (response.success) {
        setFiles(response.files || [])
      } else {
        message.error('Failed to get file list')
        setFiles([])
      }
    } catch (error) {
      message.error('Failed to get file list: ' + error.message)
      setFiles([])
    } finally {
      setLoading(false)
    }
  }

  const handleScan = async (forceRescan = false) => {
    if (!searchPath.trim()) {
      message.warning('Please enter the path to scan')
      return
    }

    setScanning(true)
    try {
      const response = await scanDirectory(searchPath, true, forceRescan)
      if (response.success) {
        const normalizedPath = response.path || searchPath.trim()
        setCurrentScanPath(normalizedPath)
        
        if (response.status === 'cached') {
          message.success(response.message || `Found ${response.file_count || 0} files in database`)
          loadFiles()
          setScanning(false)
        } else if (response.status === 'processing') {
          message.info(response.message || 'Scan task started, processing in background...')
          setTimeout(() => {
            loadFiles()
            setScanning(false)
          }, 3000)
        } else {
          message.success(response.message || 'Scan completed')
          loadFiles()
          setScanning(false)
        }
      } else {
        message.error('Scan failed')
        setScanning(false)
      }
    } catch (error) {
      if (error.message && error.message.includes('timeout')) {
        setCurrentScanPath(searchPath.trim())
        message.warning('Scan task started in background. The scan is processing, please refresh the file list later.')
        setScanning(false)
        setTimeout(() => {
          loadFiles()
        }, 5000)
      } else {
        message.error('Scan failed: ' + error.message)
        setScanning(false)
      }
    }
  }
  
  const handleClearFilter = () => {
    setCurrentScanPath(null)
    setFileType(null)
  }

  // 加载目录树
  const loadDirectoryTree = async () => {
    setTreeLoading(true)
    try {
      const response = await getDirectoryTree('/', 10)
      if (response.success && response.tree) {
        const treeNode = convertTreeData(response.tree)
        if (treeNode) {
          setTreeData([treeNode])
          // 默认展开根节点
          setExpandedKeys([treeNode.key])
          setSelectedKeys([])
        }
      } else {
        message.error(response.message || 'Failed to load directory tree')
      }
    } catch (error) {
      message.error('Failed to load directory tree: ' + error.message)
    } finally {
      setTreeLoading(false)
    }
  }

  // 转换树形数据格式
  const convertTreeData = (node, parentKey = '') => {
    if (!node) return null
    
    const key = parentKey ? `${parentKey}/${node.name}` : node.name
    const treeNode = {
      title: node.name,
      key: key,
      path: node.path,
      icon: <FolderOutlined />,
      children: []
    }

    if (node.children && node.children.length > 0) {
      treeNode.children = node.children
        .map((child) => convertTreeData(child, key))
        .filter(Boolean)
    }

    return treeNode
  }

  // 处理树节点选择
  const handleTreeSelect = (selectedKeys, info) => {
    if (selectedKeys.length > 0) {
      const selectedNode = info.node
      setSearchPath(selectedNode.path)
      setSelectedKeys(selectedKeys)
    }
  }

  // 处理树节点展开
  const handleTreeExpand = (expandedKeys) => {
    setExpandedKeys(expandedKeys)
  }

  // 打开目录树选择器
  const handleOpenTree = () => {
    setTreeVisible(true)
    if (treeData.length === 0) {
      loadDirectoryTree()
    }
  }

  // 确认选择路径
  const handleConfirmPath = () => {
    if (selectedKeys.length > 0) {
      const selectedNode = findNodeByKey(treeData, selectedKeys[0])
      if (selectedNode) {
        setSearchPath(selectedNode.path)
        setTreeVisible(false)
        message.success(`Path selected: ${selectedNode.path}`)
      }
    } else {
      message.warning('Please select a directory')
    }
  }

  // 根据key查找节点
  const findNodeByKey = (nodes, key) => {
    for (const node of nodes) {
      if (node.key === key) {
        return node
      }
      if (node.children) {
        const found = findNodeByKey(node.children, key)
        if (found) return found
      }
    }
    return null
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB'
  }

  const columns = [
    {
      title: 'File Name',
      dataIndex: 'file_name',
      key: 'file_name',
      width: 300,
      ellipsis: true,
    },
    {
      title: 'Type',
      dataIndex: 'file_type',
      key: 'file_type',
      width: 100,
      render: (type) => (type ? <Tag color="blue">{type}</Tag> : '-'),
    },
    {
      title: 'Extension',
      dataIndex: 'file_extension',
      key: 'file_extension',
      width: 100,
    },
    {
      title: 'Size',
      dataIndex: 'file_size',
      key: 'file_size',
      width: 120,
      render: (size) => formatFileSize(size),
    },
    {
      title: 'Path',
      dataIndex: 'file_path',
      key: 'file_path',
      ellipsis: true,
    },
    {
      title: 'Scan Time',
      dataIndex: 'scan_time',
      key: 'scan_time',
      width: 180,
      render: (time) => (time ? new Date(time).toLocaleString() : '-'),
    },
  ]

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

      {/* 渐变背景区域 */}
      <div style={{
        position: 'relative',
        padding: '40px 24px',
        margin: '0 24px 24px 24px',
        borderRadius: '8px',
        background: 'linear-gradient(135deg, rgba(100, 181, 246, 0.3) 0%, rgba(77, 182, 172, 0.3) 100%)',
        backdropFilter: 'blur(10px)',
        overflow: 'hidden',
      }}>
        {/* 模糊效果 */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(135deg, rgba(100, 181, 246, 0.2) 0%, rgba(77, 182, 172, 0.2) 100%)',
          filter: 'blur(20px)',
          zIndex: 0,
        }} />
        
        {/* 内容区域 */}
        <div style={{ position: 'relative', zIndex: 1 }}>
          {/* 第一行：Scan Directory 按钮 + path 输入框 + 选择路径按钮 */}
          <div style={{ display: 'flex', gap: '16px', marginBottom: '16px', alignItems: 'center' }}>
            <Button
              type="primary"
              icon={<ScanOutlined />}
              onClick={() => handleScan(false)}
              loading={scanning}
              style={{
                background: '#000000',
                borderColor: '#000000',
                minWidth: '140px',
              }}
            >
              Scan Directory
            </Button>
            <Input
              placeholder="path"
              value={searchPath}
              onChange={(e) => setSearchPath(e.target.value)}
              style={{ flex: 1, maxWidth: '400px' }}
            />
            <Button
              icon={<FolderOpenOutlined />}
              onClick={handleOpenTree}
              style={{
                background: '#ffffff',
                borderColor: '#d9d9d9',
                color: '#000000',
              }}
            >
              Select Path
            </Button>
          </div>

          {/* 第二行：Refresh 按钮 + file type 输入框 */}
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <Button
              icon={<SyncOutlined />}
              onClick={loadFiles}
              style={{
                background: '#ffffff',
                borderColor: '#d9d9d9',
                color: '#000000',
                minWidth: '140px',
              }}
            >
              Refresh
            </Button>
            <Select
              placeholder="file type"
              allowClear
              style={{ flex: 1, maxWidth: '400px' }}
              value={fileType}
              onChange={setFileType}
            >
              <Option value="image">Image</Option>
              <Option value="video">Video</Option>
              <Option value="audio">Audio</Option>
              <Option value="document">Document</Option>
              <Option value="code">Code</Option>
              <Option value="archive">Archive</Option>
              <Option value="other">Other</Option>
            </Select>
          </div>
        </div>
      </div>

      {/* 表格区域 */}
      <div style={{ padding: '0 24px 24px 24px' }}>
        <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0' }}>
          <Spin spinning={loading}>
            <Table
              columns={columns}
              dataSource={files.map((file, index) => ({ ...file, key: file.id || index }))}
              pagination={{
                pageSize: 20,
                showSizeChanger: true,
                showTotal: (total) => `Total ${total} records`,
              }}
              locale={{
                emptyText: 'No data',
              }}
            />
          </Spin>
        </Card>
      </div>

      {/* 目录树选择器 Drawer */}
      <Drawer
        title="Select Directory Path"
        placement="right"
        width={500}
        open={treeVisible}
        onClose={() => setTreeVisible(false)}
        extra={
          <Space>
            <Button onClick={() => setTreeVisible(false)}>Cancel</Button>
            <Button type="primary" onClick={handleConfirmPath}>
              Confirm
            </Button>
          </Space>
        }
      >
        <Spin spinning={treeLoading}>
          <Tree
            showIcon
            defaultExpandAll={false}
            expandedKeys={expandedKeys}
            selectedKeys={selectedKeys}
            onSelect={handleTreeSelect}
            onExpand={handleTreeExpand}
            treeData={treeData}
            style={{ background: '#ffffff' }}
          />
        </Spin>
      </Drawer>
    </div>
  )
}

export default FileListPage
