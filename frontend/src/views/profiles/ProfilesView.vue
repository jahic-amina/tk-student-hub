<template>
  <div class="min-h-screen bg-gray-50 flex flex-col font-sans text-sm text-gray-600 relative">
    
    <div v-if="toast.show" class="fixed top-5 right-5 z-50 bg-green-500 text-white px-5 py-3 rounded-xl shadow-lg font-semibold flex items-center gap-2 animate-bounce">
      <span>✓</span> {{ toast.message }}
    </div>

    <main class="flex-1 max-w-5xl w-full mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <div class="space-y-4">
        <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm text-center">
          <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=128" class="w-24 h-24 rounded-full object-cover mx-auto mb-3 border border-orange-200"/>
          <h3 class="text-base font-bold text-gray-800">{{ form.first_name }} {{ form.last_name }}</h3>
          <p class="text-xs text-gray-400 mb-4">{{ form.email }}</p>
  
          <button @click="navigateToUpload" type="button" class="w-full py-2 bg-orange-50 hover:bg-orange-100 text-orange-600 rounded-xl border border-orange-200 font-bold text-xs transition shadow-sm flex justify-center items-center gap-2">
            <span>📷</span> Uredi profilnu sliku
          </button>
        </div>

        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div class="px-4 py-2.5 bg-gray-50 border-b text-xs font-bold text-gray-400 uppercase tracking-wider">Aktivnost</div>
          <nav class="divide-y divide-gray-50">
            <a href="#" class="block px-4 py-2.5 hover:bg-orange-50 hover:text-orange-500 transition font-medium">Historija</a>
            <a href="#" class="block px-4 py-2.5 hover:bg-orange-50 hover:text-orange-500 transition font-medium">Sačuvano</a>
            <a href="#" class="block px-4 py-2.5 hover:bg-orange-50 hover:text-orange-500 transition font-medium">Javni Profil</a>
          </nav>
        </div>
      </div>

      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <h2 class="text-xl font-bold text-orange-500 mb-1">Uredi profil</h2>
          <p class="text-xs text-gray-400 mb-4">Ažurirajte vaše lične podatke i biografiju</p>
          
          <div v-if="status.isError && status.message" class="mb-4 p-3 rounded-xl text-xs bg-red-50 text-red-700 border border-red-100 font-medium">
            ⚠️ {{ status.message }}
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div><label class="block font-medium mb-1">Ime</label><input v-model="form.first_name" type="text" class="w-full p-2.5 border rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"/></div>
              <div><label class="block font-medium mb-1">Prezime</label><input v-model="form.last_name" type="text" class="w-full p-2.5 border rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"/></div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div><label class="block font-medium mb-1">Email</label><input v-model="form.email" type="email" disabled class="w-full p-2.5 border bg-gray-50 text-gray-400 rounded-xl cursor-not-allowed"/></div>
              <div>
                <label class="block font-medium mb-1">Godina studija</label>
                <select v-model="form.study_year" class="w-full p-2.5 border rounded-xl bg-white focus:ring-2 focus:ring-orange-500 focus:outline-none">
                  <option :value="null" disabled>Odaberite godinu studija</option>
                  <option v-for="y in 4" :key="y" :value="y">{{ y }}. godina</option>
                </select>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-xs mb-1">
                <label class="font-medium text-gray-700">Biografija</label>
                <span :class="form.bio.length > 500 ? 'text-red-500 font-bold' : 'text-gray-400'">{{ form.bio.length }}/500</span>
              </div>
              <textarea v-model="form.bio" rows="3" placeholder="Dodaj biografiju..." class="w-full p-2.5 border rounded-xl resize-none focus:ring-2 focus:ring-orange-500 focus:outline-none"></textarea>
            </div>

            <div class="pt-4 border-t space-y-3">
              <h3 class="font-bold text-gray-700 uppercase tracking-wider text-xs">Promijeni lozinku</h3>
              <div><label class="block text-xs font-medium mb-1 text-gray-500">Stara lozinka</label><input v-model="security.current_password" type="password" class="w-full sm:w-1/2 p-2.5 border rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"/></div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div><label class="block text-xs font-medium mb-1 text-gray-500">Nova lozinka</label><input v-model="security.new_password" type="password" class="w-full p-2.5 border rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"/></div>
                <div><label class="block text-xs font-medium mb-1 text-gray-500">Ponovi novu lozinku</label><input v-model="security.confirm_password" type="password" class="w-full p-2.5 border rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"/></div>
              </div>
            </div>

            <div class="flex justify-end pt-2 border-t">
              <button type="submit" :disabled="isLoading || form.bio.length > 500" class="px-6 py-2 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl disabled:opacity-50 transition active:scale-95 text-sm shadow-md">
                {{ isLoading ? 'Spašavanje...' : 'Sačuvaj izmjene' }}
              </button>
            </div>
          </form>
        </div>

        <div class="bg-red-50 p-6 rounded-2xl border border-red-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h3 class="text-sm font-bold text-red-800">Deaktivacija i brisanje</h3>
            <p class="text-xs text-red-500">Privremeno onemogućite ili trajno uklonite svoj račun.</p>
          </div>
          <div class="flex gap-3 text-xs">
            <button @click="alertAction('Deaktivacija računa')" type="button" class="px-4 py-2 bg-white text-red-700 border border-red-200 font-bold rounded-xl hover:bg-red-100 transition">Deaktiviraj nalog</button>
            <button @click="alertAction('Brisanje računa')" type="button" class="px-4 py-2 bg-red-600 text-white font-bold rounded-xl hover:bg-red-700 transition">Izbriši nalog</button>
          </div>
        </div>

      </div>
      <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm text-center">
        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=128" class="w-24 h-24 rounded-full object-cover mx-auto mb-3 border border-orange-200"/>
        <h3 class="text-base font-bold text-gray-800">{{ form.first_name }} {{ form.last_name }}</h3>
        <p class="text-xs text-gray-400 mb-4">{{ form.email }}</p>
  
        <button @click="showUploadModal = true" type="button" class="w-full py-2 bg-orange-50 hover:bg-orange-100 text-orange-600 rounded-xl border border-orange-200 font-bold text-xs transition shadow-sm flex justify-center items-center gap-2">
           <span>📷</span> Uredi profilnu sliku
        </button>
      </div>

      <AvatarUploadModal 
        v-if="showUploadModal" 
        @close="showUploadModal = false" 
        @save="handleSaveImage"
        @remove="handleRemoveImage"
        :initials="form.first_name.charAt(0) + form.last_name.charAt(0)"
      />
    </main>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import AvatarUploadModal from '../../components/AvatarUploadModal.vue'
