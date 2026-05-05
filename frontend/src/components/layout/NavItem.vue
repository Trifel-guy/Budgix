<template>
  <router-link
    :to="to"
    :class="[
      'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
      isActive
        ? 'bg-primary-50 text-primary-700'
        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
    ]"
  >
    <span class="text-base">{{ iconMap[icon] }}</span>
    <slot />
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({ to: String, icon: String })
const route = useRoute()
const isActive = computed(() => route.path.startsWith(props.to))

const iconMap = {
  home: '🏠', list: '📋', chart: '📊', tag: '🏷️',
  upload: '📤', shield: '🛡️', users: '👥',
}
</script>
