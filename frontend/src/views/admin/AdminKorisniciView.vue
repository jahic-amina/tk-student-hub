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
              <button
                @click="toggleUserStatus(user)"
                :class="user.is_active ? 'bg-green-100 text-green-700 hover:bg-green-200 cursor-pointer' : 'bg-gray-100 text-gray-500 hover:bg-gray-200 cursor-pointer'"
                class="px-3 py-1 rounded-full text-xs font-medium transition-colors"
                title="Klikni za promjenu statusa"
              >
                {{ user.is_active ? 'Aktivan' : 'Deaktiviran' }}
              </button>
            </td>
            <td class="px-6 py-4 text-sm text-gray-700">
              {{ roleLabel(user.role) }}
            </td>
            <td class="px-6 py-4 text-right text-sm">
              <button 
                @click="openDeleteModal(user)" 
                class="text-red-600 hover:text-red-800 font-semibold cursor-pointer transition-colors"
              >
                OBRIŠI
              </button>
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

    <div v-if="isDeleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 overflow-y-auto px-4">
      <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-xl border border-gray-100">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Trajno brisanje korisnika</h3>
        
        <p class="text-sm text-gray-500 mb-4">
          Da li ste sigurni da želite trajno obrisati korisnika 
          <strong class="text-gray-800">{{ userToDelete?.full_name }}</strong> ({{ userToDelete?.email }})? 
          Ova akcija je nepovratna.
        </p>
        
        <p class="text-xs font-medium text-gray-700 mb-2 uppercase tracking-wider">
          Upišite riječ <span class="text-red-600 font-bold">OBRIŠI</span> za potvrdu:
        </p>
        
        <input 
          v-model="deleteConfirmationInput"
          type="text" 
          placeholder="OBRIŠI" 
          class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm font-mono focus:outline-none focus:ring-2 focus:ring-red-500/30 mb-5"
        />
        
        <div class="flex justify-end gap-3">
          <button 
            @click="closeDeleteModal" 
            class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors cursor-pointer"
          >
            Odustani
          </button>
          <button 
            @click="confirmDeleteUser" 
            :disabled="deleteConfirmationInput !== 'OBRIŠI'"
            :class="deleteConfirmationInput === 'OBRIŠI' 
              ? 'bg-red-600 hover:bg-red-700 text-white cursor-pointer shadow-sm shadow-red-500/20' 
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          >
            Potvrdi brisanje
          </button>
        </div>
      </div>
    </div>

    <div v-if="showErrorModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 overflow-y-auto px-4">
      <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-xl border border-red-100">
        <h3 class="text-lg font-semibold text-red-600 mb-2">⚠️ Akcija nije dozvoljena</h3>
        
        <p class="text-sm text-gray-600 mb-6">
          {{ errorMessage }}
        </p>
        
        <div class="flex justify-end">
          <button 
            @click="closeErrorModal" 
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors cursor-pointer"
          >
            Razumijem
          </button>
        </div>
      </div>
    </div>


  </div>
</template>


<script>
import { getAllUsers, activateUser, deactivateUser, deleteUser, getMyProfile } from '../../services/api.js'

// ERROR PORUKE - CENTRALIZOVANE
const ERROR_MESSAGES = {
  CANNOT_DEACTIVATE_SELF: 'Ne možete deaktivirati svoj profil. Molimo kontaktirajte drugog administratora.',
  CANNOT_DELETE_SELF: 'Ne možete obrisati svoj profil. Molimo kontaktirajte drugog administratora.',
  DEACTIVATE_ERROR: 'Došlo je do greške prilikom promjene statusa. Pokušajte ponovo.',
  DELETE_ERROR: 'Došlo je do greške prilikom brisanja korisnika. Pokušajte ponovo.'
}

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
      selectedStatus: '', 
      isDeleteModalOpen: false,
      userToDelete: null,
      deleteConfirmationInput: '',
      showErrorModal: false,
      errorMessage: '',
      currentUserId: null
    }
  },

  mounted() {
    this.loadCurrentUser()
    this.fetchUsers()
  },

  methods: {
    async loadCurrentUser() {
      try {
        const token = localStorage.getItem('token')
        const profile = await getMyProfile(token)
        this.currentUserId = profile?.id
      } catch (error) {
        console.error('Greška pri dohvatanju profila:', error)
      }
    },

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
        this.error = 'Došlo je do greške pri dohvatu korisnika.'
      }

      this.loading = false
    },

    async toggleUserStatus(user) {
      // Provjera da li admin pokušava deaktivirati samog sebe
      if (user.id === this.currentUserId) {
        this.showError(ERROR_MESSAGES.CANNOT_DEACTIVATE_SELF)
        return
      }

      const token = localStorage.getItem('token');
      
      // Pamtimo staro stanje
      const oldIsActive = user.is_active;

      user.is_active = !user.is_active;

      try {
        if (oldIsActive) {
          await deactivateUser(token, user.id, "Deaktivacija od strane administratora");
        } else {
          await activateUser(token, user.id);
        }
      } catch (error) {
        user.is_active = oldIsActive
        this.showError(ERROR_MESSAGES.DEACTIVATE_ERROR)
        console.error(error)
      }
    }, 

    // Metode za upravljanje brisanjem
    openDeleteModal(user) {
      // Provjera da li admin pokušava obrisati samog sebe
      if (user.id === this.currentUserId) {
        this.showError(ERROR_MESSAGES.CANNOT_DELETE_SELF)
        return
      }
      this.userToDelete = user
      this.deleteConfirmationInput = ''
      this.isDeleteModalOpen = true
    },

    closeDeleteModal() {
      this.isDeleteModalOpen = false
      this.userToDelete = null
    },

    closeErrorModal() {
      this.showErrorModal = false
      this.errorMessage = ''
    },

    showError(message) {
      this.errorMessage = message
      this.showErrorModal = true
    },

    async confirmDeleteUser() {
      // Dvostruka provjera za svaki slučaj
      if (this.deleteConfirmationInput !== 'OBRIŠI') return

      const token = localStorage.getItem('token')
      
      try {
        // Poziv API servisa za brisanje
        await deleteUser(token, this.userToDelete.id)
        
        // Lokalno uklanjanje korisnika iz tabele (Optimistic / Instant UX)
        this.users = this.users.filter(u => u.id !== this.userToDelete.id)
        this.total--
        
        // Zatvaranje modala
        this.closeDeleteModal()
      } catch (error) {
        this.showError(ERROR_MESSAGES.DELETE_ERROR)
        console.error(error)
      }
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