<template>
  <footer class="footer">
    <p>© 2026 TK Student Hub. Sva prava zadržana.</p>
    <div v-if="!isCompanyLoggedIn" class="company-links">
      <span class="label">Ste kompanija?</span>
      <router-link to="/company/login">Prijava kompanije</router-link>
      <router-link to="/company/register">Registracija kompanija</router-link>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  computed: {
    isCompanyLoggedIn() {
      this.$route;
      return !!localStorage.getItem('company_token')
    }
  }
}
</script>

<style scoped>
.footer {
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
  border-top: 2px solid #f0f0f0;
  color: #888;
  font-size: 0.9rem;
}

.company-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.75rem;
  font-size: 0.85rem;
}

.company-links .label {
  color: #aaa;
}

.company-links a {
  color: var(--color-primary, #6366f1);
  text-decoration: none;
  transition: opacity 0.2s;
}

.company-links a:hover {
  opacity: 0.75;
}
</style>