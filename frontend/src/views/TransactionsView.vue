<template>
  <div class="space-y-4">
    <!-- Filters -->
    <div class="card !p-4">
      <div class="flex flex-wrap gap-3">
        <input v-model="filters.search" class="input w-48" placeholder="Rechercher..." @input="debouncedLoad" />
        <select v-model="filters.type" class="input w-36" @change="loadTx">
          <option value="">Tous types</option>
          <option value="income">Revenus</option>
          <option value="expense">Dépenses</option>
        </select>
        <select v-model="filters.category_id" class="input w-44" @change="loadTx">
          <option value="">Toutes catégories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
        </select>
        <input v-model="filters.date_from" type="date" class="input w-36" @change="loadTx" />
        <input v-model="filters.date_to" type="date" class="input w-36" @change="loadTx" />
        <button @click="openModal()" class="btn-primary ml-auto">+ Nouvelle transaction</button>
      </div>
    </div>

    <!-- Table -->
    <div class="card !p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-4 py-3 text-left font-medium text-gray-500">Date</th>
              <th class="px-4 py-3 text-left font-medium text-gray-500">Description</th>
              <th class="px-4 py-3 text-left font-medium text-gray-500">Catégorie</th>
              <th class="px-4 py-3 text-left font-medium text-gray-500">Tags</th>
              <th class="px-4 py-3 text-right font-medium text-gray-500">Montant</th>
              <th class="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="tx in transactions" :key="tx.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-4 py-3 text-gray-500 whitespace-nowrap">{{ formatDate(tx.date) }}</td>
              <td class="px-4 py-3 font-medium text-gray-900">{{ tx.description }}</td>
              <td class="px-4 py-3 text-gray-500">
                <span v-if="tx.category">{{ tx.category.icon }} {{ tx.category.name }}</span>
                <span v-else class="text-gray-300">—</span>
              </td>
              <td class="px-4 py-3">
                <span v-for="tag in tx.tags" :key="tag" class="inline-block bg-gray-100 text-gray-600 rounded-full px-2 py-0.5 text-xs mr-1">{{ tag }}</span>
              </td>
              <td class="px-4 py-3 text-right font-semibold whitespace-nowrap" :class="tx.type === 'income' ? 'text-emerald-600' : 'text-red-600'">
                {{ tx.type === 'income' ? '+' : '-' }}{{ fmt(tx.amount) }}
              </td>
              <td class="px-4 py-3 text-right">
                <button @click="openModal(tx)" class="text-gray-400 hover:text-primary-600 mr-2">✏️</button>
                <button @click="remove(tx.id)" class="text-gray-400 hover:text-red-600">🗑️</button>
              </td>
            </tr>
            <tr v-if="!transactions.length">
              <td colspan="6" class="px-4 py-8 text-center text-gray-400">Aucune transaction trouvée</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="page.pages > 1" class="flex items-center justify-between px-4 py-3 border-t border-gray-200">
        <p class="text-sm text-gray-500">{{ page.total }} transaction(s)</p>
        <div class="flex gap-2">
          <button class="btn-secondary !py-1 !px-3 text-xs" :disabled="page.page <= 1" @click="changePage(page.page - 1)">‹ Précédent</button>
          <span class="text-sm text-gray-500 flex items-center">{{ page.page }} / {{ page.pages }}</span>
          <button class="btn-secondary !py-1 !px-3 text-xs" :disabled="page.page >= page.pages" @click="changePage(page.page + 1)">Suivant ›</button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <TransactionModal v-if="showModal" :tx="editTx" :categories="categories" @close="showModal = false" @saved="loadTx" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { transactionApi, categoryApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import TransactionModal from '@/components/ui/TransactionModal.vue'

const auth = useAuthStore()
const transactions = ref([])
const categories = ref([])
const page = ref({ page: 1, pages: 1, total: 0 })
const showModal = ref(false)
const editTx = ref(null)

const filters = ref({ search: '', type: '', category_id: '', date_from: '', date_to: '' })

function fmt(v) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: auth.user?.currency || 'EUR' }).format(v)
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('fr-FR')
}

let debounceTimer
function debouncedLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(loadTx, 350)
}

async function loadTx(p = 1) {
  const params = { page: p, size: 20, ...Object.fromEntries(Object.entries(filters.value).filter(([, v]) => v)) }
  const { data } = await transactionApi.list(params)
  transactions.value = data.items
  page.value = data
}

function changePage(p) { loadTx(p) }

function openModal(tx = null) { editTx.value = tx; showModal.value = true }

async function remove(id) {
  if (!confirm('Supprimer cette transaction ?')) return
  await transactionApi.remove(id)
  loadTx()
}

onMounted(async () => {
  const { data } = await categoryApi.list()
  categories.value = data
  loadTx()
})
</script>
