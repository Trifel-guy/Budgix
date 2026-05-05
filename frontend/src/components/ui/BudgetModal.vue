<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">Nouveau budget</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">×</button>
      </div>
      <form @submit.prevent="save" class="p-6 space-y-4">
        <div>
          <label class="label">Catégorie</label>
          <select v-model="form.category_id" class="input" required>
            <option value="">Sélectionner...</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
          </select>
        </div>
        <div>
          <label class="label">Montant du budget</label>
          <input v-model="form.amount" type="number" step="0.01" min="1" class="input" required />
        </div>
        <div>
          <label class="label">Seuil d'alerte (%)</label>
          <input v-model="form.alert_threshold" type="number" min="1" max="100" class="input" />
          <p class="text-xs text-gray-400 mt-1">Alerte quand {{ form.alert_threshold }}% du budget est atteint</p>
        </div>
        <div v-if="error" class="text-sm text-red-600 bg-red-50 p-2 rounded">{{ error }}</div>
        <div class="flex gap-3 pt-2">
          <button type="button" class="btn-secondary flex-1 justify-center" @click="$emit('close')">Annuler</button>
          <button type="submit" class="btn-primary flex-1 justify-center" :disabled="loading">
            {{ loading ? '...' : 'Créer' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { budgetApi } from '@/api'

const props = defineProps({ categories: Array, month: Number, year: Number })
const emit = defineEmits(['close', 'saved'])

const form = ref({ category_id: '', amount: '', alert_threshold: 80 })
const loading = ref(false)
const error = ref(null)

async function save() {
  loading.value = true
  error.value = null
  try {
    await budgetApi.create({ ...form.value, amount: parseFloat(form.value.amount), month: props.month, year: props.year })
    emit('saved')
    emit('close')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur'
  } finally {
    loading.value = false
  }
}
</script>
