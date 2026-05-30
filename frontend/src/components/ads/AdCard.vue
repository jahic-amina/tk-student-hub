<template>
  <div class="bg-white border border-gray-100 rounded-2xl p-4 sm:p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition duration-200 h-full">
    <div>
      <div class="flex gap-1.5 mb-4 text-[10px] sm:text-xs font-semibold flex-wrap">
        <span :class="getTypeClass(ad.typeLabel)">{{ ad.typeLabel }}</span>
        <span :class="getStatusClass(ad.statusLabel)">{{ ad.statusLabel }}</span>
      </div>

      <h3 class="text-sm sm:text-base font-bold text-gray-900 mb-1 leading-snug line-clamp-2">
        <router-link
          :to="{ name: 'ad-detail', params: { id: ad.id } }"
          class="hover:text-orange-500 transition-colors cursor-pointer"
        >
          {{ ad.title }}
        </router-link>
      </h3>

      <p class="text-gray-400 text-xs sm:text-sm mb-3 font-medium">{{ ad.company }}</p>

      <div class="flex flex-wrap gap-x-3 gap-y-1.5 text-gray-500 text-[11px] sm:text-xs font-medium mb-4">
        <span class="whitespace-nowrap">📍 {{ ad.location }}</span>
        <span v-if="ad.duration" class="whitespace-nowrap">🕒 {{ ad.duration }}</span>
        <span v-if="ad.compensation" class="bg-gray-50 px-1.5 py-0.5 rounded text-gray-600 font-semibold text-[10px] sm:text-xs">
          {{ ad.compensation }}
        </span>
      </div>
    </div>

    <div class="flex flex-wrap gap-1.5 mt-auto pt-2 border-t border-gray-50">
      <span
        v-for="tag in ad.tags"
        :key="tag"
        class="bg-gray-100 text-gray-600 text-[10px] sm:text-xs px-2.5 py-1 rounded-md font-semibold tracking-wide"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script>
const BASE_BADGE = 'px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-md'

export default {
  name: 'AdCard',
  props: {
    ad: {
      type: Object,
      required: true
    }
  },
  methods: {
    getTypeClass(typeLabel) {
      if (typeLabel === 'Praksa') return `bg-blue-50 text-blue-600 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 text-indigo-600 ${BASE_BADGE}`
      return `bg-amber-50 text-amber-600 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 text-green-600 ${BASE_BADGE}`
      if (statusLabel === 'Uskoro ističe') return `bg-orange-50 text-orange-600 ${BASE_BADGE}`
      return `bg-red-50 text-red-600 ${BASE_BADGE}`
    }
  }
}
</script>