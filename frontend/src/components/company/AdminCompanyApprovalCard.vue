<template>
  <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4">
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

    <div class="flex gap-2 mt-auto">
      <button
        v-if="!company.is_deleted"
        @click="$emit('delete', company)"
        :disabled="company.updating"
        class="flex-1 py-2 rounded-lg bg-gray-100 text-gray-700 text-xs font-semibold hover:bg-gray-200 transition disabled:opacity-50"
      >
        {{ company.updating === 'deleting' ? 'Brisanje...' : 'Obriši' }}
      </button>
      <button
        v-else
        @click="$emit('restore', company)"
        :disabled="company.updating"
        class="flex-1 py-2 rounded-lg bg-blue-50 text-blue-700 text-xs font-semibold hover:bg-blue-100 transition disabled:opacity-50"
      >
        {{ company.updating === 'restoring' ? 'Vraćanje...' : 'Vrati' }}
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