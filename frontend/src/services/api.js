import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 错误处理拦截器
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// API服务类
const apiService = {
  // 浏览器AI任务相关接口
  executeBrowserTask: async (taskData) => {
    const response = await apiClient.post('/ai/task', taskData);
    return response.data;
  },
  
  // 社交媒体相关接口
  collectSocialData: async (params) => {
    const response = await apiClient.post('/ai/social/collect', params);
    return response.data;
  },
  
  analyzeSocialTrends: async (params) => {
    const response = await apiClient.post('/ai/social/trending', params);
    return response.data;
  },
  
  generateContentIdeas: async (params) => {
    const response = await apiClient.post('/ai/social/content-ideas', params);
    return response.data;
  },
  
  // 电商相关接口
  searchProducts: async (params) => {
    const response = await apiClient.post('/ai/ecommerce/products', params);
    return response.data;
  },
  
  generateListing: async (params) => {
    const response = await apiClient.post('/ai/ecommerce/listing', params);
    return response.data;
  },
  
  analyzeCompetition: async (params) => {
    const response = await apiClient.post('/ai/ecommerce/competition', params);
    return response.data;
  },
  
  findSuppliers: async (params) => {
    const response = await apiClient.post('/ai/ecommerce/suppliers', params);
    return response.data;
  },
  
  analyzeProductPotential: async (params) => {
    const response = await apiClient.post('/ai/ecommerce/product-potential', params);
    return response.data;
  },
  
  // 聊天相关接口
  sendChatMessage: async (message) => {
    const response = await apiClient.post('/ai/chat', { message });
    return response.data;
  },
  
  // 通用任务相关接口
  createTask: async (taskData) => {
    const response = await apiClient.post('/ai/task', taskData);
    return response.data;
  },
  
  getTasks: async (filters = {}) => {
    const response = await apiClient.get('/ai/tasks', { params: filters });
    return response.data;
  },
  
  getTaskById: async (taskId) => {
    const response = await apiClient.get(`/ai/tasks/${taskId}`);
    return response.data;
  },
  
  updateTask: async (taskId, taskData) => {
    const response = await apiClient.put(`/ai/tasks/${taskId}`, taskData);
    return response.data;
  },
  
  deleteTask: async (taskId) => {
    const response = await apiClient.delete(`/ai/tasks/${taskId}`);
    return response.data;
  },
};

export default apiService; 