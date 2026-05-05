<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside
      :class="[
        'flex flex-col w-64 bg-white border-r border-gray-200 transition-transform duration-300 fixed inset-y-0 z-40 lg:static lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-2 px-6 py-5 border-b border-gray-200">
        <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">B</span>
        </div>
        <span class="text-xl font-bold text-gray-900">Budgix</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <NavItem to="/dashboard" icon="home">Tableau de bord</NavItem>
        <NavItem to="/transactions" icon="list">Transactions</NavItem>
        <NavItem to="/budgets" icon="chart">Budgets</NavItem>
        <NavItem to="/categories" icon="tag">Catégories</NavItem>
        <NavItem to="/import" icon="upload">Importer</NavItem>

        <template v-if="auth.isAdmin">
          <div class="pt-4 pb-1 px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">Admin</div>
          <NavItem to="/admin/dashboard" icon="shield">Vue globale</NavItem>
          <NavItem to="/admin/users" icon="users">Utilisateurs</NavItem>
        </template>
      </nav>

      <!-- User -->
      <div class="border-t border-gray-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-semibold text-sm">
            {{ initials }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">{{ auth.user?.full_name }}</p>
            <p class="text-xs text-gray-500 truncate">{{ auth.user?.email }}</p>
          </div>
          <button @click="auth.logout(); $router.push('/login')" class="text-gray-400 hover:text-gray-600" title="Déconnexion">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Overlay mobile -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/40 z-30 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Main -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Top bar -->
      <header class="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-4 lg:px-6">
        <button class="lg:hidden text-gray-500 hover:text-gray-700" @click="sidebarOpen = !sidebarOpen">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <h1 class="text-lg font-semibold text-gray-900">{{ pageTitle }}</h1>
      </header>

      <main class="flex-1 overflow-y-auto p-4 lg:p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavItem from './NavItem.vue'

const auth = useAuthStore()
const route = useRoute()
const sidebarOpen = ref(false)

const initials = computed(() => {
  const name = auth.user?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const titles = {
  Dashboard: 'Tableau de bord',
  Transactions: 'Transactions',
  Budgets: 'Budgets',
  Categories: 'Catégories',
  Import: 'Importer des données',
  AdminDashboard: 'Admin — Vue globale',
  AdminUsers: 'Admin — Utilisateurs',
}

const pageTitle = computed(() => titles[route.name] || 'Budgix')
</script>
