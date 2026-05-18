<template>
  <div class="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition duration-200">
    <div>
      <div class="flex gap-2 mb-4 text-xs font-semibold flex-wrap">
        <span :class="getTipKlasa(oglas.tip)">{{ oglas.tip }}</span>
        <span :class="getStatusKlasa(oglas.status)">{{ oglas.status }}</span>
      </div>
      <h3 class="text-base font-bold text-gray-900 mb-1 leading-snug">{{ oglas.naslov }}</h3>
      <p class="text-gray-400 text-sm mb-3 font-medium">{{ oglas.kompanija }}</p>
      <div class="flex flex-wrap gap-x-4 gap-y-1 text-gray-500 text-xs font-medium mb-4">
        <span>📍 {{ oglas.lokacija }}</span>
        <span v-if="oglas.trajanje">🕒 {{ oglas.trajanje }}</span>
        <span v-if="oglas.dodatno">{{ oglas.dodatno }}</span>
      </div>
    </div>
    <div class="flex flex-wrap gap-2 mt-auto pt-2">
      <span
        v-for="tag in oglas.tagovi"
        :key="tag"
        class="bg-gray-100 text-gray-600 text-xs px-3 py-1 rounded-md font-semibold tracking-wide"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OglasCard',
  props: {
    oglas: {
      type: Object,
      required: true
    }
  },
  methods: {
    getTipKlasa(tip) {
      if (tip === 'Praksa') return 'bg-blue-50 text-blue-600 px-2.5 py-1 rounded-md'
      if (tip === 'Edukacija') return 'bg-indigo-50 text-indigo-600 px-2.5 py-1 rounded-md'
      return 'bg-amber-50 text-amber-600 px-2.5 py-1 rounded-md'
    },
    getStatusKlasa(status) {
      if (status === 'Aktivan') return 'bg-green-50 text-green-600 px-2.5 py-1 rounded-md'
      if (status === 'Uskoro ističe') return 'bg-orange-50 text-orange-600 px-2.5 py-1 rounded-md'
      return 'bg-red-50 text-red-600 px-2.5 py-1 rounded-md'
    }
  }
}
</script>