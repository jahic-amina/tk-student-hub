<template>
    <!-- Overlay -->
    <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center" @click.self="odustani">
        <!-- Modal -->
       <div class="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 w-[90%] sm:w-[400px]">
        <h3 class="text-lg font-bold text-gray-800 dark:text-slate-100 mb-2">{{ naslov }}</h3>
         <p class="text-sm text-gray-600 dark:text-slate-300 mb-6">{{ poruka }}</p>
          <div class="flex justify-end gap-3">
                <button
                    @click="odustani"
                    class="px-4 py-1.5 rounded-lg border dark:border-slate-600 text-gray-600 dark:text-slate-200 hover:bg-gray-100 dark:hover:bg-slate-700 transition text-sm"
                >
                    Odustani
                </button>
               <button
                @click="potvrdi"
                class="px-4 py-1.5 rounded-lg bg-red-500 text-white hover:bg-red-600 transition text-sm"
            >
                Obriši
            </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
    naslov: {
        type: String,
        default: 'Potvrda'
    },
    poruka: {
        type: String,
        required: true
    },
    onConfirm: {
        type: Function,
        required: true
    },
    onCancel: {
        type: Function,
        required: true
    }
})

function potvrdi() {
    props.onConfirm()
}

function odustani() {
    props.onCancel()
}

function handleEsc(e) {
    if (e.key === 'Escape') odustani()
}

onMounted(() => window.addEventListener('keydown', handleEsc))
onUnmounted(() => window.removeEventListener('keydown', handleEsc))
</script>