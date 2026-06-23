<template>
  <div class="min-h-screen bg-transparent dark:bg-slate-900 flex items-center justify-center transition-colors duration-200">
    <div class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-md border border-transparent dark:border-slate-700 w-full max-w-md">

      <h1 class="text-2xl font-bold text-primary mb-2">Prijava kompanije</h1>
      <p class="text-gray-500 dark:text-slate-400 mb-6">Dobrodošli nazad!</p>

      <div v-if="error" class="bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg mb-4 text-sm border border-transparent dark:border-red-900/50">
        {{ error }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Email ili broj telefona</label>
          <input
            v-model="identifier"
            type="text"
            placeholder="info@kompanija.ba"
            class="w-full border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-lg px-4 py-2 text-gray-900 dark:text-slate-100 focus:outline-none focus:border-primary dark:focus:border-primary"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Lozinka</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full border border-gray-300 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-lg px-4 py-2 text-gray-900 dark:text-slate-100 focus:outline-none focus:border-primary dark:focus:border-primary"
          />
        </div>

        <button
          @click="handleLogin"
          :disabled="loading"
          class="bg-primary text-white py-2 rounded-lg hover:bg-primary/90 transition font-medium disabled:opacity-50 border-none cursor-pointer"
        >
          {{ loading ? 'Prijava...' : 'Prijavi se' }}
        </button>
      </div>

      <p class="text-center text-sm text-gray-500 dark:text-slate-400 mt-6">
        Nemate račun?
        <router-link to="/company/register" class="text-primary font-medium hover:underline">Registrujte kompaniju</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { loginCompany } from '../../services/api'

export default {
  name: 'CompanyLoginView',
  data() {
    return {
      identifier: '',
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
        const response = await loginCompany(this.identifier, this.password)

        if (response.access_token) {
          localStorage.setItem('company_token', response.access_token)
          localStorage.setItem('company_name', response.company_name)
          localStorage.setItem('company_id', response.company_id)
          window.location.href = '/'
        } else {
          this.error = 'Pogrešan email ili lozinka.'
        }
      } catch (err) {
        this.error = 'Došlo je do greške. Pokušajte ponovo.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>