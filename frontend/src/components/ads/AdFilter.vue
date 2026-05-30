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
      <select
        :value="selectedField"
        @change="$emit('update:selectedField', $event.target.value)"
        class="w-full sm:w-auto px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-medium text-gray-700 focus:outline-none cursor-pointer text-xs sm:text-sm"
      >
        <option value="">Oblast</option>
        <option v-for="field in fields" :key="field" :value="field">
          {{ field }}
        </option>
      </select>

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
  }
}
</script>