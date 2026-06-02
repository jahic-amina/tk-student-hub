<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      
  <h1 class="text-2xl font-bold text-primary mb-2">Prijava</h1>
  <p class="text-gray-500 mb-6">Dobrodošli nazad!</p>

      <div v-if="error" class="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-4 text-sm">
        {{ error }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="tvoj@email.com"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Lozinka</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
          />
        </div>

        <button
          @click="handleLogin"
          :disabled="loading"
    class="bg-primary text-white py-2 rounded-lg hover:bg-primary/90 transition font-medium disabled:opacity-50"
        >
          {{ loading ? 'Prijava...' : 'Prijavi se' }}
        </button>
      </div>

      <p class="text-center text-sm text-gray-500 mt-6">
        Nemaš račun?
        <router-link to="/register" class="text-primary font-medium hover:underline">Registruj se</router-link>
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
        // 1. Pozivamo backend za login
        const response = await loginUser(this.email, this.password)

        // 2. Ako nam je backend dao token, lozinka je tačna
        if (response && response.access_token) {
          
          localStorage.setItem('token', response.access_token)
          
          // 3. Pokušavamo dohvatiti tvoje podatke
          const user = await getMe(response.access_token)
          
          // --- KLJUČNI DIO: Provjeravamo da li je backend vratio 'detail' (grešku) ---
          if ((user && user.detail) || (user && user.is_active === false)) {
             // Znači da je backend blokirao pristup (403) i vratio poruku o deaktivaciji!
             localStorage.removeItem('token') // Odmah brišemo token
             this.error = 'Vaš nalog je deaktiviran. Molimo obratite se administratoru.'
             this.loading = false
             return // OVDJE PREKIDAMO SVE, nema prelaska na Dashboard!
          }
          // ---------------------------------------------------------------------------

          // Ako nema greške, snimi korisnika i prebaci ga na dashboard
          if (user && user.full_name) {
             localStorage.setItem('username', user.full_name)
             localStorage.setItem('role', user.role)
          }
          
          window.dispatchEvent(new Event('user-login'))
          this.$router.push('/dashboard')
          
        } else {
          // Ako odmah u startu nema tokena (pogrešna lozinka)
          // `fetch` vraća grešku kao 'detail'
          this.error = response.detail || 'Pogrešan email ili lozinka.'
        }

      } catch (err) {
        // Kod fetch-a, ovo hvata samo situacije kad padne server ili nema interneta
        this.error = 'Došlo je do greške. Provjerite konekciju i pokušajte ponovo.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>