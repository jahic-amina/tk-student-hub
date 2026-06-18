<template>
  <div class="max-w-6xl mx-auto px-6 py-8 dark:text-gray-100">

    <div class="mb-6">
      <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">Upravljanje korisnicima</h1>
      <p class="text-sm text-primary mt-1">Pregled i upravljanje svim korisnicima sistema</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5 flex flex-col justify-center">
        <span class="text-sm text-gray-500 dark:text-gray-400 font-medium">Ukupan broj registrovanih</span>
        <div class="mt-2 flex items-center gap-2">
          <span v-if="statsLoading" class="text-2xl font-bold text-gray-300 dark:text-gray-600">...</span>
          <span v-else class="text-3xl font-bold text-gray-800 dark:text-white">{{ stats.total_users }}</span>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5 flex flex-col justify-center">
        <span class="text-sm text-gray-500 dark:text-gray-400 font-medium">Trenutno aktivni nalozi</span>
        <div class="mt-2 flex items-center gap-2">
          <span v-if="statsLoading" class="text-2xl font-bold text-gray-300 dark:text-gray-600">...</span>
          <span v-else class="text-3xl font-bold text-green-600 dark:text-green-400">{{ stats.active_users }}</span>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm p-5 flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <span class="text-sm text-gray-500 dark:text-gray-400 font-medium">Nove registracije</span>
          <select 
            v-model="statsPeriod" 
            @change="fetchStats"
            class="text-xs bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 dark:text-white rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary/50 cursor-pointer"
          >
            <option value="day">Danas</option>
            <option value="week">Ove sedmice</option>
            <option value="month">Ovog mjeseca</option>
          </select>
        </div>
        <div class="mt-2 flex items-center gap-2">
          <span v-if="statsLoading" class="text-2xl font-bold text-gray-300 dark:text-gray-600">...</span>
          <span v-else class="text-3xl font-bold text-blue-600 dark:text-blue-400">+{{ stats.new_registrations }}</span>
        </div>
      </div>
    </div>

    <div class="flex flex-col sm:flex-row gap-3 mb-6">
      <div class="relative flex-1">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
          </svg>
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Pretraži po imenu ili email adresi..."
          class="w-full pl-9 pr-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 dark:text-white dark:placeholder-gray-400 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
          @input="fetchUsers"
        />
      </div>
      <select
        v-model="selectedRole"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-4 py-2 text-sm text-gray-600 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30"
        @change="fetchUsers"
      >
        <option value="">Uloga</option>
        <option value="member">Student</option>
        <option value="admin">Administrator</option>
      </select>

      <select
        v-model="selectedStatus"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg px-4 py-2 text-sm text-gray-600 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30"
        @change="fetchUsers"
      >
        <option value="">Status</option>
        <option value="true">Aktivan</option>
        <option value="false">Deaktiviran</option>
      </select>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden">

      <div v-if="loading" class="py-12 text-center text-gray-400 dark:text-gray-500 text-sm">
        Učitavanje korisnika...
      </div>

      <div v-else-if="error" class="py-12 text-center text-red-400 dark:text-red-500 text-sm">
        {{ error }}
      </div>

      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100 dark:border-gray-700">
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">Ime</th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">Email</th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">Status</th>
            <th class="text-left px-6 py-3 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">Uloga</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="user in users"
            :key="user.id"
            class="border-b border-gray-50 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition"
          >
            <td class="px-6 py-4 text-sm font-medium text-gray-800 dark:text-gray-200">
              {{ user.full_name }}
            </td>
            <td class="px-6 py-4 text-sm text-primary">
              {{ user.email }}
            </td>
            <td class="px-6 py-4">
              <button
                @click="toggleUserStatus(user)"
                :class="user.is_active ? 'bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-400 dark:hover:bg-green-900/50 cursor-pointer' : 'bg-gray-100 text-gray-500 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-400 dark:hover:bg-gray-600 cursor-pointer'"
                class="px-3 py-1 rounded-full text-xs font-medium transition-colors"
                title="Klikni za promjenu statusa"
              >
                {{ user.is_active ? 'Aktivan' : 'Deaktiviran' }}
              </button>
            </td>
            <td class="px-6 py-4">
              <button
                @click="openRoleModal(user)"
                :class="user.role === 'admin' ? 'bg-purple-100 text-purple-700 hover:bg-purple-200 dark:bg-purple-900/30 dark:text-purple-400 dark:hover:bg-purple-900/50 cursor-pointer' : 'bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50 cursor-pointer'"
                class="px-3 py-1 rounded-full text-xs font-medium transition-colors"
                title="Klikni za promjenu uloge"
              >
                {{ roleLabel(user.role) }}
              </button>
            </td>
            <td class="px-6 py-4 text-right text-sm">
              <button 
                @click="openDeleteModal(user)" 
                class="text-red-600 dark:text-red-500 hover:text-red-800 dark:hover:text-red-400 font-semibold cursor-pointer transition-colors"
              >
                OBRIŠI
              </button>
            </td>
          </tr>

          <tr v-if="users.length === 0">
            <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-400 dark:text-gray-500">
              Nema korisnika koji odgovaraju pretrazi.
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !error" class="px-6 py-3 border-t border-gray-50 dark:border-gray-700">
        <p class="text-sm text-primary">
          Prikazano {{ users.length }} od {{ total }} korisnika
        </p>
      </div>
    </div>

    <div v-if="isDeleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 overflow-y-auto px-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full shadow-xl border border-gray-100 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Trajno brisanje korisnika</h3>
        
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
          Da li ste sigurni da želite trajno obrisati korisnika 
          <strong class="text-gray-800 dark:text-gray-200">{{ userToDelete?.full_name }}</strong> ({{ userToDelete?.email }})? 
          Ova akcija je nepovratna.
        </p>
        
        <p class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 uppercase tracking-wider">
          Upišite riječ <span class="text-red-600 dark:text-red-500 font-bold">OBRIŠI</span> za potvrdu:
        </p>
        
        <input 
          v-model="deleteConfirmationInput"
          type="text" 
          placeholder="OBRIŠI" 
          class="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 dark:text-white rounded-lg text-sm font-mono focus:outline-none focus:ring-2 focus:ring-red-500/30 mb-5"
        />
        
        <div class="flex justify-end gap-3">
          <button 
            @click="closeDeleteModal" 
            class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors cursor-pointer"
          >
            Odustani
          </button>
          <button 
            @click="confirmDeleteUser" 
            :disabled="deleteConfirmationInput !== 'OBRIŠI'"
            :class="deleteConfirmationInput === 'OBRIŠI' 
              ? 'bg-red-600 hover:bg-red-700 text-white cursor-pointer shadow-sm shadow-red-500/20' 
              : 'bg-gray-200 dark:bg-gray-600 text-gray-400 dark:text-gray-500 cursor-not-allowed'"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
          >
            Potvrdi brisanje
          </button>
        </div>
      </div>
    </div>

    <div v-if="showErrorModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 overflow-y-auto px-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full shadow-xl border border-red-100 dark:border-red-900/50">
        <h3 class="text-lg font-semibold text-red-600 dark:text-red-500 mb-2">⚠️ Akcija nije dozvoljena</h3>
        
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
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

    <div v-if="isStatusModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 overflow-y-auto px-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full shadow-xl border border-gray-100 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Potvrda akcije</h3>
    
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Da li ste sigurni da želite <strong class="font-bold text-gray-800 dark:text-gray-200">{{ actionToPerform }}</strong> korisnika 
          <strong class="text-gray-800 dark:text-gray-200">{{ userToToggle?.full_name }}</strong>?
        </p>
    
        <div class="flex justify-end gap-3">
          <button 
            @click="closeStatusModal" 
            class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors cursor-pointer"
          >
            Odustani
          </button>
          <button 
            @click="confirmStatusToggle" 
            :class="actionToPerform === 'aktivirati' ? 'bg-green-600 hover:bg-green-700 text-white' : 'bg-red-600 hover:bg-red-700 text-white'"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-colors shadow-sm cursor-pointer"
          >
            Potvrdi
          </button>
        </div>
      </div>
    </div>

    <div v-if="isRoleModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 dark:bg-black/60 overflow-y-auto px-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full shadow-xl border border-gray-100 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Potvrda promjene uloge</h3>

        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Da li ste sigurni da želite promijeniti ulogu korisnika 
          <strong class="text-gray-800 dark:text-gray-200">{{ userToChangeRole?.full_name }}</strong> 
          iz <strong class="text-gray-600 dark:text-gray-400">{{ roleLabel(userToChangeRole?.role) }}</strong> 
          u <strong class="text-primary font-bold">{{ roleLabel(targetRole) }}</strong>?
        </p>

        <div class="flex justify-end gap-3">
          <button 
            @click="closeRoleModal" 
            class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors cursor-pointer"
          >
            Odustani
          </button>
          <button 
            @click="confirmRoleChange" 
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors shadow-sm cursor-pointer"
          >
            Potvrdi
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAllUsers, activateUser, deactivateUser, deleteUser, getMyProfile, getPlatformStats, changeUserRole } from '../../services/api.js'

