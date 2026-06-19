<template>
    <!-- Modal za promjenu ocjene - Marinela -->
    <div v-if="showChangeModal" class="fixed inset-0 flex items-center justify-center z-[60]">
        <div class="bg-white dark:bg-slate-800 rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
          <h3 class="text-xl font-bold text-gray-800 dark:text-slate-100 mb-2">Želite li promijeniti ocjenu?</h3>
          <p class="text-gray-600 dark:text-slate-300 mb-6">Već ste ocijenili ovaj materijal. Da li ste sigurni?</p>
          <div class="flex gap-3 justify-center">
        <button @click="showChangeModal = false" class="border border-gray-300 dark:border-slate-600 dark:text-slate-200 px-6 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-700 transition">Ne</button>
        <button @click="confirmChangeRating" class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition">Da, promijeni</button>
            </div>
        </div>
        <div class="fixed inset-0 bg-black opacity-40 -z-10"></div>
    </div>

    <!-- Modal uspjeh ocjene -->
   <div v-if="ratingMessage" class="fixed inset-0 flex items-center justify-center z-[60]">
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
        <div class="text-5xl mb-4">⭐</div>
        <h3 class="text-xl font-bold text-gray-800 dark:text-slate-100 mb-2">{{ ratingMessage === 'Ocjena promijenjena! ⭐' ? 'Ocjena promijenjena!' : 'Hvala na ocjeni!' }}</h3>
        <p class="text-gray-600 dark:text-slate-300 mb-6">{{ ratingMessage === 'Ocjena promijenjena! ⭐' ? 'Vaša ocjena je uspješno promijenjena.' : 'Uspješno ste ocijenili ovaj materijal.' }}</p>
        <button @click="ratingMessage = ''" class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition">U redu</button>
    </div>
    <div class="fixed inset-0 bg-black opacity-40 -z-10"></div>
  </div>

    <!-- Ocjena materijala -->
    <div class="mb-6">
        <h3 class="font-semibold mb-2 text-base">Ocjena materijala</h3>
        <div class="flex items-center gap-2">
            <span v-for="star in 5" :key="star" class="text-yellow-400 text-2xl">
                {{ star <= Math.round(localAvgRating) ? '★' : '☆' }}
            </span>
            <span class="text-gray-600 dark:text-slate-300 text-sm">{{ localAvgRating }} / 5.0 ({{ localRatingCount }} ocjena)</span>
        </div>

        <!-- Ocijeni -->
        <div class="mt-4">
            <p class="text-sm text-gray-500 dark:text-slate-400 mb-1">{{ selectedRating > 0 ? 'Vaša ocjena:' : 'Ocijenite ovaj materijal:' }}</p>
        <div class="flex gap-1">
                <span v-for="star in 5" :key="star" class="text-2xl transition"
                    :class="[
                        star <= hoverRating || star <= selectedRating ? 'text-yellow-400' : 'text-gray-300',
                       (isLoggedIn && hasDownloaded) ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'
                    ]"
                    @mouseover="isLoggedIn && (hoverRating = star)"
                    @mouseleave="hoverRating = 0"
                    @click="submitRating(star)">★</span>
            </div>
            <p v-if="ratingError" class="text-sm text-red-600 mt-2">{{ ratingError }}</p>
            <p v-if="isLoggedIn && !hasDownloaded" class="text-sm text-gray-400 dark:text-slate-500 mt-2">
                Preuzmite materijal da biste mogli ocijeniti.
            </p>
            <p v-if="!isLoggedIn" class="text-sm text-gray-400 dark:text-slate-500 mt-2">
                Prijavite se da biste mogli ocijeniti materijal.
            </p>
        </div>
    </div>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'

// Importujemo API funkcije umjesto direktnog fetch-a
import { getMaterial, rateMaterial, updateRating, checkHasDownloaded } from '../services/api'

const props = defineProps({
    materialId: {
        type: Number,
        required: true
    },
    parentHasDownloaded: {
        type: Boolean,
        default: false
    }
})

const hoverRating = ref(0)
const selectedRating = ref(0)

// Lokalne kopije prosjecne ocjene i broja ocjena
const localAvgRating = ref(0)
const localRatingCount = ref(0)

// Korisnikova ocjena
const myRating = ref(0)

