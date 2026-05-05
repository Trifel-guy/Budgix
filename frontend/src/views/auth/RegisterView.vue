<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-lg mb-4">
          <span class="text-3xl font-bold text-primary-600">B</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Budgix</h1>
        <p class="text-primary-100 mt-1">Créez votre compte gratuitement</p>
      </div>

      <div class="card">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Inscription</h2>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="label">Nom complet</label>
            <input v-model="form.full_name" type="text" class="input" placeholder="Jean Dupont" required />
          </div>
          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" class="input" placeholder="you@example.com" required />
          </div>
          <div>
            <label class="label">Mot de passe</label>
            <input v-model="form.password" type="password" class="input" placeholder="8 caractères min." required minlength="8" />
          </div>
          <div>
            <label class="label">Devise</label>
            <select v-model="form.currency" class="input">
              <option value="EUR">EUR — Euro</option>
              <option value="USD">USD — Dollar US</option>
              <option value="GBP">GBP — Livre Sterling</option>
              <option value="MAD">MAD — Dirham</option>
            </select>
          </div>

          <div v-if="error" class="rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">
            {{ error }}
          </div>
          <div v-if="success" class="rounded-lg bg-emerald-50 border border-emerald-200 p-3 text-sm text-emerald-700">
            Compte créé ! <router-link to="/login" class="font-semibold underline">Se connecter</router-link>
          </div>

          <button type="submit" class="btn-primary w-full justify-center" :disabled="auth.loading">
            <span v-if="auth.loading">Création...</span>
            <span v-else>Créer mon compte</span>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-4">
          Déjà un compte ?
          <router-link to="/login" class="text-primary-600 font-medium hover:underline">Se connecter</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const form = ref({ full_name: '', email: '', password: '', currency: 'EUR' })
const error = ref(null)
const success = ref(false)

async function handleRegister() {
  error.value = null
  success.value = false
  try {
    await auth.register(form.value)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur lors de la création du compte'
  }
}
</script>