// ERROR PORUKE - CENTRALIZOVANE
const ERROR_MESSAGES = {
  CANNOT_DEACTIVATE_SELF: 'Ne možete ovdje deaktivirati svoj profil. Molimo da to uradite u dijelu uredi profil.',
  CANNOT_DELETE_SELF: 'Ne možete obrisati svoj profil. Molimo kontaktirajte drugog administratora.',
  CANNOT_CHANGE_ROLE_SELF: 'Ne možete sami sebi promijeniti ulogu.',
  DEACTIVATE_ERROR: 'Došlo je do greške prilikom promjene statusa. Pokušajte ponovo.',
  DELETE_ERROR: 'Došlo je do greške prilikom brisanja korisnika. Pokušajte ponovo.',
  ROLE_ERROR: 'Došlo je do greške prilikom promjene uloge. Pokušajte ponovo.'
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
      isStatusModalOpen: false,
      userToToggle: null,
      actionToPerform: '',
      showErrorModal: false,
      errorMessage: '',
      currentUserId: null,
      stats: {
        total_users: 0,
        active_users: 0,
        new_registrations: 0
      },
      statsPeriod: 'month',
      statsLoading: false,
      isRoleModalOpen: false,    
      userToChangeRole: null,     
      targetRole: '',
    
    }
  },

  mounted() {
    this.loadCurrentUser()
    this.fetchUsers()
    this.fetchStats()
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

    toggleUserStatus(user) {
      // Provjera da li admin pokušava deaktivirati samog sebe
      if (user.id === this.currentUserId) {
        this.showError(ERROR_MESSAGES.CANNOT_DEACTIVATE_SELF)
        return
      }

      this.openStatusModal(user)
    },
    async confirmStatusToggle() {
        if (!this.userToToggle) return

        const user = this.userToToggle
        const token = localStorage.getItem('token')
        const oldIsActive = user.is_active

        user.is_active = !user.is_active
        this.closeStatusModal()

        try {
          if (oldIsActive) {
            await deactivateUser(token, user.id, "Deaktivacija od strane administratora")
          } else {
            await activateUser(token, user.id)
          }
        } catch (error) {
          user.is_active = oldIsActive
          this.showError(ERROR_MESSAGES.DEACTIVATE_ERROR)
          console.error(error)
        }
      },

    // METODA ZA STATISTIKU
      async fetchStats() {
        this.statsLoading = true
        try {
          const token = localStorage.getItem('token')
          const data = await getPlatformStats(token, this.statsPeriod)
        
          if (data) {
            this.stats = data
          }
        } catch (error) {
          console.error('Greška pri dohvatanju statistike:', error)
        } finally {
          this.statsLoading = false
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
        if (this.deleteConfirmationInput !== 'OBRIŠI') return

        const token = localStorage.getItem('token')
      
        try {
        // Poziv API servisa za brisanje
          await deleteUser(token, this.userToDelete.id)
        
          this.users = this.users.filter(u => u.id !== this.userToDelete.id)
          this.total--
          this.closeDeleteModal()
        } catch (error) {
          this.showError(ERROR_MESSAGES.DELETE_ERROR)
          console.error(error)
        }
      },

      openStatusModal(user) {
        this.userToToggle = user;
        this.actionToPerform = user.is_active ? 'deaktivirati' : 'aktivirati';
        this.isStatusModalOpen = true;
      },

      closeStatusModal() {
        this.isStatusModalOpen = false;
        this.userToToggle = null;
        this.actionToPerform = '';
      },

      async confirmStatusToggle() {
        if (!this.userToToggle) return;
        const user = this.userToToggle;
  
  // Provjera da li admin pokušava deaktivirati samog sebe
        if (user.id === this.currentUserId) {
          this.closeStatusModal(); 
          this.showError(ERROR_MESSAGES.CANNOT_DEACTIVATE_SELF);
          return;
        }

        const token = localStorage.getItem('token');
        const oldIsActive = user.is_active;

        user.is_active = !user.is_active;
        this.closeStatusModal(); 

        try {
          if (oldIsActive) {
            await deactivateUser(token, user.id, "Deaktivacija od strane administratora");
          } else {
            await activateUser(token, user.id);
          }
          this.fetchStats();
        } catch (error) {
          user.is_active = oldIsActive; 
          this.showError(ERROR_MESSAGES.DEACTIVATE_ERROR);
          console.error(error);
        }
      },
      openRoleModal(user) {
        if (user.id === this.currentUserId) {
          this.showError(ERROR_MESSAGES.CANNOT_CHANGE_ROLE_SELF)
          return
        }

        this.userToChangeRole = user
        this.targetRole = user.role === 'admin' ? 'member' : 'admin'
        this.isRoleModalOpen = true
      },

      closeRoleModal() {
        this.isRoleModalOpen = false
        this.userToChangeRole = null
        this.targetRole = ''
      },

      async confirmRoleChange() {
        if (!this.userToChangeRole) return

        const user = this.userToChangeRole
        const token = localStorage.getItem('token')
        const oldRole = user.role
        const newRole = user.role === 'admin' ? 'member' : 'admin'

        user.role = newRole
        this.closeRoleModal()

        try {
          await changeUserRole(token, user.id, { role: newRole })
        } catch (error) {
   
          user.role = oldRole
          this.showError(ERROR_MESSAGES.ROLE_ERROR)
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