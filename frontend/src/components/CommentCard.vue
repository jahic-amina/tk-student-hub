<template>
    <div class="border rounded-xl p-4 shadow-sm bg-white">
        <div class="flex items-center justify-between mb-2">
            <span class="font-semibold text-gray-800">{{ comment.user?.full_name || 'Nepoznato' }}</span>
            <div class="flex items-center gap-3">
                <span class="text-xs text-gray-400">{{ relativnoVrijeme(comment.created_at) }}</span>
                <button
                    v-if="mozeBrisati"
                    @click="otvoriModal"
                    class="text-xs text-red-400 hover:text-red-600 transition"
                >
                    Obriši
                </button>
            </div>
        </div>
        <p class="text-gray-600 text-sm leading-relaxed">{{ comment.content }}</p>

        <!-- Toast -->
        <div v-if="toastPoruka" class="mt-2 text-xs text-green-500">{{ toastPoruka }}</div>

        <!-- Confirm Modal -->
        <ConfirmModal
            v-if="prikaziModal"
            naslov="Brisanje komentara"
            poruka="Jeste li sigurni da želite obrisati ovaj komentar?"
            :onConfirm="obrisi"
            :onCancel="zatvoriModal"
        />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ConfirmModal from './ConfirmModal.vue'
import { deleteComment } from '../services/api.js'

const props = defineProps({
    comment: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['obrisan'])

const prikaziModal = ref(false)
const toastPoruka = ref('')

function getUserIdIzTokena() {
    const token = localStorage.getItem('token')
    if (!token) return null
    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return parseInt(payload.sub)
    } catch {
        return null
    }
}

function getRolaIzTokena() {
    const token = localStorage.getItem('token')
    if (!token) return ''
    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return payload.role || ''
    } catch {
        return ''
    }
}

const trenutniUserId = getUserIdIzTokena()
const trenutnaRola = getRolaIzTokena()

const mozeBrisati = computed(() => {
    return props.comment.user_id === trenutniUserId || trenutnaRola === 'admin'
})

function otvoriModal() {
    prikaziModal.value = true
}

function zatvoriModal() {
    prikaziModal.value = false
}

async function obrisi() {
    try {
        await deleteComment(props.comment.material_id, props.comment.id)
        prikaziModal.value = false
        toastPoruka.value = 'Komentar uspješno obrisan.'
        setTimeout(() => emit('obrisan', props.comment.id), 1000)
    } catch (e) {
        prikaziModal.value = false
        toastPoruka.value = 'Greška pri brisanju komentara.'
    }
}

function relativnoVrijeme(dateStr) {
    if (!dateStr) return 'N/A'
    const sada = new Date()
    const utcStr = dateStr.endsWith('Z') ? dateStr : dateStr + 'Z'
    const datum = new Date(utcStr)
    const razlikaMs = sada - datum
    const razlikaSek = Math.floor(razlikaMs / 1000)
    const razlikaMin = Math.floor(razlikaSek / 60)
    const razlikaSati = Math.floor(razlikaMin / 60)
    const razlikaDana = Math.floor(razlikaSati / 24)

    if (razlikaSek < 60) return 'Upravo sada'
    if (razlikaMin < 60) return `Prije ${razlikaMin} ${razlikaMin === 1 ? 'minutu' : 'minuta'}`
    if (razlikaSati < 24) return `Prije ${razlikaSati} ${razlikaSati === 1 ? 'sat' : 'sati'}`
    if (razlikaDana === 1) return 'Jučer'
    if (razlikaDana < 7) return `Prije ${razlikaDana} dana`

    // Stariji komentari — standardni format DD.MM.YYYY.
    return datum.toLocaleDateString('bs-BA')
}
</script>