<template>
  <div>
    <div v-if="!isEditing" class="max-w-4xl mx-auto py-8 px-4">

      <div v-if="loading" class="text-center py-20 text-gray-400"> Učitavanje...</div>

      <div v-else-if="error" class="bg-red-100 text-red-600 p-4 rounded-lg">
         {{ error }} 
      </div>
      
      <div v-else-if="profile">
        <UserProfileCard :profile="profile" @edit-avatar="showModal = true" @edit-profile="isEditing = true"/>
        
        <div class="bg-white rounded-xl shadow p-6 mb-6">
          <h2 class="text-lg font-bold mb-3">O meni</h2>
          <p class="text-gray-600 text-sm">{{ profile.biografija || 'Nije unesena biografija.' }}</p>
        </div>
      <div class="grid grid-cols-2 gap-6">
  <div class="bg-white rounded-xl shadow p-6">
    <h2 class="text-lg font-bold mb-4">Trenutne prakse</h2>
    <div v-if="prakse.length === 0">
      <p class="text-gray-400 text-sm">Nema trenutnih praksi.</p>
    </div>
    <div v-else class="flex flex-col gap-3">
      <div v-for="praksa in prakse" :key="praksa.id">
        <p class="font-medium text-gray-800">{{ praksa.naziv }}</p>
        <p class="text-sm text-gray-400">{{ praksa.kompanija }} · <span class="text-orange-500">{{ praksa.status }}</span></p>
      </div>
    </div>
  </div>

  <div class="bg-white rounded-xl shadow p-6">
    <h2 class="text-lg font-bold mb-4">Nedavna aktivnost</h2>
    <ActivityFeed :activities="activities" :loading="activityLoading" />
    <button 
      v-if="hasMore && !showingAll"
      @click="handleShowAll"
      class="mt-4 text-sm text-orange-500 hover:text-orange-600 flex items-center gap-1"
    >
      Prikaži sve
    </button>
  </div>
