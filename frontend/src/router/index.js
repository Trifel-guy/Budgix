import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Auth
  { path: '/login', name: 'Login', component: () => import('@/views/auth/LoginView.vue'), meta: { public: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/auth/RegisterView.vue'), meta: { public: true } },

  // App
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'transactions', name: 'Transactions', component: () => import('@/views/TransactionsView.vue') },
      { path: 'categories', name: 'Categories', component: () => import('@/views/CategoriesView.vue') },
      { path: 'budgets', name: 'Budgets', component: () => import('@/views/BudgetsView.vue') },
      { path: 'import', name: 'Import', component: () => import('@/views/ImportView.vue') },
      // Admin
      {
        path: 'admin',
        meta: { requiresAdmin: true },
        children: [
          { path: '', redirect: '/admin/dashboard' },
          { path: 'dashboard', name: 'AdminDashboard', component: () => import('@/views/admin/AdminDashboardView.vue') },
          { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/AdminUsersView.vue') },
        ],
      },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  if (auth.isAuthenticated && !auth.user) {
    try { await auth.fetchUser() } catch { auth.logout(); return { name: 'Login' } }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'Dashboard' }
  }
})

export default router
