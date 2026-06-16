<template>
<!----------------------------------------------------------------------------------------------------------------->
<!---Promjena ocijene - Marinela---->
<div v-if="showChangeModal" class="fixed inset-0 flex items-center justify-center z-[60]">
    <div class="bg-white rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
        <div class="text-5xl mb-4">⭐</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Želite li promijeniti ocjenu?</h3>
        <p class="text-gray-600 mb-6">Već ste ocijenili ovaj materijal. Da li ste sigurni da želite promijeniti svoju ocjenu?</p>
        <div class="flex gap-3 justify-center">
            <button @click="showChangeModal = false"
                class="border border-gray-300 px-6 py-2 rounded-lg hover:bg-gray-50 transition">
                Ne
            </button>
            <button @click="confirmChangeRating"
                class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition">
                Da, promijeni
            </button>
        </div>
    </div>
    <div class="fixed inset-0 bg-black opacity-40 -z-10"></div>
</div> 

<!----------------------------------------------------------------------------------------------------------->
  <!-- Overlay -->
    <div class="fixed inset-0 bg-black/50 z-40" @click="$emit('close')" />

    <!-- Modal -->
    <div
        class="fixed inset-0 sm:inset-auto sm:top-1/2 sm:left-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2 bg-white sm:rounded-xl sm:w-[600px] sm:max-h-[80vh] overflow-y-auto z-50 p-6">

        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
            <div>
                <h2 class="text-xl font-bold">{{ material.title }}</h2>
                <p class="text-sm text-gray-400">
                    Postavio: {{ material.user.full_name }} • {{ formatDate(material.created_at) }}
                </p>
            </div>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">✕</button>
        </div>

        <hr class="mb-4" />

        <!-- Opis -->
        <div class="mb-6">
            <h3 class="font-semibold mb-2">Detaljan opis</h3>
            <p class="text-gray-600 text-sm">{{ material.description }}</p>
        </div>

<!---Poruka za uspjesno ocijenjen materijal - Marinela--->
<div v-if="ratingMessage" class="fixed inset-0 flex items-center justify-center z-[60]">
    <div class="bg-white rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
        <div class="text-5xl mb-4">⭐</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Hvala na ocjeni!</h3>
        <p class="text-gray-600 mb-6">Uspješno ste ocijenili ovaj materijal.</p>
        <button
            @click="ratingMessage = ''"
            class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition">
            U redu
        </button>
    </div>
    <div class="fixed inset-0 bg-black opacity-40 -z-10"></div>
</div>
<!------------------------------------------------------------------------------------------>

        <!-- Ocjena -->
        <div class="mb-6">
            <h3 class="font-semibold mb-2">Ocjena materijala</h3>
            <div class="flex items-center gap-2">
                <span v-for="star in 5" :key="star" class="text-yellow-400 text-2xl">
                    {{ star <= Math.round(localAvgRating) ? '★' : '☆' }} </span>
                        <span class="text-gray-600">{{ localAvgRating }} / 5.0 ({{ localRatingCount }}
                            ocjena)</span>
            </div>
           
            <p class="text-sm text-gray-500 mt-2">Broj preuzimanja: {{ material.number_of_downloads }}</p>

            <!-- Ocijeni -->
            <div class="mt-4">
                <p class="text-sm text-gray-500 mb-1">{{ selectedRating > 0 ? 'Vaša ocjena:' : 'Ocijenite ovaj materijal:' }}</p>
                <div class="flex gap-1">
                    <span v-for="star in 5" :key="star" class="text-2xl cursor-pointer transition"
                        :class="[
                star <= hoverRating || star <= selectedRating ? 'text-yellow-400' : 'text-gray-300',
                isLoggedIn ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'
            ]"
            @mouseover="isLoggedIn && (hoverRating = star)" 
            @mouseleave="hoverRating = 0"
            @click="submitRating(star)">★</span>
    </div>
    <p v-if="ratingError" class="text-sm text-red-600 mt-2">{{ ratingError }}</p>
    <p v-if="!isLoggedIn" class="text-sm text-gray-400 mt-2">Prijavite se da biste ocijenili materijal.</p>
    </div>
</div>

        <!-- Preuzmi dugme -->
        <div class="mb-6">
            <DownloadButton :material-id="material.id" :full-width="true" />
        </div>

        <!-- Komentari -->
        <CommentList :material-id="material.id" />

    </div>
