<template>
  <div class="space-y-6">
    <!-- Period selector -->
    <div class="flex items-center gap-3">
      <select v-model="selectedMonth" class="input w-36">
        <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
      </select>
      <select v-model="selectedYear" class="input w-28">
        <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>

    <!-- Summary cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <SummaryCard label="Revenus" :value="summary.income" color="emerald" icon="📈" :currency="currency" />
      <SummaryCard label="Dépenses" :value="summary.expenses" color="red" icon="📉" :currency="currency" />
      <SummaryCard label="Solde" :value="summary.balance" :color="summary.balance >= 0 ? 'primary' : 'red'" icon="💰" :currency="currency" />
    </div>

    <!-- Charts row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Donut — expenses by category -->
      <div class="card">
        <h3 class="text-base font-semibold text-gray-900 mb-4">Dépenses par catégorie</h3>
        <div v-if="categoryData.length">
          <apexchart type="donut" :options="donutOptions" :series="donutSeries" height="280" />
        </div>
        <div v-else class="h-48 flex items-center justify-center text-gray-400 text-sm">Aucune dépense ce mois</div>
      </div>

      <!-- Bar — monthly trend -->
      <div class="card">
        <h3 class="text-base font-semibold text-gray-900 mb-4">Tendance {{ selectedYear }}</h3>
        <apexchart type="bar" :options="barOptions" :series="barSeries" height="280" />
      </div>
    </div>

    <!-- Recent transactions -->
    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-base font-semibold text-gray-900">Transactions récentes</h3>
        <router-link to="/transactions" class="text-sm text-primary-600 hover:underline">Voir tout →</router-link>
      </div>
      <div v-if="recentTx.length" class="divide-y divide-gray-100">
        <div v-for="tx in recentTx" :key="tx.id" class="flex items-center justify-between py-3">
          <div class="flex items-center gap-3">
            <span class="text-xl">{{ tx.category?.icon || '💸' }}</span>
            <div>
              <p class="text-sm font-medium text-gray-900">{{ tx.description }}</p>
              <p class="text-xs text-gray-500">{{ formatDate(tx.date) }} · {{ tx.category?.name || 'Sans catégorie' }}</p>
            </div>
          </div>
          <span :class="tx.type === 'income' ? 'text-emerald-600 font-semibold' : 'text-red-600 font-semibold'">
            {{ tx.type === 'income' ? '+' : '-' }}{{ formatAmount(tx.amount) }}
          </span>
        </div>
      </div>
      <p v-else class="text-sm text-gray-400 text-center py-6">Aucune transaction</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { dashboardApi } from '@/api'
import SummaryCard from '@/components/ui/SummaryCard.vue'

const auth = useAuthStore()
const currency = computed(() => auth.user?.currency || 'EUR')

const now = new Date()
const selectedMonth = ref(now.getMonth() + 1)
const selectedYear = ref(now.getFullYear())

const summary = ref({ income: 0, expenses: 0, balance: 0 })
const categoryData = ref([])
const trendData = ref([])
const recentTx = ref([])

const months = [
  { value: 1, label: 'Janvier' }, { value: 2, label: 'Février' }, { value: 3, label: 'Mars' },
  { value: 4, label: 'Avril' }, { value: 5, label: 'Mai' }, { value: 6, label: 'Juin' },
  { value: 7, label: 'Juillet' }, { value: 8, label: 'Août' }, { value: 9, label: 'Septembre' },
  { value: 10, label: 'Octobre' }, { value: 11, label: 'Novembre' }, { value: 12, label: 'Décembre' },
]
const years = Array.from({ length: 6 }, (_, i) => now.getFullYear() - 2 + i)

function formatAmount(val) {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: currency.value }).format(val)
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

// Donut chart
const donutSeries = computed(() => categoryData.value.map(c => parseFloat(c.total)))
const donutOptions = computed(() => ({
  labels: categoryData.value.map(c => `${c.icon} ${c.name}`),
  colors: categoryData.value.map(c => c.color),
  legend: { position: 'bottom', fontSize: '12px' },
  dataLabels: { enabled: false },
  tooltip: { y: { formatter: (v) => formatAmount(v) } },
  plotOptions: { pie: { donut: { size: '60%' } } },
}))

// Bar chart
const barSeries = computed(() => [
  { name: 'Revenus', data: trendData.value.map(m => m.income) },
  { name: 'Dépenses', data: trendData.value.map(m => m.expense) },
])
const barOptions = computed(() => ({
  colors: ['#10b981', '#ef4444'],
  chart: { toolbar: { show: false } },
  xaxis: { categories: months.map(m => m.label.slice(0, 3)) },
  yaxis: { labels: { formatter: (v) => `${v}` } },
  legend: { position: 'top' },
  dataLabels: { enabled: false },
  tooltip: { y: { formatter: (v) => formatAmount(v) } },
}))

async function loadData() {
  const [s, cat, trend, recent] = await Promise.all([
    dashboardApi.summary(selectedMonth.value, selectedYear.value),
    dashboardApi.expensesByCategory(selectedMonth.value, selectedYear.value),
    dashboardApi.monthlyTrend(selectedYear.value),
    dashboardApi.recentTransactions(6),
  ])
  summary.value = s.data
  categoryData.value = cat.data
  trendData.value = trend.data
  recentTx.value = recent.data
}

watch([selectedMonth, selectedYear], loadData)
onMounted(loadData)
</script>
