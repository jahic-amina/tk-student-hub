<template>
  <div class="relative bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4">
    <div class="flex items-start justify-between gap-2">
      <div>
        <h2 class="text-base font-bold text-gray-900">{{ company.company_name }}</h2>
        <p class="text-xs text-gray-400 mt-0.5">{{ company.email }}</p>
      </div>
      <span v-if="company.is_deleted" class="text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap bg-gray-100 text-gray-700">
        Obrisano
      </span>
      <span v-else :class="statusBadgeClass(company.status)">
        {{ statusLabel(company.status) }}
      </span>
    </div>

    <div class="text-xs text-gray-500 space-y-1">
      <p><span class="font-semibold text-gray-700">TIN:</span> {{ company.tin }}</p>
      <p><span class="font-semibold text-gray-700">Adresa:</span> {{ company.address }}</p>
      <p>
        <span class="font-semibold text-gray-700">Web:</span>
        <a :href="company.website_url" target="_blank" class="text-orange-500 hover:underline ml-1">
          {{ company.website_url }}
        </a>
      </p>
    </div>

    <p class="text-xs text-gray-500 leading-relaxed line-clamp-3">{{ company.description }}</p>

    <div v-if="!company.is_deleted && company.status === 'pending'" class="flex gap-2 mt-auto">
      <button
        @click="$emit('approve', company)"
        :disabled="company.updating"
        class="flex-1 py-2 rounded-lg bg-green-50 text-green-700 text-xs font-semibold hover:bg-green-100 transition disabled:opacity-50"
      >
        {{ company.updating === 'approved' ? 'Slanje...' : 'Odobri' }}
      </button>
      <button
        @click="$emit('reject', company)"
        :disabled="company.updating"
        class="flex-1 py-2 rounded-lg bg-red-50 text-red-700 text-xs font-semibold hover:bg-red-100 transition disabled:opacity-50"
      >
        {{ company.updating === 'denied' ? 'Slanje...' : 'Odbij' }}
      </button>
    </div>

    <div class="absolute bottom-4 right-4 flex gap-2">
      <button
        v-if="!company.is_deleted"
        @click="$emit('delete', company)"
        :disabled="company.updating"
        class="p-2 rounded-full bg-red-50 text-red-600 hover:bg-red-100 transition disabled:opacity-50"
        :title="company.updating === 'deleting' ? 'Brisanje...' : 'Obriši'"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
      <button
        v-else
        @click="$emit('restore', company)"
        :disabled="company.updating"
        class="p-2 rounded-full bg-green-50 text-green-600 hover:bg-green-100 transition disabled:opacity-50"
        :title="company.updating === 'restoring' ? 'Vraćanje...' : 'Vrati'"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
const STATUS_LABEL = {
  pending: 'Na čekanju',
  approved: 'Odobrena',
  denied: 'Odbijena'
}

export default {
  name: 'AdminCompanyCard',
  props: {
    company: {
      type: Object,
      required: true
    }
  },
  emits: ['approve', 'reject', 'delete', 'restore'],
  methods: {
    statusLabel(status) {
      return STATUS_LABEL[status] || status
    },
    statusBadgeClass(status) {
      const base = 'text-xs font-semibold px-2.5 py-1 rounded-full whitespace-nowrap'
      if (status === 'approved') return `${base} bg-green-50 text-green-700`
      if (status === 'denied') return `${base} bg-red-50 text-red-700`
      return `${base} bg-yellow-50 text-yellow-700`
    }
  }
}
</script>