</template>

<script setup>
import { ref, computed,  onMounted  } from 'vue'
import DownloadButton from './DownloadButton.vue'
import CommentList from './CommentList.vue'

const BASE_URL = 'http://127.0.0.1:8000'

const props = defineProps({
    material: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['close', 'rated'])

const hoverRating = ref(0)
const selectedRating = ref(0)
const loading = ref(false)

//-----------------------------------------------------------------------------------
//Ocjenjivanje materijala - Marinela

// Lokalne kopije prosjecne ocjene i broja ocjena - osvjezavaju se nakon ocjenjivanja
const localAvgRating = ref(props.material.average_rating)
const localRatingCount = ref(props.material.rating_count)

// Moja ocjena - postavlja se kad se kartica otvori
const myRating = ref(0)

// Poruke uspjeha i greske
const ratingMessage = ref('')
const ratingError = ref('')

// Modal za promjenu ocjene  
const showChangeModal = ref(false)
const pendingStar = ref(0)

// Provjera da li je korisnik prijavljen
const isLoggedIn = computed(() => !!localStorage.getItem('token'))

// Kad se kartica otvori, provjeri da li je korisnik ocijenio ovaj materijal
onMounted(async () => {
    const response = await fetch(`${BASE_URL}/materials/${props.material.id}`)
    const data = await response.json()
    
    // Izracunaj prosjek iz ratings liste
    if (data.ratings && data.ratings.length > 0) {
        const sum = data.ratings.reduce((acc, r) => acc + r.rating, 0)
        localAvgRating.value = Math.round((sum / data.ratings.length) * 10) / 10
        localRatingCount.value = data.ratings.length
    }

    if (isLoggedIn.value) {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        const myRatingObj = data.ratings?.find(r => r.user_id === user.id)
        if (myRatingObj) {
            myRating.value = myRatingObj.rating
            selectedRating.value = myRatingObj.rating
        }
    }
})

// Slanje ocjene na backend
async function submitRating(star) {
    if (!isLoggedIn.value) return

    // Ako je vec ocijenio, prikazuje modal za promjenu  
    if (selectedRating.value > 0) {
        pendingStar.value = star
        showChangeModal.value = true
        return
    }

    selectedRating.value = star
    ratingMessage.value = ''
    ratingError.value = ''

 try {
        const token = localStorage.getItem('token')
        const response = await fetch(`${BASE_URL}/materials/${props.material.id}/rate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ rating: star, material_id: props.material.id })
        })

        if (response.status === 409) {
            ratingError.value = 'Već ste ocijenili ovaj materijal.'
            return
        }
        if (!response.ok) {
            ratingError.value = 'Greška prilikom ocjenjivanja.'
            return
        }

        ratingMessage.value = 'Hvala na ocjeni! ⭐'
        ratingError.value = ''

         // Osvjezi prosjecnu ocjenu i broj ocjena bez reloada
        const updated = await fetch(`${BASE_URL}/materials/${props.material.id}`)
        const data = await updated.json()
        localAvgRating.value = data.average_rating
        localRatingCount.value = data.rating_count
        emit('rated', props.material.id)

    } catch (err) {
        ratingError.value = 'Greška prilikom ocjenjivanja.'
    }
}

// Promjena ocjene - Marinela
async function confirmChangeRating() {
    showChangeModal.value = false
    const token = localStorage.getItem('token')
    try {
        const response = await fetch(`${BASE_URL}/materials/${props.material.id}/rate`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ rating: pendingStar.value, material_id: props.material.id })
        })
        if (!response.ok) {
            ratingError.value = 'Greška prilikom promjene ocjene.'
            return
        }
        selectedRating.value = pendingStar.value
        ratingMessage.value = 'Ocjena promijenjena! ⭐'
        ratingError.value = ''
        const updated = await fetch(`${BASE_URL}/materials/${props.material.id}`)
        const data = await updated.json()
        localAvgRating.value = data.average_rating
        localRatingCount.value = data.rating_count
        emit('rated', props.material.id)
    } catch (err) {
        ratingError.value = 'Greška prilikom promjene ocjene.'
    }
}

//----------------------------------------------------------------------------------
function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>