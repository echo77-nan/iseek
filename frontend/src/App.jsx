import React, { useState } from 'react'
import { Layout, Menu, theme, ConfigProvider } from 'antd'
import { 
  SearchOutlined, 
  DatabaseOutlined, 
  BarChartOutlined,
  GithubOutlined,
  FileSearchOutlined,
  FolderOutlined,
  ReloadOutlined,
  ScanOutlined,
  PlayCircleOutlined,
  PlusOutlined
} from '@ant-design/icons'
import SearchPage from './pages/SearchPage'
import StatisticsPage from './pages/StatisticsPage'
import FileListPage from './pages/FileListPage'
import HomePage from './pages/HomePage'
import DirectoryTreePage from './pages/DirectoryTreePage'
import './App.css'

const { Header, Content, Sider } = Layout

// 浅色主题配置（与 Figma 设计保持一致）
const lightTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorBgBase: '#ffffff',
    colorBgContainer: '#ffffff',
    colorBgElevated: '#ffffff',
    colorBorder: '#e0e0e0',
    colorText: '#000000',
    colorTextSecondary: '#666666',
    colorPrimary: '#000000',
    borderRadius: 6,
  },
  components: {
    Card: {
      colorBgContainer: '#ffffff',
      colorBorderSecondary: '#e0e0e0',
    },
    Input: {
      colorBgContainer: '#ffffff',
      colorBorder: '#d9d9d9',
      activeBorderColor: '#000000',
      hoverBorderColor: '#000000',
    },
    Button: {
      primaryColor: '#ffffff',
      primaryBg: '#000000',
    },
    Table: {
      colorBgContainer: '#ffffff',
      colorBorderSecondary: '#e0e0e0',
      headerBg: '#fafafa',
      headerColor: '#000000',
    },
    Select: {
      colorBgContainer: '#ffffff',
      colorBorder: '#d9d9d9',
    },
    Menu: {
      itemSelectedBg: '#f5f5f5',
      itemHoverBg: '#fafafa',
      itemColor: '#000000',
      itemSelectedColor: '#000000',
    },
  },
}

function App() {
  const [selectedKey, setSelectedKey] = useState('home')
  const {
    token: { colorBgContainer },
  } = theme.useToken()

  const handleNavigate = (key) => {
    setSelectedKey(key)
  }

  const getPagePath = () => {
    switch (selectedKey) {
      case 'files':
        return '/search'
      case 'search':
        return '/scan'
      case 'statistics':
        return '/gensql'
      case 'directory-tree':
        return '/directory-tree'
      default:
        return ''
    }
  }

  const renderContent = () => {
    switch (selectedKey) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />
      case 'files':
        return <FileListPage onNavigate={handleNavigate} />
      case 'search':
        return <SearchPage onNavigate={handleNavigate} />
      case 'statistics':
        return <StatisticsPage onNavigate={handleNavigate} />
      case 'directory-tree':
        return <DirectoryTreePage onNavigate={handleNavigate} />
      default:
        return <HomePage onNavigate={handleNavigate} />
    }
  }

  // 如果是首页，不显示侧边栏和Header
  if (selectedKey === 'home') {
    return <HomePage onNavigate={handleNavigate} />
  }

  return (
    <ConfigProvider theme={lightTheme}>
      <Layout style={{ minHeight: '100vh', background: 'rgba(113, 188, 32, 0.05)' }}>
        {/* 顶部导航栏 - 根据 Figma 设计 */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '16px 24px',
          background: '#ffffff',
          borderBottom: '1px solid #e0e0e0',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PlayCircleOutlined style={{ fontSize: '16px', color: '#666666' }} />
            <span style={{ color: selectedKey === 'search' ? '#1890ff' : '#666666', fontSize: '14px' }}>
              {getPagePath()}
            </span>
          </div>
          <PlusOutlined style={{ fontSize: '16px', color: '#666666', cursor: 'pointer' }} />
        </div>
        
        <Layout style={{ background: 'rgba(113, 188, 32, 0.05)' }}>
          <Content
            style={{
              padding: 0,
              margin: 0,
              minHeight: 'calc(100vh - 57px)',
              background: 'rgba(113, 188, 32, 0.05)',
            }}
          >
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}

export default App

