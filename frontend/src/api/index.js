import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // 5分钟超时，用于扫描大量文件
})

// 扫描目录
export const scanDirectory = async (path, recursive = true, forceRescan = false) => {
  const response = await api.post('/scan', null, {
    params: { path, recursive, force_rescan: forceRescan },
  })
  return response.data
}

// 搜索文件
export const searchFiles = async (keyword, limit = 100, offset = 0) => {
  const response = await api.get('/search', {
    params: { keyword, limit, offset },
  })
  return response.data
}

// 获取统计信息
export const getStatistics = async () => {
  const response = await api.get('/statistics')
  return response.data
}

// 获取文件列表（pathPrefix 现在是必需的）
export const getFiles = async (pathPrefix, fileType = null, limit = null, offset = 0) => {
  if (!pathPrefix) {
    throw new Error('pathPrefix is required')
  }
  const params = { 
    path_prefix: pathPrefix,
    offset 
  }
  if (fileType) {
    params.file_type = fileType
  }
  if (limit !== null) {
    params.limit = limit
  }
  const response = await api.get('/files', { params })
  return response.data
}

// 生成SQL查询
export const generateSQL = async (query) => {
  const response = await api.post('/generate-sql', null, {
    params: { query },
  })
  return response.data
}

// 执行SQL查询
export const executeSQL = async (sql) => {
  const response = await api.post('/execute-sql', null, {
    params: { sql },
  })
  return response.data
}

// 健康检查
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

// 获取目录树
export const getDirectoryTree = async (rootPath = '/', maxDepth = 10) => {
  const response = await api.get('/directory-tree', {
    params: { root_path: rootPath, max_depth: maxDepth },
  })
  return response.data
}

