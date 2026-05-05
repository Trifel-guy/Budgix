<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-lg mb-4">
          <span class="text-3xl font-bold text-primary-600">B</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Budgix</h1>
        <p class="text-primary-100 mt-1">Gérez votre budget simplement</p>
      </div>

      <div class="card">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Connexion</h2>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" class="input" placeholder="you@example.com" required />
          </div>
          <div>
            <label class="label">Mot de passe</label>
            <input v-model="form.password" type="password" class="input" placeholder="••••••••" required />
          </div>

          <div v-if="error" class="rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">
            {{ error }}
          </div>

          <button type="submit" class="btn-primary w-full justify-center" :disabled="auth.loading">
            <span v-if="auth.loading">Connexion...</span>
            <span v-else>Se connecter</span>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-4">
          Pas encore de compte ?
          <router-link to="/register" class="text-primary-600 font-medium hover:underline">S'inscrire</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = ref({ email: '', password: '' })
const error = ref(null)

async function handleLogin() {
  error.value = null
  try {
    await auth.login(form.value.email, form.value.password)
    router.push(route.query.redirect || '/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Identifiants incorrects'
  }
}
</script>