import axios from 'axios'
const showUploadModal = ref(false)
const handleSaveImage = (file) => {
  console.log('Spremam sliku:', file)
  // Ovdje će ići API poziv za slanje slike na backend (uploadAvatar)
  showUploadModal.value = false
}

const handleRemoveImage = () => {
  console.log('Brišem sliku...')
  // Ovdje će ići API poziv za brisanje (removeAvatar)
  showUploadModal.value = false
}
const API_BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({ baseURL: API_BASE_URL })
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const form = reactive({ first_name: '', last_name: '', email: '', study_year: 1, bio: '' })
const security = reactive({ current_password: '', new_password: '', confirm_password: '' })
const isLoading = ref(false)
const status = reactive({ message: '', isError: false })
const toast = reactive({ show: false, message: '' })

const showToast = (msg) => {
  toast.message = msg; toast.show = true
  setTimeout(() => { toast.show = false }, 3000)
}
const alertAction = (action) => alert(`${action} će biti uskoro dostupno!`)

const fetchUserProfile = async () => {
  status.message = ''
  status.isError = false
  try {
    const { data } = await api.get('/profiles/me')
    if (data) {
      // 1. Čupamo ime i prezime iz full_name
      const fullName = data.full_name || ''
      const nameParts = fullName.trim().split(' ')
      form.first_name = nameParts[0] || ''
      form.last_name = nameParts.slice(1).join(' ') || ''
      
      // 2. Mapiramo ostale podatke
      form.email = data.email || ''
      
      // Dodali smo "|| data.biografija" kao plan B, ako je backend vraća na bosanskom
      form.study_year = data.study_year || data.godina_studija || 1
      form.bio = data.bio || data.biografija || ''
    }
  } catch (err) {
    console.error('Greška pri učitavanju profila:', err)
    if (err.response?.status === 401) {
      status.message = 'Sesija je istekla. Molimo vas da se ponovo prijavite.'
      status.isError = true
    }
  }
}

const handleSubmit = async () => {
  if (form.bio.length > 500) return
  
  isLoading.value = true
  status.message = ''
  status.isError = false
  
  const mergedName = `${form.first_name.trim()} ${form.last_name.trim()}`

  try {
    if (security.new_password && security.new_password !== security.confirm_password) {
      throw new Error('Nove lozinke se ne podudaraju.')
    }

   
    await api.patch('/profiles/me', {
      full_name: mergedName,
      biografija: form.bio,            
      godina_studija: form.study_year  
    })

    showToast('Izmjene su uspješno sačuvane!')
    
    // Osvježavamo podatke sa servera da potvrdimo
    await fetchUserProfile()
  } catch (err) {
    status.message = err.response?.data?.detail || err.message || 'Greška prilikom spašavanja.'
    status.isError = true
    console.error('Detalji greške:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchUserProfile)
</script>