<template>
  <div class="max-w-6xl mx-auto px-6 py-8">

    <div class="mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">Upravljanje korisnicima</h1>
      <p class="text-sm text-primary mt-1">Pregled i upravljanje svim korisnicima sistema</p>
    </div>

    <div class="flex flex-col sm:flex-row gap-3 mb-6">

      <div class="relative flex-1">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
          </svg>
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Pretraži po imenu ili email adresi..."
          class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
          @input="fetchUsers"
        />
      </div>
      <select
        v-model="selectedRole"
        class="border border-gray-200 rounded-lg px-4 py-2 text-sm text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary/30"
        @change="fetchUsers"
      >
        <option value="">Uloga</option>
        <option value="member">Student</option>
        <option value="mentor">Mentor</option>
        <option value="admin">Administrator</option>
      </select>

      <select
        v-model="selectedStatus"
        class="border border-gray-200 rounded-lg px-4 py-2 text-sm text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary/30"
        @change="fetchUsers"
      >
        <option value="">Status</option>
        <option value="true">Aktivan</option>
        <option value="false">Deaktiviran</option>
      </select>

    </div>

    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">

      <div v-if="loading" class="py-12 text-center text-gray-400 text-sm">
        Ucitavanje korisnika...
      </div>

      <div v-else-if="error" class="py-12 text-center text-red-400 text-sm">
        {{ error }}
      </div>

      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100">
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              Ime
            </th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              Email
            </th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              Status
            </th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              Uloga
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="user in users"
            :key="user.id"
            class="border-b border-gray-50 hover:bg-gray-50 transition"
          >
            <td class="px-6 py-4 text-sm font-medium text-gray-800">
              {{ user.full_name }}
            </td>
            <td class="px-6 py-4 text-sm text-primary">
              {{ user.email }}
            </td>
            <td class="px-6 py-4">
              <span
                :class="user.is_active
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-500'"
                class="px-3 py-1 rounded-full text-xs font-medium"
              >
                {{ user.is_active ? 'Aktivan' : 'Deaktiviran' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-700">
              {{ roleLabel(user.role) }}
            </td>
          </tr>

          <tr v-if="users.length === 0">
            <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-400">
              Nema korisnika koji odgovaraju pretrazi.
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !error" class="px-6 py-3 border-t border-gray-50">
        <p class="text-sm text-primary">
          Prikazano {{ users.length }} od {{ total }} korisnika
        </p>
      </div>

    </div>
  </div>
</template>
<script>
import { getAllUsers } from '../../services/api.js'

export default {
  name: 'AdminKorisniciView',

  data() {
    return {
      users: [],         
      total: 0,          
      loading: false,     
      error: null,        
      searchQuery: '',    
      selectedRole: '',   
      selectedStatus: '' 
    }
  },

  mounted() {
    this.fetchUsers()
  },

  methods: {
    async fetchUsers() {
      this.loading = true
      this.error = null

      const token = localStorage.getItem('token')

      const filters = {
        search: this.searchQuery,
        role: this.selectedRole,
        is_active: this.selectedStatus
      }

      const data = await getAllUsers(token, filters)

      if (data && data.users) {
        this.users = data.users
        this.total = data.total
      } else {
        this.error = 'Doslo je do greske pri dohvatu korisnika.'
      }

      this.loading = false
    },

    roleLabel(role) {
      const labels = {
        member: 'Student',
        mentor: 'Mentor',
        admin: 'Administrator'
      }
      return labels[role] || role
    }
  }
}
</script>