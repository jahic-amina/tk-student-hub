<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">

  <h1 class="text-2xl font-bold text-primary mb-2">Registracija</h1>
  <p class="text-gray-500 mb-6">Kreiraj račun na TK Student Hub</p>

      <div v-if="error" class="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-4 text-sm">
        {{ error }}
      </div>

      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ime i prezime</label>
          <input
            v-model="fullName"
            type="text"
            placeholder="Ime Prezime"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
          />
        </div>

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
          @click="handleRegister"
          :disabled="loading"
            class="bg-primary text-white py-2 rounded-lg hover:bg-primary/90 transition font-medium disabled:opacity-50"
        >
          {{ loading ? 'Registracija...' : 'Registruj se' }}
        </button>
      </div>

      <p class="text-center text-sm text-gray-500 mt-6">
        Već imaš račun?
        <router-link to="/login" class="text-primary font-medium hover:underline">Prijavi se</router-link>
      </p>

    </div>
  </div>
</template>

<script>
import { registerUser, getMe } from '../services/api'

export default {
  name: 'RegisterView',
  data() {
    return {
      fullName: '',
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.error = null

      const response = await registerUser(this.email, this.fullName, this.password)

      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        const user = await getMe(response.access_token)
        localStorage.setItem('username', user.full_name)
        window.location.href = '/'
      } else {
        this.error = response.detail || 'Greška pri registraciji.'
      }

      this.loading = false
    }
  }
}
</script>