// Provjera da li je korisnik preuzeo materijal
const hasDownloaded = ref(false)
watch(() => props.parentHasDownloaded, (downloaded) => {
    if (downloaded) {
        hasDownloaded.value = true
    }
})

// Poruke uspjeha i greske
const ratingMessage = ref('')
const ratingError = ref('')

// Modal za promjenu ocjene
const showChangeModal = ref(false)
const pendingStar = ref(0)

// Provjera da li je korisnik prijavljen
const isLoggedIn = computed(() => !!localStorage.getItem('token'))

// Izvuci user_id iz JWT tokena
function getUserIdFromToken() {
    const token = localStorage.getItem('token')
    if (!token) return null
    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return Number(payload.sub) || Number(payload.user_id) || Number(payload.id)
    } catch {
        return null
    }
}

// Kad se komponenta mountuje, fetchaj ocjene i provjeri korisnikovu ocjenu
onMounted(async () => {
    ratingError.value = ''
    const data = await getMaterial(props.materialId)
    if (data.ratings && data.ratings.length > 0) {
        const sum = data.ratings.reduce((acc, r) => acc + r.rating, 0)
        localAvgRating.value = Math.round((sum / data.ratings.length) * 10) / 10
        localRatingCount.value = data.ratings.length
    }

    // Provjera da li je korisnik vec ocijenio ovaj materijal
    if (isLoggedIn.value) {
       const userId = getUserIdFromToken()
       const myRatingObj = data.ratings?.find(r => r.user_id === userId)
        if (myRatingObj) {
            myRating.value = myRatingObj.rating
            selectedRating.value = myRatingObj.rating
        } 
       // Provjera da li je korisnik preuzeo materijal
    try {
         const token = localStorage.getItem('token')
         const json = await checkHasDownloaded(props.materialId)
         hasDownloaded.value = json.has_downloaded
         await nextTick()  
    } catch {
        hasDownloaded.value = false
    }
}
}) 

// Slanje ocjene na backend
async function submitRating(star) {
    if (!isLoggedIn.value) return

 // Blokira ocjenjivanje ako korisnik nije preuzeo materijal
    if (!hasDownloaded.value) {
    return
    }
    
 // Ako je vec ocijenio, prikazuje modal za promjenu
    if (selectedRating.value > 0) {
        pendingStar.value = star
        showChangeModal.value = true
        return
    }

// Provjera - korisnik ne moze ocijeniti vlastiti materijal 
const userId = getUserIdFromToken()
const materialData = await getMaterial(props.materialId)
if (materialData.user?.id === Number(userId)) {
    ratingError.value = 'Ne možete ocijeniti vlastiti materijal.'
    return
}

    selectedRating.value = star
    ratingMessage.value = ''
    ratingError.value = ''
    try {
        const response = await rateMaterial(props.materialId, star)

        if (response.status === 409) { ratingError.value = 'Već ste ocijenili ovaj materijal.'; return }
        if (!response.ok) { ratingError.value = 'Greška prilikom ocjenjivanja.'; return }
        ratingMessage.value = 'Hvala na ocjeni! ⭐'
        ratingError.value = ''
        await refreshRating()
    } catch (err) {
        ratingError.value = 'Greška prilikom ocjenjivanja.'
    }
}

// Promjena postojece ocjene
async function confirmChangeRating() {
    showChangeModal.value = false
    ratingMessage.value = '' 
    ratingError.value = '' 
    try {
        const response = await updateRating(props.materialId, pendingStar.value)
        if (!response.ok) { ratingError.value = 'Greška prilikom promjene ocjene.'; return }
        selectedRating.value = pendingStar.value
        ratingMessage.value = 'Ocjena promijenjena! ⭐'
        ratingError.value = ''
        await refreshRating()
    } catch (err) {
        ratingError.value = 'Greška prilikom promjene ocjene.'
    }
}

// Osvjezavanje prosjecne ocjene i broja ocjena nakon ocjenjivanja
async function refreshRating() {
    const data = await getMaterial(props.materialId)
    if (data.ratings && data.ratings.length > 0) {
        const sum = data.ratings.reduce((acc, r) => acc + r.rating, 0)
        localAvgRating.value = Math.round((sum / data.ratings.length) * 10) / 10
        localRatingCount.value = data.ratings.length
    }
}
</script>