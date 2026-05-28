<template>
    <div class="mt-4">
        <!-- Neprijavljen korisnik -->
        <div v-if="!prijavljen" class="text-sm text-gray-500 italic">
            <router-link to="/login" class="text-primary font-medium hover:underline">Prijavi se</router-link>
            da bi mogao komentarisati.
        </div>

        <!-- Prijavljen korisnik -->
        <div v-else>
            <textarea
                v-model="tekst"
                placeholder="Napišite komentar..."
                rows="3"
                maxlength="500"
                class="w-full border rounded-lg p-3 text-sm text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <div class="flex justify-between items-center mt-1">
                <span class="text-xs text-gray-400">{{ preostaloKaraktera }} / 500</span>
                <button
                    @click="objavi"
                    :disabled="!validan || slanje"
                    class="bg-primary text-white px-4 py-1.5 rounded-lg text-sm transition hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {{ slanje ? 'Slanje...' : 'Objavi' }}
                </button>
            </div>
            <p v-if="greska" class="text-red-400 text-xs mt-1">{{ greska }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { postComment } from '../services/api.js'

const props = defineProps({
    materialId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['komentar-dodan'])

const tekst = ref('')
const slanje = ref(false)
const greska = ref('')
const prijavljen = !!localStorage.getItem('token')

const preostaloKaraktera = computed(() => tekst.value.length)
const validan = computed(() => tekst.value.trim().length >= 1 && tekst.value.trim().length <= 500)

async function objavi() {
    if (!validan.value) return
    slanje.value = true
    greska.value = ''
    try {
        const noviKomentar = await postComment(props.materialId, tekst.value.trim())
        emit('komentar-dodan', noviKomentar)
        tekst.value = ''
    } catch (e) {
        greska.value = 'Greška pri slanju komentara. Pokušajte ponovo.'
    } finally {
        slanje.value = false
    }
}
</script>