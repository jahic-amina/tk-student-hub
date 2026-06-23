<template>
  <div class="bg-white dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-2xl p-4 sm:p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition duration-200 h-full relative">
    
    <button 
      v-if="canBookmark"
      @click.prevent.stop="toggleBookmark" 
      class="absolute top-4 right-4 focus:outline-none transition-transform hover:scale-110 active:scale-95 z-10"
      title="Sačuvaj oglas"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        :fill="isBookmarked ? 'currentColor' : 'none'" 
        viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" 
        :class="[
          'w-6 h-6 sm:w-7 sm:h-7 transition-colors duration-300', 
          isBookmarked ? 'text-orange-500' : 'text-gray-300 dark:text-slate-500 hover:text-orange-400 dark:hover:text-orange-400'
        ]"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
      </svg>
    </button>

    <div>
      <div class="flex gap-1.5 mb-4 text-[10px] sm:text-xs font-semibold flex-wrap pr-10">
        <span :class="getTypeClass(ad.typeLabel)">{{ ad.typeLabel }}</span>
        <span :class="getStatusClass(ad.statusLabel)">{{ ad.statusLabel }}</span>
      </div>

      <h3 class="text-sm sm:text-base font-bold text-gray-900 dark:text-slate-100 mb-1 leading-snug line-clamp-2">
        <router-link
          :to="{ name: 'ad-detail', params: { id: ad.id } }"
          class="hover:text-orange-500 dark:hover:text-orange-400 transition-colors cursor-pointer"
        >
          {{ ad.title }}
        </router-link>
      </h3>

      <p class="text-gray-400 dark:text-slate-400 text-xs sm:text-sm mb-3 font-medium">
        <router-link :to="`/companies/${ad.company_id}`" class="hover:text-orange-500 dark:hover:text-orange-400 transition-colors">
          {{ ad.company }}
        </router-link>
      </p>

      <div class="flex flex-wrap gap-x-3 gap-y-1.5 text-gray-500 dark:text-slate-400 text-[11px] sm:text-xs font-medium mb-4">
        <span class="whitespace-nowrap">📍 {{ ad.location }}</span>
        <span v-if="ad.duration" class="whitespace-nowrap">🕒 {{ ad.duration }} mjeseca</span>
        <span v-if="ad.spots" class="whitespace-nowrap" :class="ad.applicants_count >= ad.spots ? 'text-red-400' : 'text-gray-500 dark:text-slate-400'">
          👥 {{ ad.applicants_count }}/{{ ad.spots }} prijava
        </span>
        <span v-if="ad.compensation" class="bg-gray-50 dark:bg-slate-700 px-1.5 py-0.5 rounded text-gray-600 dark:text-slate-300 font-semibold text-[10px] sm:text-xs">
          {{ ad.compensation }}
        </span>
      </div>
    </div>

    <div class="flex flex-wrap gap-1.5 mt-auto pt-2 border-t border-gray-50 dark:border-slate-700/50">
      <span
        v-for="tag in ad.tags"
        :key="tag"
        class="bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 text-[10px] sm:text-xs px-2.5 py-1 rounded-md font-semibold tracking-wide"
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
    },
    bookmarkId: {
      type: Number,
      default: null
    },
    canBookmark: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isBookmarked() {
      return this.bookmarkId !== null;
    }
  },
  methods: {
    getTypeClass(typeLabel) {
      if (typeLabel === 'Praksa') return `bg-blue-50 text-blue-600 dark:bg-blue-950/40 dark:text-blue-400 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400 ${BASE_BADGE}`
      return `bg-amber-50 text-amber-600 dark:bg-amber-950/40 dark:text-amber-400 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 text-green-600 dark:bg-green-950/40 dark:text-green-400 ${BASE_BADGE}`
      if (statusLabel === 'Uskoro ističe') return `bg-orange-50 text-orange-600 dark:bg-orange-950/40 dark:text-orange-400 ${BASE_BADGE}`
      return `bg-red-50 text-red-600 dark:bg-red-950/40 dark:text-red-400 ${BASE_BADGE}`
    },
    toggleBookmark() {
      this.$emit('toggle-bookmark', {
        adId: this.ad.id,
        bookmarkId: this.bookmarkId
      });
    }
  }
}
</script>