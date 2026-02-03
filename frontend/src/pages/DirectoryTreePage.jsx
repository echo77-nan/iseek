import React, { useState, useEffect } from 'react'
import {
  Tree,
  Card,
  Typography,
  Button,
  Input,
  Space,
  message,
  Spin,
  Empty,
} from 'antd'
import {
  FolderOutlined,
  FolderOpenOutlined,
  ScanOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import { getDirectoryTree, scanDirectory } from '../api'
import '../App.css'

const { Title, Text } = Typography
const { Search } = Input

function DirectoryTreePage({ onNavigate }) {
  const [treeData, setTreeData] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedPath, setSelectedPath] = useState('')
  const [scanning, setScanning] = useState(false)
  const [expandedKeys, setExpandedKeys] = useState([])
  const [searchValue, setSearchValue] = useState('')
  const [autoExpandParent, setAutoExpandParent] = useState(true)

  useEffect(() => {
    loadDirectoryTree()
  }, [])

  const loadDirectoryTree = async () => {
    setLoading(true)
    try {
      const response = await getDirectoryTree('/', 10)
      if (response.success) {
        const formattedTree = formatTreeData([response.tree])
        setTreeData(formattedTree)
        // 默认展开根节点
        if (formattedTree.length > 0) {
          setExpandedKeys([formattedTree[0].key])
        }
      } else {
        message.error('Failed to load directory tree')
      }
    } catch (error) {
      message.error('Failed to load directory tree: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const formatTreeData = (nodes, parentKey = '') => {
    if (!nodes || !Array.isArray(nodes)) {
      return []
    }

    return nodes.map((node, index) => {
      const key = parentKey ? `${parentKey}-${index}` : `root-${index}`
      const formattedNode = {
        title: (
          <span
            onClick={() => handleNodeSelect(node.path)}
            style={{
              cursor: 'pointer',
              padding: '4px 8px',
              borderRadius: '4px',
              display: 'inline-block',
              width: '100%',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#f5f5f5'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <Text strong style={{ color: '#000000' }}>
              {node.name}
            </Text>
            <Text
              style={{
                color: '#666666',
                fontSize: '12px',
                marginLeft: '8px',
              }}
            >
              ({node.path})
            </Text>
          </span>
        ),
        key: key,
        path: node.path,
        icon: <FolderOutlined />,
        children: node.children && node.children.length > 0
          ? formatTreeData(node.children, key)
          : undefined,
      }
      return formattedNode
    })
  }

  const handleNodeSelect = (path) => {
    setSelectedPath(path)
    message.info(`Selected path: ${path}`)
  }

  const handleScan = async () => {
    if (!selectedPath) {
      message.warning('Please select a directory path first')
      return
    }

    setScanning(true)
    try {
      const response = await scanDirectory(selectedPath, true, false)
      if (response.success) {
        // 保存选中的路径到 localStorage，以便 FileListPage 使用
        const normalizedPath = response.path || selectedPath
        localStorage.setItem('lastScanPath', normalizedPath)
        
        if (response.status === 'cached') {
          message.success(
            `Using cached data from database (${response.file_count} files found)`
          )
        } else {
          message.success('Scan task started, processing in background...')
        }
        // 导航到文件列表页面
        if (onNavigate) {
          onNavigate('files')
        }
      } else {
        message.error('Scan failed')
      }
    } catch (error) {
      message.error('Scan failed: ' + error.message)
    } finally {
      setScanning(false)
    }
  }

  const onExpand = (expandedKeysValue) => {
    setExpandedKeys(expandedKeysValue)
    setAutoExpandParent(false)
  }

  const getParentKey = (key, tree) => {
    let parentKey
    for (let i = 0; i < tree.length; i++) {
      const node = tree[i]
      if (node.children) {
        if (node.children.some((item) => item.key === key)) {
          parentKey = node.key
        } else if (getParentKey(key, node.children)) {
          parentKey = getParentKey(key, node.children)
        }
      }
    }
    return parentKey
  }

  const onSearch = (value) => {
    setSearchValue(value)
    setExpandedKeys([])
    setAutoExpandParent(true)
  }

  const filterTreeData = (data, searchValue) => {
    if (!searchValue) {
      return data
    }

    const filter = (nodes) => {
      return nodes
        .map((node) => {
          const match = node.path
            .toLowerCase()
            .includes(searchValue.toLowerCase())
          const children = node.children ? filter(node.children) : []

          if (match || children.length > 0) {
            return {
              ...node,
              children: children.length > 0 ? children : undefined,
            }
          }
          return null
        })
        .filter((node) => node !== null)
    }

    return filter(data)
  }

  const displayTreeData = searchValue
    ? filterTreeData(treeData, searchValue)
    : treeData

  return (
    <div style={{ minHeight: '100vh', background: 'rgba(113, 188, 32, 0.05)' }}>
      {/* Desktop · Primary 标题 */}
      <div style={{ padding: '16px 24px', color: '#666666', fontSize: '14px' }}>
        Desktop · Primary
      </div>

      <div style={{ padding: '24px' }}>
        <Title level={2} style={{ color: '#000000', marginBottom: '24px' }}>
          Directory Tree
        </Title>

        <Card
          style={{
            background: '#ffffff',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            marginBottom: '24px',
          }}
        >
          <Space direction="vertical" style={{ width: '100%' }} size="large">
            <Space style={{ width: '100%' }}>
              <Search
                placeholder="Search directory path..."
                allowClear
                onSearch={onSearch}
                onChange={(e) => onSearch(e.target.value)}
                style={{ flex: 1, maxWidth: '400px' }}
              />
              <Button
                icon={<ReloadOutlined />}
                onClick={loadDirectoryTree}
                loading={loading}
                style={{
                  background: '#ffffff',
                  borderColor: '#d9d9d9',
                  color: '#000000',
                }}
              >
                Refresh
              </Button>
            </Space>

            {selectedPath && (
              <div
                style={{
                  padding: '12px',
                  background: '#f5f5f5',
                  borderRadius: '4px',
                  border: '1px solid #e0e0e0',
                }}
              >
                <Text strong style={{ color: '#000000' }}>
                  Selected Path:
                </Text>
                <Text style={{ color: '#666666', marginLeft: '8px' }}>
                  {selectedPath}
                </Text>
              </div>
            )}

            <Button
              type="primary"
              icon={<ScanOutlined />}
              onClick={handleScan}
              loading={scanning}
              disabled={!selectedPath}
              style={{
                background: '#000000',
                borderColor: '#000000',
                width: '100%',
                maxWidth: '200px',
              }}
            >
              Scan Selected Directory
            </Button>
          </Space>
        </Card>

        <Card
          style={{
            background: '#ffffff',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            minHeight: '500px',
          }}
        >
          <Spin spinning={loading}>
            {treeData.length > 0 ? (
              <Tree
                showIcon
                defaultExpandAll={false}
                onExpand={onExpand}
                expandedKeys={expandedKeys}
                autoExpandParent={autoExpandParent}
                treeData={displayTreeData}
                style={{
                  color: '#000000',
                  fontSize: '14px',
                }}
              />
            ) : (
              <Empty
                description="No directory tree data available"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
            )}
          </Spin>
        </Card>
      </div>
    </div>
  )
}

export default DirectoryTreePage

