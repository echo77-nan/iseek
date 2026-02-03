import React, { useState, useEffect } from 'react'
import { 
  Card, 
  Typography, 
  Spin, 
  message, 
  Tabs, 
  Table, 
  Tag, 
  Input, 
  Button, 
  Space,
  Divider
} from 'antd'
import { 
  PlayCircleOutlined, 
  ThunderboltOutlined,
  GithubOutlined,
  CodeOutlined,
  HomeOutlined
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'
import { getStatistics, generateSQL, executeSQL } from '../api'
import '../App.css'

const { Title, Text } = Typography
const { TextArea } = Input

function StatisticsPage({ onNavigate }) {
  const [loading, setLoading] = useState(false)
  const [statistics, setStatistics] = useState(null)
  const [sqlQueries, setSqlQueries] = useState([])
  const [charts, setCharts] = useState([])
  const [insights, setInsights] = useState([])
  
  // SQL生成和执行相关状态
  const [naturalLanguageQuery, setNaturalLanguageQuery] = useState('')
  const [generatedSQL, setGeneratedSQL] = useState('')
  const [sqlDescription, setSqlDescription] = useState('')
  const [sqlExplanation, setSqlExplanation] = useState('')
  const [generatingSQL, setGeneratingSQL] = useState(false)
  const [executingSQL, setExecutingSQL] = useState(false)
  const [sqlResults, setSqlResults] = useState([])
  const [sqlError, setSqlError] = useState('')

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    setLoading(true)
    try {
      const response = await getStatistics()
      if (response.success) {
        setStatistics(response.statistics)
        setSqlQueries(response.sql_queries || [])
        setCharts(response.charts || [])
        setInsights(response.insights || [])
      } else {
        message.error('Failed to get statistics')
      }
    } catch (error) {
      message.error('Failed to get statistics: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateSQL = async () => {
    if (!naturalLanguageQuery.trim()) {
      message.warning('Please enter a query in natural language')
      return
    }

    setGeneratingSQL(true)
    setSqlError('')
    setSqlResults([])
    try {
      const response = await generateSQL(naturalLanguageQuery)
      if (response.success) {
        setGeneratedSQL(response.sql || '')
        setSqlDescription(response.description || '')
        setSqlExplanation(response.explanation || '')
        if (response.sql) {
          message.success('SQL generated successfully')
        } else {
          message.warning('Failed to generate SQL')
        }
      } else {
        message.error('Failed to generate SQL')
      }
    } catch (error) {
      message.error('Failed to generate SQL: ' + error.message)
      setSqlError(error.message)
    } finally {
      setGeneratingSQL(false)
    }
  }

  const handleExecuteSQL = async () => {
    if (!generatedSQL.trim()) {
      message.warning('Please generate SQL first')
      return
    }

    setExecutingSQL(true)
    setSqlError('')
    setSqlResults([])
    try {
      const response = await executeSQL(generatedSQL)
      if (response.success) {
        setSqlResults(response.results || [])
        message.success(`Query executed successfully, returned ${response.count || 0} rows`)
      } else {
        message.error('Failed to execute SQL')
      }
    } catch (error) {
      message.error('Failed to execute SQL: ' + error.message)
      setSqlError(error.message)
    } finally {
      setExecutingSQL(false)
    }
  }

  const renderTypeChart = () => {
    if (!statistics || !statistics.by_type) return null

    const data = statistics.by_type.map((item) => ({
      value: item.count,
      name: item.file_type || 'Unknown',
    }))

    const option = {
      title: {
        text: 'File Type Distribution',
        left: 'center',
        textStyle: {
          color: '#000000',
        },
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        textStyle: {
          color: '#000000',
        },
      },
      series: [
        {
          name: 'File Type',
          type: 'pie',
          radius: '50%',
          data: data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    }

    return <ReactECharts option={option} style={{ height: '400px' }} />
  }

  const renderExtensionChart = () => {
    if (!statistics || !statistics.by_extension) return null

    const data = statistics.by_extension.map((item) => item.file_extension)
    const values = statistics.by_extension.map((item) => item.count)

    const option = {
      title: {
        text: 'File Extension Distribution (Top 20)',
        left: 'center',
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      xAxis: {
        type: 'category',
        data: data,
        axisLabel: {
          rotate: 45,
          color: '#000000',
        },
        axisLine: {
          lineStyle: {
            color: '#e0e0e0',
          },
        },
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#000000',
        },
        splitLine: {
          lineStyle: {
            color: '#e0e0e0',
          },
        },
      },
      series: [
        {
          name: 'File Count',
          type: 'bar',
          data: values,
          itemStyle: {
            color: '#000000',
          },
        },
      ],
    }

    return <ReactECharts option={option} style={{ height: '400px' }} />
  }

  const renderSizeChart = () => {
    if (!statistics || !statistics.by_size) return null

    const data = statistics.by_size.map((item) => ({
      value: item.count,
      name: item.size_range,
    }))

    const option = {
      title: {
        text: 'File Size Distribution',
        left: 'center',
        textStyle: {
          color: '#000000',
        },
      },
      tooltip: {
        trigger: 'item',
      },
      series: [
        {
          name: 'File Size',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#ffffff',
            borderWidth: 2,
          },
          label: {
            show: false,
            position: 'center',
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '30',
              fontWeight: 'bold',
              color: '#000000',
            },
          },
          labelLine: {
            show: false,
          },
          data: data,
        },
      ],
    }

    return <ReactECharts option={option} style={{ height: '400px' }} />
  }

  const sqlColumns = [
    {
      title: 'Query Name',
      dataIndex: 'name',
      key: 'name',
      render: (text) => <Text style={{ color: '#000000' }}>{text}</Text>,
    },
    {
      title: 'SQL Statement',
      dataIndex: 'sql',
      key: 'sql',
      render: (text) => (
        <code style={{ background: '#f5f5f5', padding: '4px 8px', borderRadius: 4, border: '1px solid #e0e0e0', color: '#000000' }}>
          {text}
        </code>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      render: (text) => <Text style={{ color: '#666666' }}>{text}</Text>,
    },
  ]

  const tabItems = [
    {
      key: 'overview',
      label: 'Overview',
      children: (
        <div>
          <Card style={{ marginBottom: 24, background: '#ffffff', border: '1px solid #e0e0e0' }}>
            <Title level={4} style={{ color: '#000000' }}>Statistics Overview</Title>
            <div style={{ fontSize: '16px', lineHeight: '32px', color: '#000000' }}>
              <p>
                <strong>Total Files:</strong>
                {statistics?.total_files || 0}
              </p>
              {insights.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <Title level={5} style={{ color: '#000000' }}>AI Insights</Title>
                  <ul>
                    {insights.map((insight, index) => (
                      <li key={index}>{insight}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </Card>
        </div>
      ),
    },
    {
      key: 'charts',
      label: 'Charts',
      children: (
        <div>
          <Card className="chart-container">{renderTypeChart()}</Card>
          <Card className="chart-container">{renderExtensionChart()}</Card>
          <Card className="chart-container">{renderSizeChart()}</Card>
        </div>
      ),
    },
    {
      key: 'sql',
      label: 'SQL Queries',
      children: (
        <div>
          <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0', marginBottom: 24 }}>
            <Title level={4} style={{ color: '#000000', marginBottom: 16 }}>Natural Language to SQL</Title>
            <Space direction="vertical" style={{ width: '100%' }} size="large">
              <div>
                <Text strong style={{ color: '#000000', display: 'block', marginBottom: 8 }}>
                  Enter your query in natural language:
                </Text>
                <TextArea
                  rows={3}
                  placeholder="e.g., Show me all image files larger than 10MB, or Find all Python code files created in the last month"
                  value={naturalLanguageQuery}
                  onChange={(e) => setNaturalLanguageQuery(e.target.value)}
                  style={{ 
                    background: '#ffffff', 
                    border: '1px solid #d9d9d9',
                    color: '#000000'
                  }}
                />
              </div>
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                onClick={handleGenerateSQL}
                loading={generatingSQL}
                style={{
                  background: '#000000',
                  borderColor: '#000000',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#333333'
                  e.currentTarget.style.borderColor = '#333333'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#000000'
                  e.currentTarget.style.borderColor = '#000000'
                }}
              >
                Generate SQL
              </Button>
            </Space>
          </Card>

          {generatedSQL && (
            <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0', marginBottom: 24 }}>
              <Title level={4} style={{ color: '#000000', marginBottom: 16 }}>
                <CodeOutlined /> Generated SQL Query
              </Title>
              {sqlDescription && (
                <div style={{ marginBottom: 12 }}>
                  <Text style={{ color: '#666666' }}>{sqlDescription}</Text>
                </div>
              )}
              <div style={{ 
                background: '#f5f5f5', 
                padding: '12px', 
                borderRadius: '6px',
                border: '1px solid #e0e0e0',
                marginBottom: 16
              }}>
                <Text code style={{ color: '#000000', fontSize: '14px', whiteSpace: 'pre-wrap' }}>
                  {generatedSQL}
                </Text>
              </div>
              {sqlExplanation && (
                <div style={{ marginBottom: 12, padding: '8px', background: '#f5f5f5', borderRadius: '4px' }}>
                  <Text style={{ color: '#666666', fontSize: '12px' }}>{sqlExplanation}</Text>
                </div>
              )}
              <Button
                type="primary"
                icon={<PlayCircleOutlined />}
                onClick={handleExecuteSQL}
                loading={executingSQL}
                style={{
                  background: '#000000',
                  borderColor: '#000000',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#333333'
                  e.currentTarget.style.borderColor = '#333333'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#000000'
                  e.currentTarget.style.borderColor = '#000000'
                }}
              >
                Execute SQL
              </Button>
            </Card>
          )}

          {sqlError && (
            <Card style={{ background: '#ffffff', border: '1px solid #ff4d4f', marginBottom: 24 }}>
              <Text style={{ color: '#ff4d4f' }}>Error: {sqlError}</Text>
            </Card>
          )}

          {sqlResults.length > 0 && (
            <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0' }}>
              <Title level={4} style={{ color: '#000000', marginBottom: 16 }}>
                Query Results ({sqlResults.length} rows)
              </Title>
              <Table
                dataSource={sqlResults.map((row, index) => ({ ...row, key: index }))}
                columns={Object.keys(sqlResults[0] || {}).map(key => ({
                  title: key,
                  dataIndex: key,
                  key: key,
                  ellipsis: true,
                }))}
                pagination={{
                  pageSize: 20,
                  showSizeChanger: true,
                }}
                scroll={{ x: 'max-content' }}
              />
            </Card>
          )}

          {sqlQueries.length > 0 && (
            <>
              <Divider style={{ borderColor: '#e0e0e0', margin: '24px 0' }}>
                <Text style={{ color: '#666666' }}>Pre-generated SQL Queries</Text>
              </Divider>
              <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0' }}>
                <Title level={4} style={{ color: '#000000' }}>AI Generated SQL Queries</Title>
                <Table
                  columns={sqlColumns}
                  dataSource={sqlQueries.map((q, index) => ({ ...q, key: index }))}
                  pagination={false}
                />
              </Card>
            </>
          )}
        </div>
      ),
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

      {/* 主标题区域 */}
      <div style={{ padding: '40px 24px 24px 24px' }}>
        <Title level={1} style={{ color: '#000000', marginBottom: '32px', fontSize: '32px', fontWeight: 600 }}>
          GenSQL Intelligent File Query, Elevate Your Data Workflow
        </Title>

        <Spin spinning={loading}>
          {statistics ? (
            <Tabs 
              items={tabItems}
              style={{
                background: '#ffffff',
                padding: '24px',
                borderRadius: '8px',
                border: '1px solid #e0e0e0',
              }}
            />
          ) : (
            <Card style={{ background: '#ffffff', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
              <p style={{ color: '#666666' }}>No statistics available, please scan files first</p>
            </Card>
          )}
        </Spin>
      </div>
    </div>
  )
}

export default StatisticsPage

