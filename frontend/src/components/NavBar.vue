<template>
  <nav class="bg-white dark:bg-slate-900 border-b border-gray-100 dark:border-slate-700 shadow-sm transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <router-link to="/" class="text-xl font-bold text-primary dark:text-orange-500">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
        <router-link to="/prakse-i-edukacije" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Prakse i edukacije</router-link>
        <router-link to="/mentoring" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Materijali</router-link>
        <router-link to="/forum" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Forum</router-link>
        <router-link to="/profiles" class="text-gray-600 dark:text-slate-300 hover:text-primary dark:hover:text-orange-400 font-medium transition">Profili</router-link>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <router-link to="/profiles" class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logout" class="border border-primary text-primary dark:border-orange-500 dark:text-orange-500 px-4 py-1.5 rounded-lg hover:bg-primary dark:hover:bg-orange-500 hover:text-white dark:hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 dark:text-slate-300 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
            Registracija
          </router-link>
        </template>
      </div>

      <div class="flex items-center gap-2 border-l border-gray-200 dark:border-slate-700 pl-4 ml-2">
        <span class="text-xs font-semibold text-gray-600 dark:text-gray-300 select-none whitespace-nowrap">
          {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
        </span>
        <button 
          @click="toggleDarkMode"
          class="w-10 h-6 flex items-center bg-gray-300 dark:bg-orange-500 rounded-full p-1 transition-colors duration-300 focus:outline-none flex-shrink-0"
        >
          <div 
            class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
            :class="{ 'translate-x-4': isDarkMode }"
          ></div>
        </button>
      </div>

    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      isDarkMode: localStorage.getItem('theme') === 'dark'
    }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    username() {
      return localStorage.getItem('username') || 'Profil'
    }
  },
  mounted() {
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  }
}
</script>