<template>
  <div class="card">
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm font-medium text-gray-500">{{ label }}</span>
      <span class="text-2xl">{{ icon }}</span>
    </div>
    <p :class="['text-2xl font-bold', colorClass]">{{ formatted }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  value: [Number, String],
  color: { type: String, default: 'primary' },
  icon: String,
  currency: { type: String, default: 'EUR' },
})

const colorClass = computed(() => ({
  emerald: 'text-emerald-600',
  red: 'text-red-600',
  primary: 'text-primary-600',
}[props.color] || 'text-gray-900'))

const formatted = computed(() =>
  new Intl.NumberFormat('fr-FR', { style: 'currency', currency: props.currency }).format(props.value || 0)
)
</script>
