<template>
  <div class="reg-page">
    <div class="reg-header">
      <h1>Registracija kompanije / saradnika</h1>
      <p>Kompanije dobijaju pristup predlaganju praksi i edukacija.</p>
    </div>

    <div class="reg-layout">
      <div class="reg-card">

        <!-- Poruka o uspjehu -->
        <div v-if="submitStatus === 'success'" class="alert alert-success">
          Registracija uspješna! Vaš zahtjev je poslan na odobravanje.
        </div>

        <!-- Poruka o grešci -->
        <div v-if="submitStatus === 'error'" class="alert alert-error">
          {{ serverError }}
        </div>

        <template v-if="submitStatus !== 'success'">
          <div class="form-row">
            <div class="form-group">
              <label for="company_name">Naziv kompanije</label>
              <input
                id="company_name"
                v-model="form.company_name"
                type="text"
                class="field"
                :class="{ 'field-error': errors.company_name }"
                placeholder="HT Eronet d.o.o."
                @blur="validateField('company_name')"
              />
              <span v-if="errors.company_name" class="error-msg">{{ errors.company_name }}</span>
            </div>
            <div class="form-group">
              <label for="jib">JIB</label>
              <input
                id="jib"
                v-model="form.jib"
                type="text"
                class="field"
                :class="{ 'field-error': errors.jib }"
                placeholder="4200000000000"
                @blur="validateField('jib')"
              />
              <span v-if="errors.jib" class="error-msg">{{ errors.jib }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="website_url">Web stranica</label>
              <input
                id="website_url"
                v-model="form.website_url"
                type="url"
                class="field"
                :class="{ 'field-error': errors.website_url }"
                placeholder="https://hteronet.ba"
                @blur="validateField('website_url')"
              />
              <span v-if="errors.website_url" class="error-msg">{{ errors.website_url }}</span>
            </div>
            <div class="form-group">
              <label for="address">Adresa</label>
              <input
                id="address"
                v-model="form.address"
                type="text"
                class="field"
                :class="{ 'field-error': errors.address }"
                placeholder="Kneza Višeslava 1, Mostar"
                @blur="validateField('address')"
              />
              <span v-if="errors.address" class="error-msg">{{ errors.address }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full">
              <label for="description">Opis kompanije</label>
              <textarea
                id="description"
                v-model="form.description"
                class="field"
                :class="{ 'field-error': errors.description }"
                placeholder="Telekom operator sa fokusom na mobilne, fiksne i optičke mreže."
                @blur="validateField('description')"
              />
              <span v-if="errors.description" class="error-msg">{{ errors.description }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">Email kompanije</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="field"
                :class="{ 'field-error': errors.email }"
                placeholder="hr@hteronet.ba"
                @blur="validateField('email')"
              />
              <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
            </div>
            <div class="form-group">
              <label for="phone_number">Broj telefona</label>
              <input
                id="phone_number"
                v-model="form.phone_number"
                type="tel"
                class="field"
                :class="{ 'field-error': errors.phone_number }"
                placeholder="+387 36 000 000"
                @blur="validateField('phone_number')"
              />
              <span v-if="errors.phone_number" class="error-msg">{{ errors.phone_number }}</span>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full">
              <label for="logo_url">URL loga</label>
              <input
                id="logo_url"
                v-model="form.logo_url"
                type="url"
                class="field"
                :class="{ 'field-error': errors.logo_url }"
                placeholder="https://hteronet.ba/logo.png"
                @blur="validateField('logo_url')"
              />
              <span v-if="errors.logo_url" class="error-msg">{{ errors.logo_url }}</span>
            </div>
          </div>

          <div class="form-row">
          <div class="form-group full">
            <label for="password">Lozinka</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="field"
              :class="{ 'field-error': errors.password }"
              placeholder="Minimalno 8 karaktera"
              @blur="validateField('password')"
            />
            <span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
          </div>
        </div>

          <div class="form-actions">
            <button class="btn-submit" :disabled="isLoading" @click="handleSubmit">
              <span v-if="isLoading">Slanje...</span>
              <span v-else>Registruj kompaniju</span>
            </button>
          </div>
        </template>

      </div>

      <div class="info-card">
        <h3>Nakon registracije</h3>
        <div v-for="(step, i) in steps" :key="i" class="info-step">
          <div class="step-num">{{ i + 1 }}</div>
          <div class="step-text">{{ step }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { registerCompany } from '../../services/api.js'

const form = reactive({
  company_name: '',
  jib: '',
  website_url: '',
  address: '',
  description: '',
  email: '',
  phone_number: '',
  logo_url: '',
  password: '',
})

const errors = reactive({
  company_name: '',
  jib: '',
  website_url: '',
  address: '',
  description: '',
  email: '',
  phone_number: '',
  logo_url: '',
  password: '',
})

const isLoading = ref(false)
const submitStatus = ref(null) // null | 'success' | 'error'
const serverError = ref('')

const steps = [
  'Predlažete praksu ili edukaciju.',
  'Administrator odobrava sadržaj prije objave.',
  'Pratite statuse prijedloga i prijave studenata.',
]

const validators = {
  company_name: (v) => v.trim() ? '' : 'Naziv kompanije je obavezan.',
  jib: (v) => {
    if (!v.trim()) return 'JIB je obavezan.'
    if (!/^\d{13}$/.test(v.trim())) return 'JIB mora sadržavati tačno 13 cifara.'
    return ''
  },
  website_url: (v) => {
    if (!v.trim()) return 'Web stranica je obavezna.'
    try { new URL(v.trim()); return '' }
    catch { return 'Unesite validan URL (npr. https://kompanija.ba).' }
  },
  address: (v) => v.trim() ? '' : 'Adresa je obavezna.',
  description: (v) => v.trim() ? '' : 'Opis kompanije je obavezan.',
  email: (v) => {
    if (!v.trim()) return 'Email je obavezan.'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())) return 'Unesite validan email.'
    return ''
  },
  phone_number: (v) => v.trim() ? '' : 'Broj telefona je obavezan.',
  logo_url: (v) => {
    if (!v.trim()) return 'URL loga je obavezan.'
    try { new URL(v.trim()); return '' }
    catch { return 'Unesite validan URL loga.' }
  },
  password: (v) => {
  if (!v.trim()) return 'Lozinka je obavezna.'
  if (v.length < 8) return 'Lozinka mora imati najmanje 8 karaktera.'
  return ''
  },
}

const validateField = (field) => {
  errors[field] = validators[field](form[field])
}

const validateAll = () => {
  let isValid = true
  for (const field in validators) {
    errors[field] = validators[field](form[field])
    if (errors[field]) isValid = false
  }
  return isValid
}

const handleSubmit = async () => {
  const valid = validateAll()
  console.log('Errors:', JSON.stringify(errors))
  if (!validateAll()) return

  isLoading.value = true
  submitStatus.value = null
  serverError.value = ''

  try {
    const response = await registerCompany({ ...form })

    if (response.ok) {
      submitStatus.value = 'success'
    } else {
      const data = await response.json()
      serverError.value = data.detail || 'Došlo je do greške. Pokušajte ponovo.'
      submitStatus.value = 'error'
    }
  } catch {
    serverError.value = 'Nije moguće povezati se sa serverom. Provjerite internet konekciju.'
    submitStatus.value = 'error'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* ── Base (mobile) ── */
.reg-page {
  padding: 1.25rem;
  background: #f9f8f6;
  min-height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.reg-header {
  margin-bottom: 1.5rem;
}

.reg-header h1 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 0.3rem;
}

.reg-header p {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.reg-layout {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.reg-card,
.info-card {
  background: #fff;
  border: 1px solid #e8e8e4;
  border-radius: 12px;
  padding: 1.25rem;
}

.alert {
  border-radius: 8px;
  padding: 0.9rem 1rem;
  font-size: 0.9rem;
  margin-bottom: 1.25rem;
}

.alert-success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
}

.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
}

.field {
  padding: 0.65rem 0.85rem;
  border: 1px solid #ddd;
  border-radius: 7px;
  font-size: 0.95rem;
  color: #1a1a1a;
  background: #fff;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  font-family: inherit;
  transition: border-color 0.15s;
}

.field:focus {
  border-color: #e87722;
  box-shadow: 0 0 0 3px rgba(232, 119, 34, 0.12);
}

.field-error {
  border-color: #e53e3e;
}

.field-error:focus {
  border-color: #e53e3e;
  box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.12);
}

.error-msg {
  font-size: 0.8rem;
  color: #e53e3e;
}

textarea.field {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.btn-submit {
  width: 100%;
  background: #e87722;
  color: #fff;
  border: none;
  border-radius: 7px;
  padding: 0.8rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-submit:hover:not(:disabled) {
  background: #cf6918;
}

.btn-submit:disabled {
  background: #f0b07a;
  cursor: not-allowed;
}

.info-card h3 {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 1rem;
}

.info-step {
  display: flex;
  gap: 0.85rem;
  margin-bottom: 1rem;
  align-items: flex-start;
}

.step-num {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2px solid #e87722;
  color: #e87722;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.step-text {
  font-size: 0.88rem;
  color: #555;
  line-height: 1.4;
  padding-top: 3px;
}

/* ── Tablet (640px+) ── */
@media (min-width: 640px) {
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
  }

  .form-group.full {
    grid-column: 1 / -1;
  }

  .btn-submit {
    width: auto;
  }
}

/* ── Desktop (1024px+) ── */
@media (min-width: 1024px) {
  .reg-page {
    padding: 2rem;
  }

  .reg-header h1 {
    font-size: 1.6rem;
  }

  .reg-layout {
    display: grid;
    grid-template-columns: 1fr 320px;
    align-items: start;
  }

  .reg-card,
  .info-card {
    padding: 2rem;
  }
}
</style>