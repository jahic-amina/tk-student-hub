<template>
    <div v-if="message" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl p-8 max-w-md w-full mx-4 text-center">
            <div class="text-5xl mb-4">{{ icon }}</div>
            <h3 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">{{ title }}</h3>
            <p class="text-gray-600 dark:text-gray-300 mb-6">{{ message }}</p>
            <button @click="$emit('close')"
                class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition">
                U redu
            </button>
        </div>
        <div class="fixed inset-0 bg-black opacity-40 dark:opacity-60 -z-10"></div>
    </div>
</template>

<script setup>
defineProps({
    message: { type: String, default: '' },
    title: { type: String, default: 'Uspješno!' },
    icon: { type: String, default: '✅' }
})
defineEmits(['close'])
</script>