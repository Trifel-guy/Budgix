<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-3">
      <select v-model="selectedMonth" class="input w-36" @change="loadBudgets">
        <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>
      <select v-model="selectedYear" class="input w-28" @change="loadBudgets">
        <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
      </select>
      <button @click="showModal = true" class="btn-primary ml-auto">+ Nouveau budget</button>
    </div>

    <!-- Budget radial chart -->
    <div v-if="budgets.length" class="card">
      <h3 class="text-base font-semibold text-gray-900 mb-4">Vue d'ensemble</h3>
      <apexchart type="radialBar" :options="radialOptions" :series="radialSeries" height="300" />
    </div>

    <!-- Budget cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="b in budgets" :key="b.id" class="card">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <span class="text-2xl">{{ b.category?.icon || '📁' }}</span>
            <div>
              <p class="font-semibold text-gray-900 text-sm">{{ b.category?.name || 'Catégorie' }}</p>
              <p class="text-xs text-gray-400">Budget : {{ fmt(b.amount) }}</p>
            </div>
          </div>
          <div class="flex gap-1">
            <button @click="removeBudget(b.id)" class="text-gray-300 hover:text-red-500 text-sm">🗑️</button>
          </div>
        </div>

        <!-- Progress bar -->
        <div class="space-y-1">
          <div class="flex justify-between text-xs text-gray-500">
            <span>{{ fmt(b.spent) }} dépensé</span>
            <span :class="b.is_over_budget ? 'text-red-600 font-semibold' : ''">{{ b.percentage.toFixed(0) }}%</span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div
              class="h-2 rounded-full transition-all"
              :style="{ width: Math.min(b.percentage, 100) + '%', backgroundColor: b.is_over_budget ? '#ef4444' : b.is_alert_triggered ? '#f59e0b' : '#10b981' }"
            />
          </div>
          <div class="flex justify-between text-xs">
            <span :class="b.remaining >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ b.remaining >= 0 ? fmt(b.remaining) + ' restant' : fmt(Math.abs(b.remaining)) + ' dépassé' }}
            </span>
            <span v-if="b.is_alert_triggered && !b.is_over_budget" class="text-amber-500 font-medium">⚠️ Alerte</span>
            <span v-if="b.is_over_budget" class="text-red-600 font-medium">🚨 Dépassé</span>
          </div>
        </div>
      </div>

      <div v-if="!budgets.length" class="sm:col-span-2 lg:col-span-3 text-center py-12 text-gray-400">
        Aucun budget pour cette période. Créez-en un !
      </div>
    </div>

    <!-- Modal -->
    <BudgetModal v-if="showModal" :categories="categories" :month="selectedMonth" :year="selectedYear" @close="showModal = false" @saved="loadBudgets" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { budgetApi, categoryApi } from '@/api'
import { useAuthStore } from '@/stores/auth'
import BudgetModal from '@/components/ui/BudgetModal.vue'

const auth = useAuthStore()
const now = new Date()
const selectedMonth = ref(now.getMonth() + 1)
const selectedYear = ref(now.getFullYear())
const budgets = ref([])
const categories = ref([])
const showModal = ref(false)

const months = [
  { value: 1, label: 'Janvier' }, { value: 2, label: 'Février' }, { value: 3, label: 'Mars' },
  { value: 4, label: 'Avril' }, { value: 5, label: 'Mai' }, { value: 6, label: 'Juin' },
  { value: 7, label: 'Juillet' }, { value: 8, label: 'Août' }, { value: 9, label: 'Septembre' },
  { value: 10, label: 'Octobre' }, { value: 11, label: 'Novembre' }, { value: 12, label: 'Décembre' },
]
const years = Array.from({ length: 5 }, (_, i) => now.getFullYear() - 1 + i)

function fmt(v) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: auth.user?.currency || 'EUR' }).format(v)
}

// Radial bar series (% of budget used, capped at 100)
const radialSeries = computed(() => budgets.value.map(b => Math.min(b.percentage, 100)))
const radialOptions = computed(() => ({
  labels: budgets.value.map(b => b.category?.name || 'Budget'),
  colors: budgets.value.map(b => b.is_over_budget ? '#ef4444' : b.category?.color || '#6366f1'),
  plotOptions: { radialBar: { dataLabels: { total: { show: true, label: 'Budgets' } } } },
  legend: { show: true, position: 'bottom' },
}))

async function loadBudgets() {
  const { data } = await budgetApi.list({ month: selectedMonth.value, year: selectedYear.value })
  budgets.value = data
}

async function removeBudget(id) {
  if (!confirm('Supprimer ce budget ?')) return
  await budgetApi.remove(id)
  loadBudgets()
}

onMounted(async () => {
  const { data } = await categoryApi.list()
  categories.value = data.filter(c => c.type === 'expense')
  loadBudgets()
})
</script>
