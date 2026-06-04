<template>
  <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col lg:flex-row gap-4 items-stretch lg:items-center justify-between mb-6">
    <div class="flex-1">
      <input
        type="text"
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        placeholder="⌕  Pretraga po nazivu, kompaniji..."
        class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-orange-400"
      />
    </div>

    <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2.5 text-sm items-center">
      <div class="relative w-full sm:w-auto">
        <button
          type="button"
          @click="isFieldOpen = !isFieldOpen"
          class="w-full sm:w-auto min-w-[180px] px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none text-xs sm:text-sm flex items-center justify-between gap-3"
        >
          <span class="truncate">{{ selectedField || 'Oblast' }}</span>
          <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="isFieldOpen ? 'rotate-180' : ''" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.168l3.71-3.938a.75.75 0 1 1 1.08 1.04l-4.24 4.5a.75.75 0 0 1-1.08 0l-4.24-4.5a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
          </svg>
        </button>

        <div
          v-if="isFieldOpen"
          class="absolute left-0 right-0 mt-2 z-20 bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden"
        >
          <button
            type="button"
            @click="selectField('')"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 text-gray-700"
          >
            Sve oblasti
          </button>
          <button
            v-for="field in fields"
            :key="field"
            type="button"
            @click="selectField(field)"
            class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center justify-between gap-3"
            :class="selectedField === field ? 'bg-orange-50 text-orange-600 font-medium' : 'text-gray-700'"
          >
            <span class="truncate">{{ field }}</span>
            <span v-if="selectedField === field" class="text-orange-500">✓</span>
          </button>
        </div>
      </div>

      <div class="col-span-2 sm:col-span-1 flex items-center justify-between sm:justify-start gap-3 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
        <span class="text-gray-700 font-medium text-xs sm:text-sm">Plaćeno</span>
        <button
          @click="$emit('update:isPaid', !isPaid)"
          :class="['relative inline-flex h-5 w-10 items-center rounded-full transition-colors duration-200 focus:outline-none', isPaid ? 'bg-orange-500' : 'bg-gray-300']"
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