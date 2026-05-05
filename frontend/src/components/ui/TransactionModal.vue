<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">{{ tx ? 'Modifier' : 'Nouvelle transaction' }}</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">×</button>
      </div>

      <form @submit.prevent="save" class="p-6 space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Type</label>
            <select v-model="form.type" class="input" required>
              <option value="expense">Dépense</option>
              <option value="income">Revenu</option>
            </select>
          </div>
          <div>
            <label class="label">Montant</label>
            <input v-model="form.amount" type="number" step="0.01" min="0.01" class="input" required />
          </div>
        </div>

        <div>
          <label class="label">Description</label>
          <input v-model="form.description" type="text" class="input" required />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Date</label>
            <input v-model="form.date" type="date" class="input" required />
          </div>
          <div>
            <label class="label">Catégorie</label>
            <select v-model="form.category_id" class="input">
              <option value="">Sans catégorie</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="label">Tags (séparés par virgule)</label>
          <input v-model="tagsInput" type="text" class="input" placeholder="courses, loisirs" />
        </div>

        <div>
          <label class="label">Note</label>
          <textarea v-model="form.note" class="input resize-none" rows="2" />
        </div>

        <div v-if="error" class="text-sm text-red-600 bg-red-50 p-2 rounded">{{ error }}</div>

        <div class="flex gap-3 pt-2">
          <button type="button" class="btn-secondary flex-1 justify-center" @click="$emit('close')">Annuler</button>
          <button type="submit" class="btn-primary flex-1 justify-center" :disabled="loading">
            {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { transactionApi } from '@/api'

const props = defineProps({ tx: Object, categories: Array })
const emit = defineEmits(['close', 'saved'])

const today = new Date().toISOString().split('T')[0]
const form = ref({ type: 'expense', amount: '', description: '', date: today, category_id: '', note: '' })
const tagsInput = ref('')
const loading = ref(false)
const error = ref(null)

onMounted(() => {
  if (props.tx) {
    Object.assign(form.value, { ...props.tx, category_id: props.tx.category_id || '' })
    tagsInput.value = (props.tx.tags || []).join(', ')
  }
})

async function save() {
  loading.value = true
  error.value = null
  try {
    const payload = {
      ...form.value,
      amount: parseFloat(form.value.amount),
      tags: tagsInput.value.split(',').map(t => t.trim()).filter(Boolean),
      category_id: form.value.category_id || null,
    }
    if (props.tx) {
      await transactionApi.update(props.tx.id, payload)
    } else {
      await transactionApi.create(payload)
    }
    emit('saved')
    emit('close')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur lors de l\'enregistrement'
  } finally {
    loading.value = false
  }
}
</script>
