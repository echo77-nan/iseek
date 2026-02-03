import React from 'react'
import { Button, Card, Typography } from 'antd'
import { GithubOutlined, ScanOutlined, SearchOutlined, BarChartOutlined } from '@ant-design/icons'
import './HomePage.css'

const { Title } = Typography

function HomePage({ onNavigate }) {
  const handleGetStarted = () => {
    if (onNavigate) {
      onNavigate('files')
    }
  }

  const handleQuickScan = () => {
    if (onNavigate) {
      onNavigate('files')
    }
  }

  const handleSmartSearch = () => {
    if (onNavigate) {
      onNavigate('search')
    }
  }

  const handleGenSQLStats = () => {
    if (onNavigate) {
      onNavigate('statistics')
    }
  }

  return (
    <div className="home-page">
      <div className="home-container">
        {/* Left Section - Main Content */}
        <div className="home-left-section">
          {/* Header */}
          <header className="home-header">
            <div className="home-logo">iSEEK</div>
            <nav className="home-nav">
              <a href="#contact" className="home-nav-link">Contact</a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="home-nav-link">
                <GithubOutlined /> Github
              </a>
            </nav>
          </header>

          {/* Hero Section */}
          <section className="home-hero">
            <div className="home-hero-powered">Powered by SeekDB</div>
            <Title level={1} className="home-hero-title">
              Your Personal File Manager, Smart Search & Analytics
            </Title>
            <Button 
              type="primary" 
              size="large" 
              className="home-hero-button"
              onClick={handleGetStarted}
            >
              Get Started
            </Button>
          </section>

          {/* Feature Cards */}
          <section className="home-features">
            <Card className="home-feature-card home-card-scan">
              <div className="home-card-header">
                <Title level={3}>One-Click Scan</Title>
              </div>
              <div className="home-card-body">
                <Button 
                  type="primary" 
                  icon={<ScanOutlined />}
                  onClick={handleQuickScan}
                  className="home-card-button"
                >
                  Quick Scan
                </Button>
              </div>
            </Card>

            <Card className="home-feature-card home-card-search">
              <div className="home-card-header">
                <Title level={3}>AI Search</Title>
              </div>
              <div className="home-card-body">
                <Button 
                  type="primary" 
                  icon={<SearchOutlined />}
                  onClick={handleSmartSearch}
                  className="home-card-button"
                >
                  Smart Search
                </Button>
              </div>
            </Card>

            <Card className="home-feature-card home-card-sql">
              <div className="home-card-header">
                <Title level={3}>GenSQL Intelligent Analysis</Title>
              </div>
              <div className="home-card-body">
                <Button 
                  type="primary" 
                  icon={<BarChartOutlined />}
                  onClick={handleGenSQLStats}
                  className="home-card-button"
                >
                  GenSQL&Stats
                </Button>
              </div>
            </Card>
          </section>
        </div>
      </div>
    </div>
  )
}

export default HomePage
