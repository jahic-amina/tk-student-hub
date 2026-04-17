<template>
  <nav class="bg-white border-b border-gray-100 shadow-sm">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      
      <router-link to="/" class="text-xl font-bold text-primary">
        TK Student Hub
      </router-link>

      <div class="flex gap-6">
      <router-link to="/prakse-i-edukacije" class="text-gray-600 hover:text-primary font-medium transition">Prakse i edukacije</router-link>
      <router-link to="/mentoring" class="text-gray-600 hover:text-primary font-medium transition">Materijali</router-link>
      <router-link to="/forum" class="text-gray-600 hover:text-primary font-medium transition">Forum</router-link>
      <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium transition">Profili</router-link>
        </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <router-link to="/profiles" class="text-gray-600 hover:text-primary font-medium">{{ username }}</router-link>
          <button @click="logout" class="border border-primary text-primary px-4 py-1.5 rounded-lg hover:bg-primary hover:text-white transition">
            Odjava
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-gray-600 hover:text-primary font-medium">Prijava</router-link>
          <router-link to="/register" class="bg-primary text-white px-4 py-1.5 rounded-lg hover:bg-primary/90 transition">
            Registracija
          </router-link>
        </template>
      </div>

    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    username() {
      return localStorage.getItem('username') || 'Profil'
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      this.$router.push('/login')
    }
  }
}
</script>