<template>
  <div class="max-w-2xl space-y-6">
    <!-- Template download -->
    <div class="card">
      <h3 class="text-base font-semibold text-gray-900 mb-2">Format attendu</h3>
      <p class="text-sm text-gray-500 mb-4">
        Téléchargez le template CSV et remplissez-le avec vos transactions.
        Colonnes obligatoires : <code class="bg-gray-100 px-1 rounded">date, amount, type, description</code>.
      </p>
      <button @click="downloadTemplate" class="btn-secondary text-sm">⬇️ Télécharger le template CSV</button>
    </div>

    <!-- Upload zone -->
    <div class="card">
      <h3 class="text-base font-semibold text-gray-900 mb-4">Importer un fichier</h3>

      <div
        class="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-primary-400 transition-colors cursor-pointer"
        :class="{ 'border-primary-500 bg-primary-50': dragOver }"
        @dragover.prevent="dragOver = true"
        @dragleave="dragOver = false"
        @drop.prevent="onDrop"
        @click="fileInput.click()"
      >
        <p class="text-4xl mb-3">📂</p>
        <p class="text-gray-600 font-medium">Glissez un fichier CSV ou Excel ici</p>
        <p class="text-sm text-gray-400 mt-1">ou cliquez pour parcourir</p>
        <p class="text-xs text-gray-300 mt-2">Max 5 MB — .csv, .xlsx, .xls</p>
      </div>
      <input ref="fileInput" type="file" class="hidden" accept=".csv,.xlsx,.xls" @change="onFileSelect" />

      <div v-if="selectedFile" class="mt-4 flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
        <span class="text-2xl">📄</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">{{ selectedFile.name }}</p>
          <p class="text-xs text-gray-400">{{ (selectedFile.size / 1024).toFixed(1) }} KB</p>
        </div>
        <button @click="selectedFile = null" class="text-gray-400 hover:text-gray-600">×</button>
      </div>

      <button
        v-if="selectedFile"
        @click="uploadFile"
        class="btn-primary w-full justify-center mt-4"
        :disabled="loading"
      >
        {{ loading ? 'Import en cours...' : '📤 Importer' }}
      </button>
    </div>

    <!-- Results -->
    <div v-if="result" class="card">
      <h3 class="text-base font-semibold text-gray-900 mb-3">Résultat de l'import</h3>
      <div class="flex gap-4 mb-4">
        <div class="flex-1 bg-emerald-50 rounded-lg p-4 text-center">
          <p class="text-2xl font-bold text-emerald-600">{{ result.created }}</p>
          <p class="text-sm text-emerald-700">transactions importées</p>
        </div>
        <div class="flex-1 bg-red-50 rounded-lg p-4 text-center">
          <p class="text-2xl font-bold text-red-600">{{ result.errors.length }}</p>
          <p class="text-sm text-red-700">erreurs</p>
        </div>
      </div>
      <div v-if="result.errors.length" class="space-y-1">
        <p class="text-sm font-medium text-gray-700">Lignes en erreur :</p>
        <div v-for="e in result.errors" :key="e.row" class="text-xs bg-red-50 text-red-600 px-3 py-1.5 rounded">
          Ligne {{ e.row }} : {{ e.error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { importApi } from '@/api'

const fileInput = ref(null)
const selectedFile = ref(null)
const dragOver = ref(false)
const loading = ref(false)
const result = ref(null)

function onDrop(e) {
  dragOver.value = false
  const f = e.dataTransfer.files[0]
  if (f) selectedFile.value = f
}
function onFileSelect(e) {
  selectedFile.value = e.target.files[0] || null
}

async function uploadFile() {
  loading.value = true
  result.value = null
  try {
    const { data } = await importApi.uploadTransactions(selectedFile.value)
    result.value = data
    selectedFile.value = null
  } finally {
    loading.value = false
  }
}

async function downloadTemplate() {
  const { data } = await importApi.template()
  const header = data.columns.join(',')
  const example = data.columns.map(c => data.example[c] || '').join(',')
  const csv = [header, example].join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = 'budgix-template.csv'; a.click()
  URL.revokeObjectURL(url)
}
</script>
