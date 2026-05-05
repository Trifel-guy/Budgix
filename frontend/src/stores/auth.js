import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, userApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshTokenValue = ref(localStorage.getItem('refresh_token') || null)
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email, password) {
    loading.value = true
    try {
      const { data } = await authApi.login({ email, password })
      token.value = data.access_token
      refreshTokenValue.value = data.refresh_token
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      await fetchUser()
    } finally {
      loading.value = false
    }
  }

  async function register(payload) {
    loading.value = true
    try {
      await authApi.register(payload)
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    const { data } = await userApi.me()
    user.value = data
  }

  async function refreshToken() {
    if (!refreshTokenValue.value) throw new Error('No refresh token')
    const { data } = await authApi.refresh(refreshTokenValue.value)
    token.value = data.access_token
    refreshTokenValue.value = data.refresh_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  function logout() {
    token.value = null
    refreshTokenValue.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { token, user, loading, isAuthenticated, isAdmin, login, register, fetchUser, refreshToken, logout }
})
