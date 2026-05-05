<template>
  <div class="space-y-6">
    <h2 class="text-lg font-semibold text-gray-900">Statistiques globales</h2>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card text-center">
        <p class="text-3xl font-bold text-primary-600">{{ stats.total_users }}</p>
        <p class="text-sm text-gray-500 mt-1">Utilisateurs total</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-emerald-600">{{ stats.active_users }}</p>
        <p class="text-sm text-gray-500 mt-1">Utilisateurs actifs</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-primary-600">{{ stats.total_transactions }}</p>
        <p class="text-sm text-gray-500 mt-1">Transactions</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-primary-600">{{ fmtK(stats.total_volume) }}</p>
        <p class="text-sm text-gray-500 mt-1">Volume total</p>
      </div>
    </div>

    <!-- Gauge: active users rate -->
    <div class="card max-w-sm">
      <h3 class="text-base font-semibold text-gray-900 mb-4">Taux d'utilisateurs actifs</h3>
      <apexchart type="radialBar" :options="gaugeOptions" :series="gaugeSeries" height="250" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api'

const stats = ref({ total_users: 0, active_users: 0, total_transactions: 0, total_volume: 0 })

function fmtK(v) {
  if (v >= 1e6) return (v / 1e6).toFixed(1) + 'M €'
  if (v >= 1e3) return (v / 1e3).toFixed(1) + 'k €'
  return v.toFixed(2) + ' €'
}

const gaugeSeries = computed(() => {
  const pct = stats.value.total_users > 0
    ? Math.round(stats.value.active_users / stats.value.total_users * 100)
    : 0
  return [pct]
})

const gaugeOptions = {
  labels: ['Actifs'],
  colors: ['#6366f1'],
  plotOptions: { radialBar: { hollow: { size: '60%' }, dataLabels: { value: { fontSize: '22px', fontWeight: 700 } } } },
}

onMounted(async () => {
  const { data } = await adminApi.stats()
  stats.value = data
})
</script>
