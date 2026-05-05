<template>
  <div class="space-y-6">
    <div class="flex justify-end">
      <button @click="openModal()" class="btn-primary">+ Nouvelle catégorie</button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div v-for="section in ['income', 'expense']" :key="section">
        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
          {{ section === 'income' ? '📈 Revenus' : '📉 Dépenses' }}
        </h3>
        <div class="space-y-2">
          <div
            v-for="cat in byType(section)"
            :key="cat.id"
            class="card !p-4 flex items-center justify-between"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center text-xl" :style="{ backgroundColor: cat.color + '20' }">
                {{ cat.icon }}
              </div>
              <span class="font-medium text-gray-900">{{ cat.name }}</span>
            </div>
            <div class="flex gap-2">
              <button @click="openModal(cat)" class="text-gray-400 hover:text-primary-600">✏️</button>
              <button @click="remove(cat.id)" class="text-gray-400 hover:text-red-600">🗑️</button>
            </div>
          </div>
          <div v-if="!byType(section).length" class="text-sm text-gray-400 text-center py-4">
            Aucune catégorie
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold">{{ editCat ? 'Modifier' : 'Nouvelle' }} catégorie</h2>
          <button @click="showModal = false" class="text-gray-400 text-xl">×</button>
        </div>
        <form @submit.prevent="saveCategory" class="p-6 space-y-4">
          <div>
            <label class="label">Nom</label>
            <input v-model="form.name" type="text" class="input" required />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Icône</label>
              <input v-model="form.icon" type="text" class="input text-center text-xl" maxlength="2" />
            </div>
            <div>
              <label class="label">Couleur</label>
              <input v-model="form.color" type="color" class="input !p-1 !h-10 cursor-pointer" />
            </div>
          </div>
          <div v-if="!editCat">
            <label class="label">Type</label>
            <select v-model="form.type" class="input" required>
              <option value="expense">Dépense</option>
              <option value="income">Revenu</option>
            </select>
          </div>
          <div class="flex gap-3 pt-2">
            <button type="button" class="btn-secondary flex-1 justify-center" @click="showModal = false">Annuler</button>
            <button type="submit" class="btn-primary flex-1 justify-center">Enregistrer</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { categoryApi } from '@/api'

const categories = ref([])
const showModal = ref(false)
const editCat = ref(null)
const form = ref({ name: '', icon: '💰', color: '#6366f1', type: 'expense' })

const byType = (type) => categories.value.filter(c => c.type === type)

function openModal(cat = null) {
  editCat.value = cat
  if (cat) Object.assign(form.value, cat)
  else form.value = { name: '', icon: '💰', color: '#6366f1', type: 'expense' }
  showModal.value = true
}

async function saveCategory() {
  if (editCat.value) {
    await categoryApi.update(editCat.value.id, { name: form.value.name, icon: form.value.icon, color: form.value.color })
  } else {
    await categoryApi.create(form.value)
  }
  showModal.value = false
  await loadCategories()
}

async function remove(id) {
  if (!confirm('Supprimer cette catégorie ?')) return
  await categoryApi.remove(id)
  await loadCategories()
}

async function loadCategories() {
  const { data } = await categoryApi.list()
  categories.value = data
}

onMounted(loadCategories)
</script>
