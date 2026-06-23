<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-slate-900 transition-colors duration-300 px-4">
    
    <div class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-800 p-8 rounded-xl shadow-md w-full max-w-md transition-colors duration-200">

      <h1 class="text-2xl font-bold text-primary dark:text-orange-500 mb-2">Prijava</h1>
      <p class="text-gray-500 dark:text-slate-400 mb-6">Dobrodošli nazad!</p>

      <div v-if="error" class="bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 border border-transparent dark:border-red-900/40 px-4 py-3 rounded-lg mb-4 text-sm font-medium">
        {{ error }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Email</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="tvoj@email.com"
            class="w-full border border-gray-300 dark:border-slate-700 rounded-lg px-4 py-2 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all" 
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Lozinka</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="••••••••"
            class="w-full border border-gray-300 dark:border-slate-700 rounded-lg px-4 py-2 text-slate-800 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-orange-400 transition-all" 
          />
        </div>

        <button 
          @click="handleLogin" 
          :disabled="loading"
          class="bg-primary dark:bg-orange-500 hover:bg-primary/90 dark:hover:bg-orange-400 text-white py-2 rounded-lg transition-colors font-medium disabled:opacity-50 active:scale-[0.99] cursor-pointer border-none shadow-sm"
        >
          {{ loading ? 'Prijava...' : 'Prijavi se' }}
        </button>
      </div>

      <p class="text-center text-sm text-gray-500 dark:text-slate-400 mt-6">
        Nemaš račun?
        <router-link to="/register" class="text-primary dark:text-orange-400 font-medium hover:underline">Registruj se</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { loginUser, getMe } from '../services/api'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = null

      try {
        const response = await loginUser(this.email, this.password)

        if (response && response.access_token) {
          localStorage.setItem('token', response.access_token)
          const user = await getMe(response.access_token)

          if (user && user.full_name) {
            localStorage.setItem('username', user.full_name)
            localStorage.setItem('role', user.role)
            localStorage.setItem('user_id', user.id)
          }

          window.dispatchEvent(new Event('user-login'))
          this.$router.push('/dashboard')
        } else {
          this.error = 'Pogrešan email ili lozinka.'
        }

      } catch (err) {
        const errorMessage = err.message || '';
        let serverPoruka = '';
        try {
          const parsedError = JSON.parse(errorMessage);
          serverPoruka = parsedError.detail || ''; 
        } catch (e) {
          serverPoruka = errorMessage; 
        }

        if (serverPoruka.includes('Not authenticated') || serverPoruka.includes('pogrešan')) {
          this.error = 'Pogrešan email ili lozinka.';
        } else if (serverPoruka.toLowerCase().includes('deaktiviran') || serverPoruka.toLowerCase().includes('inactive')) {
          localStorage.removeItem('token');
          this.error = 'Vaš nalog je deaktiviran. Molimo obratite se administratoru.';
        } else if (serverPoruka) {
          this.error = serverPoruka;
        } else {
          this.error = 'Došlo je do greške. Provjerite konekciju i pokušajte ponovo.';
        }
      } finally {
        this.loading = false
      }
    } 
  }
}
</script>