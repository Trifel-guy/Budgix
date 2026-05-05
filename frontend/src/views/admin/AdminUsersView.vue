<template>
  <div class="space-y-4">
    <div class="flex gap-3">
      <input v-model="search" class="input w-64" placeholder="Rechercher un utilisateur..." @input="debounceLoad" />
    </div>

    <div class="card !p-0 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 text-left font-medium text-gray-500">Utilisateur</th>
            <th class="px-4 py-3 text-left font-medium text-gray-500">Email</th>
            <th class="px-4 py-3 text-left font-medium text-gray-500">Rôle</th>
            <th class="px-4 py-3 text-left font-medium text-gray-500">Statut</th>
            <th class="px-4 py-3 text-left font-medium text-gray-500">Devise</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900">{{ u.full_name }}</td>
            <td class="px-4 py-3 text-gray-500">{{ u.email }}</td>
            <td class="px-4 py-3">
              <span :class="u.role === 'admin' ? 'badge-income' : 'badge-expense'">{{ u.role }}</span>
            </td>
            <td class="px-4 py-3">
              <span :class="u.is_active ? 'badge-income' : 'badge-expense'">{{ u.is_active ? 'Actif' : 'Inactif' }}</span>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ u.currency }}</td>
            <td class="px-4 py-3">
              <button @click="toggleActive(u)" class="text-xs text-gray-400 hover:text-primary-600 underline">
                {{ u.is_active ? 'Désactiver' : 'Activer' }}
              </button>
            </td>
          </tr>
          <tr v-if="!users.length">
            <td colspan="6" class="px-4 py-8 text-center text-gray-400">Aucun utilisateur</td>
          </tr>
        </tbody>
      </table>

      <div v-if="totalPages > 1" class="flex items-center justify-between px-4 py-3 border-t border-gray-200">
        <p class="text-sm text-gray-500">Page {{ page }} / {{ totalPages }}</p>
        <div class="flex gap-2">
          <button class="btn-secondary !py-1 !px-3 text-xs" :disabled="page <= 1" @click="changePage(page - 1)">‹</button>
          <button class="btn-secondary !py-1 !px-3 text-xs" :disabled="page >= totalPages" @click="changePage(page + 1)">›</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'

const users = ref([])
const search = ref('')
const page = ref(1)
const totalPages = ref(1)

let timer
function debounceLoad() {
  clearTimeout(timer)
  timer = setTimeout(() => loadUsers(1), 350)
}

async function loadUsers(p = 1) {
  page.value = p
  const params = { page: p, size: 20 }
  if (search.value) params.search = search.value
  const { data } = await adminApi.listUsers(params)
  users.value = data
  // estimate pages
  totalPages.value = data.length === 20 ? p + 1 : p
}

async function toggleActive(u) {
  await adminApi.updateUser(u.id, { is_active: !u.is_active })
  u.is_active = !u.is_active
}

function changePage(p) { loadUsers(p) }
onMounted(() => loadUsers())
</script>
