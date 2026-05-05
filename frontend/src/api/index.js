import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: 15000,
})

// Request interceptor — attach JWT
api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

// Response interceptor — handle 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const auth = useAuthStore()
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true
      try {
        await auth.refreshToken()
        error.config.headers.Authorization = `Bearer ${auth.token}`
        return api(error.config)
      } catch {
        auth.logout()
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default api

// Endpoint helpers
export const authApi = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  refresh: (token) => api.post('/auth/refresh', null, { params: { token } }),
}

export const userApi = {
  me: () => api.get('/users/me'),
  update: (data) => api.patch('/users/me', data),
}

export const categoryApi = {
  list: () => api.get('/categories'),
  create: (data) => api.post('/categories', data),
  update: (id, data) => api.patch(`/categories/${id}`, data),
  remove: (id) => api.delete(`/categories/${id}`),
}

export const transactionApi = {
  list: (params) => api.get('/transactions', { params }),
  create: (data) => api.post('/transactions', data),
  update: (id, data) => api.patch(`/transactions/${id}`, data),
  remove: (id) => api.delete(`/transactions/${id}`),
}

export const budgetApi = {
  list: (params) => api.get('/budgets', { params }),
  create: (data) => api.post('/budgets', data),
  update: (id, data) => api.patch(`/budgets/${id}`, data),
  remove: (id) => api.delete(`/budgets/${id}`),
}

export const dashboardApi = {
  summary: (month, year) => api.get('/dashboard/summary', { params: { month, year } }),
  expensesByCategory: (month, year) => api.get('/dashboard/expenses-by-category', { params: { month, year } }),
  monthlyTrend: (year) => api.get('/dashboard/monthly-trend', { params: { year } }),
  recentTransactions: (limit = 5) => api.get('/dashboard/recent-transactions', { params: { limit } }),
}

export const adminApi = {
  stats: () => api.get('/admin/stats'),
  listUsers: (params) => api.get('/admin/users', { params }),
  getUser: (id) => api.get(`/admin/users/${id}`),
  updateUser: (id, data) => api.patch(`/admin/users/${id}`, data),
}

export const importApi = {
  uploadTransactions: (file) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/import/transactions', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  template: () => api.get('/import/template'),
}
