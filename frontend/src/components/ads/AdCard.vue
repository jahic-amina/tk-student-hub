<template>
  <div class="bg-white border border-gray-100 rounded-2xl p-4 sm:p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition duration-200 h-full relative">
    
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
          isBookmarked ? 'text-orange-500' : 'text-gray-300 hover:text-orange-400'
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

      <h3 class="text-sm sm:text-base font-bold text-gray-900 mb-1 leading-snug line-clamp-2">
        <router-link
          :to="{ name: 'ad-detail', params: { id: ad.id } }"
          class="hover:text-orange-500 transition-colors cursor-pointer"
        >
          {{ ad.title }}
        </router-link>
      </h3>

      <p class="text-gray-400 text-xs sm:text-sm mb-3 font-medium">
        <router-link :to="`/companies/${ad.company_id}`" class="hover:text-orange-500 transition-colors">
          {{ ad.company }}
        </router-link>
      </p>

      <div class="flex flex-wrap gap-x-3 gap-y-1.5 text-gray-500 text-[11px] sm:text-xs font-medium mb-4">
        <span class="whitespace-nowrap">📍 {{ ad.location }}</span>
        <span v-if="ad.duration" class="whitespace-nowrap">🕒 {{ ad.duration }} mjeseca</span>
        <span v-if="ad.spots" class="whitespace-nowrap" :class="ad.applicants_count >= ad.spots ? 'text-red-400' : 'text-gray-500'">
          👥 {{ ad.applicants_count }}/{{ ad.spots }} prijava
        </span>
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
      if (typeLabel === 'Praksa') return `bg-blue-50 text-blue-600 ${BASE_BADGE}`
      if (typeLabel === 'Edukacija') return `bg-indigo-50 text-indigo-600 ${BASE_BADGE}`
      return `bg-amber-50 text-amber-600 ${BASE_BADGE}`
    },
    getStatusClass(statusLabel) {
      if (statusLabel === 'Aktivan') return `bg-green-50 text-green-600 ${BASE_BADGE}`
      if (statusLabel === 'Uskoro ističe') return `bg-orange-50 text-orange-600 ${BASE_BADGE}`
      return `bg-red-50 text-red-600 ${BASE_BADGE}`
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