</div>
        <div v-if="successMessage" class="mt-4 bg-green-100 text-green-700 p-3 rounded-lg font-medium">{{ successMessage }} </div>
      </div>

    </div>

    <div v-else class="min-h-screen bg-gray-50 flex flex-col font-sans text-sm text-gray-600 relative">
      
      <div v-if="toast.show" class="fixed top-5 right-5 z-50 bg-green-500 text-white px-5 py-3 rounded-xl shadow-lg font-semibold flex items-center gap-2 animate-bounce">
        <span>✓</span> {{ toast.message }}
      </div>

      <div class="max-w-5xl w-full mx-auto px-4 pt-6">
        <button @click="isEditing = false" class="text-gray-400 hover:text-gray-800 font-bold flex items-center gap-2 transition px-3 py-1.5 rounded-lg hover:bg-gray-100">
          ← Nazad na profil
        </button>
      </div>

      <main class="flex-1 max-w-5xl w-full mx-auto px-4 py-4 grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="space-y-4">
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm text-center">
            <div class="w-24 h-24 rounded-full mx-auto mb-3 border bg-gray-200 flex items-center justify-center overflow-hidden">
              <img v-if="profile?.profilna_slika_url" :src="`http://localhost:8000${profile.profilna_slika_url}`" class="w-full h-full object-cover" />
              <span v-else class="text-white text-4xl font-bold">{{ getInitials() }}</span>
            </div>            
            <p class="text-xs text-gray-400 mb-4">{{ form.email }}</p>
            <button @click="showModal = true" type="button" class="w-full py-2 bg-orange-55 hover:bg-orange-100 text-orange-600 rounded-xl border border-orange-200 font-bold text-xs transition shadow-sm flex justify-center items-center gap-2">
              <span>📷</span> Uredi profilnu sliku
            </button>
          </div>

          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="px-4 py-2.5 bg-gray-50 border-b text-xs font-bold text-gray-400 uppercase tracking-wider">Aktivnost</div>
            <nav class="divide-y divide-gray-50">
              <a v-for="link in ['Historija', 'Sačuvano', 'Javni Profil']" :key="link" href="#" class="block px-4 py-2.5 hover:bg-orange-50 hover:text-orange-500 transition font-medium">{{ link }}</a>
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
              <h3 class="text-sm font-bold text-red-800">Deaktivacija računa</h3>
              <p class="text-xs text-red-500">Privremeno onemogućite svoj račun.</p>
            </div>
            <button @click="showDeactivateModal = true" type="button" class="px-4 py-2 bg-white text-red-700 border border-red-200 font-bold rounded-xl hover:bg-red-100 transition text-xs">Deaktiviraj nalog</button>          </div>
        </div>
      </main>
    </div>

    <AvatarUploadModal 
      v-if="showModal" 
      :currentImageUrl="profile?.profilna_slika_url"
      @close="showModal = false" 
      @save="onSave"
      @remove="onRemove"
      :initials="(form.first_name?.charAt(0) || '') + (form.last_name?.charAt(0) || '')"
    />
    <div v-if="showDeactivateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 px-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-xl border border-gray-100">
        <h3 class="text-lg font-bold text-red-600 mb-2">Potvrda deaktivacije</h3>
        <p class="text-sm text-gray-600 mb-4">
          Da biste deaktivirali nalog, molimo unesite svoju lozinku. Nakon uspješne deaktivacije bićete odjavljeni iz sistema.
        </p>
        
        <div v-if="deactivateError" class="mb-4 p-3 rounded-xl text-xs bg-red-50 text-red-700 border border-red-100 font-medium">
          ⚠️ {{ deactivateError }}
        </div>
        
        <label class="block text-xs font-medium mb-1 text-gray-500">Vaša lozinka</label>
        <input 
          v-model="deactivatePassword" 
          type="password" 
          placeholder="Unesite lozinku..." 
          class="w-full p-2.5 border rounded-xl focus:ring-2 focus:ring-red-500 focus:outline-none mb-6"
        />
        
        <div class="flex justify-end gap-3">
          <button @click="closeDeactivateModal" :disabled="isDeactivating" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl font-medium transition text-sm">
            Odustani
          </button>
          <button @click="handleDeactivate" :disabled="isDeactivating || !deactivatePassword" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl disabled:opacity-50 transition shadow-md text-sm">
            {{ isDeactivating ? 'Deaktivacija...' : 'Potvrdi deaktivaciju' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 px-4">
      <div class="bg-white rounded-2xl p-8 w-full max-w-md shadow-xl border border-gray-100 text-center">
        <div class="mb-4 text-4xl">✓</div>
        <h3 class="text-lg font-bold text-green-600 mb-2">Deaktivacija uspješna</h3>
        <p class="text-sm text-gray-600 mb-6">
          Uspješno ste deaktivirali profil. Za ponovnu aktivaciju obratite se administratoru.
        </p>
        
        <button @click="handleSuccessModalClose" class="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition shadow-md text-sm">
          Razumijem
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

import UserProfileCard from '../../components/UserProfileCard.vue'
import AvatarUploadModal from '../../components/AvatarUploadModal.vue'
import { getMyProfile, uploadAvatar, removeAvatar } from '../../services/api.js'
import ActivityFeed from '../../components/ActivityFeed.vue'
import { getMyActivity } from '../../services/api.js'


const activities = ref([])
const activityLoading = ref(false)
const hasMore = ref(false)
const showingAll = ref(false)

function getToken() {
  return localStorage.getItem('token') || localStorage.getItem('access_token')
}

async function loadPreview() {
  activityLoading.value = true
  try {
    const data = await getMyActivity(getToken(), 3, 0)
    activities.value = data.items
    hasMore.value = data.has_more
  } catch (error) {
    console.error('Greška pri dohvatanju aktivnosti:', error)
  } finally {
    activityLoading.value = false
  }
}

async function loadAll() {
  activityLoading.value = true
  try {
    const data = await getMyActivity(getToken(), 20, 0)
    activities.value = data.items
    hasMore.value = data.has_more
  } catch (error) {
    console.error('Greška pri dohvatanju aktivnosti:', error)
  } finally {
    activityLoading.value = false
  }
}

async function handleShowAll() {
  await loadAll()
  showingAll.value = true
}

function getInitials() {
  const first = form.first_name?.charAt(0).toUpperCase() || ''
  const last = form.last_name?.charAt(0).toUpperCase() || ''
  return first + last
}

const api = axios.create({ baseURL: 'http://127.0.0.1:8000' })
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
api.interceptors.response.use(
  (response) => {
    return response; // Ako je sve ok, samo proslijedi odgovor dalje
  },
  (error) => {
    // Provjeravamo da li je backend vratio grešku 403 i našu poruku o deaktivaciji
    if (error.response && error.response.status === 403) {
      if (error.response.data?.detail?.includes("deaktiviran")) {
        
        // 1. Očisti tokene (odjavi korisnika)
        localStorage.removeItem('token')
        localStorage.removeItem('access_token')
        
        // 2. Izbaci upozorenje
        alert("Vaš nalog je deaktiviran. Kontaktirajte administratora za reaktivaciju.")
        
        // 3. Preusmjeri ga na stranicu za login
        window.location.href = '/login' // Prilagodi putanju ako ti se login ruta zove drugačije
      }
    }
    return Promise.reject(error);
  }
)

const token = localStorage.getItem('token') || localStorage.getItem('access_token')

const isEditing = ref(false) 

const profile = ref(null)
const loading = ref(false)
const error = ref(null)
const successMessage = ref(null)
const showModal = ref(false)
const router = useRouter()
const showDeactivateModal = ref(false)
const showSuccessModal = ref(false)
const deactivatePassword = ref('')
const deactivateError = ref('')
const isDeactivating = ref(false)
const closeDeactivateModal = () => {
  showDeactivateModal.value = false
  deactivatePassword.value = ''
  deactivateError.value = ''
}

const isLoading = ref(false)
const toast = reactive({ show: false, message: '' })
const status = reactive({ message: '', isError: false })
const form = reactive({ first_name: '', last_name: '', email: '', study_year: 1, bio: '' })
const security = reactive({ current_password: '', new_password: '', confirm_password: '' })

const showToast = (msg) => {
  Object.assign(toast, { show: true, message: msg })
  setTimeout(() => toast.show = false, 3000)
}
const alertAction = (action) => alert(`${action} će biti uskoro dostupno!`)

const fetchProfileData = async () => {
  loading.value = true
  error.value = null
  Object.assign(status, { message: '', isError: false })
  
  try {
    const data = await getMyProfile(token)
    profile.value = data 
    
    if (data) {
      const [first, ...rest] = (data.full_name || '').trim().split(' ')
      Object.assign(form, {
        first_name: first || '',
        last_name: rest.join(' '),
        email: data.email || '',
        study_year: data.study_year || data.godina_studija || 1,
        bio: data.bio || data.biografija || ''
      })
    }
  } catch (err) {
    if (err.response && err.response.status === 403) {
      // 1. Očisti tokene
      localStorage.removeItem('token')
      localStorage.removeItem('access_token')
      
      // 2. Obavijesti korisnika
      alert("Vaš nalog je deaktiviran. Kontaktirajte administratora za reaktivaciju.")
      
      // 3. Vrati ga na login
      window.location.href = '/login' 
      return // Prekidamo dalje izvršavanje koda
    }
    error.value = "Greška pri učitavanju profila. Molimo pokušajte ponovo."
    if (err.response?.status === 401) Object.assign(status, { message: 'Sesija je istekla.', isError: true })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfileData()
  loadPreview()
})

const handleSubmit = async () => {
  const { first_name, last_name, bio, study_year } = form
  
  if (!first_name.trim() || !last_name.trim()) return Object.assign(status, { message: 'Ime i prezime su obavezni.', isError: true })
  if (bio.length > 500) return
  
  isLoading.value = true
  Object.assign(status, { message: '', isError: false })

  try {
    await api.patch('/profiles/me', { 
      full_name: `${first_name.trim()} ${last_name.trim()}`, 
      biografija: bio, 
      godina_studija: study_year 
    })

    const { current_password, new_password, confirm_password } = security
    if (current_password || new_password) {
      if (!current_password) throw new Error('Unesite trenutnu lozinku.')
      if (new_password !== confirm_password) throw new Error('Nove lozinke se ne podudaraju.')
      
      await api.patch('/profiles/me/password', { current_password, new_password })
      Object.assign(security, { current_password: '', new_password: '', confirm_password: '' })
    }

    showToast('Izmjene uspješno sačuvane!')

    await fetchProfileData() 
  } catch (err) {
    Object.assign(status, { message: err.response?.data?.detail || err.message || 'Greška prilikom spašavanja.', isError: true })
  } finally {
    isLoading.value = false
  }
}

async function onSave(file) {
  showModal.value = false
  try {
    const data = await uploadAvatar(token, file)
    console.log('Response od backend-a:', data)
    if(profile.value) profile.value.profilna_slika_url = data.profilna_slika_url
    successMessage.value = 'Profilna slika je uspjesno azurirana.'
    showToast('Profilna slika je uspješno ažurirana.')
    setTimeout(() => { successMessage.value = null }, 3000)
  } catch (e) {
    error.value = 'Greska pri uploadu slike.'
    Object.assign(status, { message: 'Greska pri uploadu slike.', isError: true })
  }
}

async function onRemove() {
  showModal.value = false
  try {
    await removeAvatar(token)
    if(profile.value) profile.value.profilna_slika_url = null
    
    successMessage.value = 'Profilna slika je uklonjena.'
    showToast('Profilna slika je uklonjena.')
    setTimeout(() => { successMessage.value = null }, 3000)
  } catch (e) {
    error.value = 'Greska pri uklanjanju slike.'
    Object.assign(status, { message: 'Greska pri uklanjanju slike.', isError: true })
  }
}
const prakse = ref([
  {
    id: 1,
    naziv: "Full Stack Developer",
    kompanija: "Tech Corp",
    status: "U toku"
  },
  {
    id: 2,
    naziv: "AI Research Assistant",
    kompanija: "University Lab",
    status: "U toku"
  }
])

// --- Funkcija za deaktivaciju ---
const handleDeactivate = async () => {
  if (!deactivatePassword.value) return

  isDeactivating.value = true
  deactivateError.value = ''

  try {
    // Pozivamo backend rutu 
    await api.post('/account/deactivate', { 
      password: deactivatePassword.value 
    })

    // Ako je uspješno, zatvori modal
    closeDeactivateModal()
    
    // Obriši sesiju (token) iz lokalnog storage-a
    localStorage.removeItem('token')
    localStorage.removeItem('access_token')
    
    // Prikaži success modal
    showSuccessModal.value = true

  } catch (err) {
    // Ako lozinka nije tačna, ispiši grešku unutar modala
    deactivateError.value = err.response?.data?.detail || "Greška pri deaktivaciji. Pokušajte ponovo."
  } finally {
    isDeactivating.value = false
  }
}

const handleSuccessModalClose = () => {
  showSuccessModal.value = false
  // Preusmjeri korisnika na login nakon što zatvori modal
  router.push('/login')
}
</script>