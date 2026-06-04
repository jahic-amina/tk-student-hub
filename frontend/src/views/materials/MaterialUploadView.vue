<template>
    <div class="max-w-2xl mx-auto py-8 px-4">
        <!-- Nazad dugme -->
        <button @click="$router.push('/materials')"
            class="inline-flex items-center gap-2 bg-primary text-white font-semibold px-5 py-2.5 rounded-lg shadow-sm hover:bg-primary/90 active:scale-[0.98] transition mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>NAZAD</span>
        </button>

       <!-- Forma za upload — prikazuje se sa dugmetom uspjeha -->
       <MaterialUploadForm :direct-show="true" @submit="handleSubmit" @success="handleSuccess" />
    </div>
</template>

<script setup>

// Stranica za dodavanje novog materijala
import { useRouter } from 'vue-router'
import MaterialUploadForm from '../../components/MaterialUploadForm.vue'

const router = useRouter()

// Nakon što korisnik klikne "U redu" na success modalu, preusmjerava na listu
function handleSuccess() {
    router.push('/materials')
}

// handleSubmit samo čeka na success event
function handleSubmit() {
}
</script>