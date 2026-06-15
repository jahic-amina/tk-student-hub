<template>
  <div class="activity-feed">
    <div v-if="loading" class="flex flex-col gap-4">
      <div
        v-for="n in 3"
        :key="n"
        class="flex items-start gap-3 animate-pulse"
      >
        <div class="w-10 h-10 rounded-full bg-gray-200 shrink-0"></div>
        <div class="flex flex-col gap-2 flex-1">
          <div class="h-3 bg-gray-200 rounded w-1/3"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
          <div class="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-col gap-4">
        <p v-if ="activities.length === 0" class="text-gray-400 text-sm">Nema nedavne aktivnosti</p>
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="flex items-start gap-3"
      >
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
          :class="iconBg(activity.activity_type)"
        >
          <component :is="iconComponent(activity.activity_type)" class="w-5 h-5" :class="iconColor(activity.activity_type)" />
        </div>

        <div class="flex flex-col">
          <span class="text-sm" :class="typeLabel(activity.activity_type).color">
            {{ typeLabel(activity.activity_type).text }}
          </span>
          <span class="font-medium text-gray-900">{{ activity.title }}</span>
          <span class="text-sm text-gray-500">
            {{ activity.subtitle }} · {{ formatRelativeTime(activity.created_at) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DocumentTextIcon, ChatBubbleLeftIcon, CheckCircleIcon, ArrowUpTrayIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  activities: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

function iconComponent(type) {
  const map = {
    material_posted: DocumentTextIcon,
    material_uploaded: ArrowUpTrayIcon,
    forum_comment: ChatBubbleLeftIcon,
    forum_answer: ChatBubbleLeftIcon,
    internship_completed: CheckCircleIcon
  }
  return map[type] || DocumentTextIcon
}

function iconBg(type) {
  const map = {
    material_posted: 'bg-blue-100',
    material_uploaded: 'bg-purple-100',
    forum_comment: 'bg-green-100',
    forum_answer: 'bg-green-100',
    internship_completed: 'bg-orange-100'
  }
  return map[type] || 'bg-gray-100'
}

function iconColor(type) {
  const map = {
    material_posted: 'text-blue-600',
    material_uploaded: 'text-purple-600',
    forum_comment: 'text-green-600',
    forum_answer: 'text-green-600',
    internship_completed: 'text-orange-500'
  }
  return map[type] || 'text-gray-500'
}

function typeLabel(type) {
  const map = {
    material_posted: { text: 'Postavio novi materijal', color: 'text-blue-500' },
    material_uploaded: { text: 'Uploadovao materijal', color: 'text-purple-500' },
    forum_comment: { text: 'Komentarisao na forumu', color: 'text-green-500' },
    forum_answer: { text: 'Odgovorio na pitanje', color: 'text-green-500' },
    internship_completed: { text: 'Završio praksu', color: 'text-orange-500' }
  }
  return map[type] || { text: 'Aktivnost', color: 'text-gray-500' }
}

function formatRelativeTime(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 60) return `Pre ${diffMins} minuta`
  if (diffHours < 24) return `Pre ${diffHours} sata`
  return `Pre ${diffDays} dana`
}
</script>