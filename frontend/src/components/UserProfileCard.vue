<template>
  <div class="bg-white rounded-xl shadow p-6 mb-6">
    <div class="flex items-start gap-6">
      <div class="relative flex-shrink-0 cursor-pointer" @click="$emit('edit-avatar')">
        <div class="w-20 h-20 rounded-full bg-gray-300 flex items-center justify-center overflow-hidden">
          <img
            v-if="profile.profilna_slika_url"
            :src="`http://localhost:8000${profile.profilna_slika_url}`"
            class="w-full h-full object-cover"/>
          <span v-else class="text-white text-2xl font-bold">{{ initials }}</span>
        </div>
        <div class="absolute bottom-0 right-0 bg-primary rounded-full w-6 h-6 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
      </div>
       <div class="flex-1">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ profile.full_name }}</h1>
            <p class="text-gray-500 text-sm mt-1">{{ profile.role }}</p>
          </div>
          
        </div>
         <div class="grid grid-cols-2 gap-3 mt-4 text-sm text-gray-600">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
            </svg>
            <span>{{ profile.email }}</span>
          </div>
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            <span>Član od {{ formattedDate }}</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
})
defineEmits(['edit-avatar'])

const initials = computed(() => {
  if (!props.profile?.full_name) return '?'
  return props.profile.full_name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
})
const formattedDate = computed(() => {
  if (!props.profile?.created_at) return ''
  return new Date(props.profile.created_at).toLocaleDateString('bs-BA', {
    month: 'long',
    year: 'numeric'
  })
})
</script>
