<template>
  <div class="bg-white dark:bg-slate-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between mb-6 transition-colors duration-200">
    <div class="flex-1">
      <input
        type="text"
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        placeholder="⌕  Pretraga po nazivu, kompaniji..."
        class="w-full px-4 py-2.5 bg-gray-50 dark:bg-slate-700/50 border border-gray-200 dark:border-slate-600 rounded-lg text-sm text-gray-900 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-400 focus:outline-none focus:border-orange-400 dark:focus:border-orange-500"
      />
    </div>

    <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2.5 text-sm items-center">
      <div class="relative w-full sm:w-auto">
        <button
          type="button"
          @click="isFieldOpen = !isFieldOpen"
          @keydown.esc.stop.prevent="isFieldOpen = false"
          :aria-expanded="isFieldOpen ? 'true' : 'false'"
          aria-haspopup="listbox"
          class="w-full sm:w-auto min-w-[180px] px-3 py-2 bg-gray-50 dark:bg-slate-700/50 border border-gray-200 dark:border-slate-600 rounded-lg font-medium text-gray-700 dark:text-slate-200 focus:outline-none text-xs sm:text-sm flex items-center justify-between gap-3 hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors"
        >
          <span class="truncate">{{ selectedField || 'Oblast' }}</span>
          <svg class="w-4 h-4 text-gray-400 dark:text-slate-400 transition-transform duration-200" :class="isFieldOpen ? 'rotate-180' : ''" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.168l3.71-3.938a.75.75 0 1 1 1.08 1.04l-4.24 4.5a.75.75 0 0 1-1.08 0l-4.24-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
          </svg>
        </button>

        <div
          v-if="isFieldOpen"
          class="absolute left-0 right-0 mt-2 z-20 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl shadow-lg overflow-hidden"
        >
          <button
            type="button"
            @click="selectField('')"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-slate-300 bg-transparent border-none cursor-pointer"
          >
            Sve oblasti
          </button>
          <button
            v-for="field in fields"
            :key="field"
            type="button"
            @click="selectField(field)"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-slate-700 flex items-center justify-between gap-3 bg-transparent border-none cursor-pointer"
            :class="selectedField === field ? 'bg-orange-50 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 font-medium' : 'text-gray-700 dark:text-slate-300'"
          >
            <span class="truncate">{{ field }}</span>
            <span v-if="selectedField === field" class="text-orange-500 dark:text-orange-400">✓</span>
          </button>
        </div>
      </div>

      <div class="col-span-2 sm:col-span-1 flex items-center justify-between sm:justify-start gap-3 px-3 py-2 bg-gray-50 dark:bg-slate-700/50 border border-gray-200 dark:border-slate-600 rounded-lg">
        <span class="text-gray-700 dark:text-slate-200 font-medium text-xs sm:text-sm">Plaćeno</span>
        <button
          type="button"
          @click="$emit('update:isPaid', !isPaid)"
          :class="['relative inline-flex h-5 w-10 items-center rounded-full transition-colors duration-200 focus:outline-none border-none cursor-pointer', isPaid ? 'bg-orange-500' : 'bg-gray-300 dark:bg-slate-600']"
        >
          <span :class="['inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform duration-200', isPaid ? 'translate-x-5' : 'translate-x-0.5']"></span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdFilter',
  props: {
    searchQuery: String,
    isPaid: Boolean,
    selectedField: String,
    fields: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isFieldOpen: false
    }
  },
  methods: {
    selectField(field) {
      this.$emit('update:selectedField', field)
      this.isFieldOpen = false
    }
  }
}
</script>