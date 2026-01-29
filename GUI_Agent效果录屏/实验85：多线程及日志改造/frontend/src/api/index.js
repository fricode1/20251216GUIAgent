import axios from 'axios';

const api = axios.create({
  baseURL: '/violation',
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API 方法
export const violationAPI = {
  // 创建应用
  createApplication: (data) => {
    return api.post('', data);
  },

  // 查询应用列表
  getApplications: (params) => {
    return api.get('', { params });
  },

  // 删除应用
  deleteApplication: (id) => {
    return api.delete(`/${id}`);
  },

  // 查询图片列表
  getImages: (params) => {
    return api.get('/images', { params });
  },
  
  // 查询日志列表
  getLogs: (id) => {
    return api.get(`/${id}/logs`);
  },
};

export default api;
