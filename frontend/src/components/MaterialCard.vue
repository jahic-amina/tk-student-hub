<template>
    <div
        class="flex flex-col sm:flex-row sm:items-center justify-between border rounded-xl p-4 shadow-sm hover:shadow-md transition gap-4">
        <div class="flex items-start gap-4 flex-1 cursor-pointer" @click="$emit('click', material.id)">
            <div class="bg-red-100 text-red-500 p-3 rounded-lg shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide lucide-file-text w-8 h-8 text-destructive">
                    <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
                    <path d="M14 2v4a2 2 0 0 0 2 2h4"></path>
                    <path d="M10 9H8"></path>
                    <path d="M16 13H8"></path>
                    <path d="M16 17H8"></path>
                </svg>
            </div>
            <div>
                <p class="font-semibold text-gray-800">{{ material.title }}</p>
                <p class="text-sm text-gray-500">{{ material.description }}</p>
                <p class="text-xs text-gray-400 mt-1">
                    Ko je postavio: {{ material.user?.full_name || 'Nepoznato' }} &nbsp;
                    Datum postavljanja: {{ formatDate(material.created_at) }}
                </p>
            </div>
        </div>

        <div class="flex sm:flex-col md:flex-row items-center gap-4 sm:gap-2 md:gap-6 sm:ml-auto min-w-[150px]">
            <div class="text-left sm:text-right w-full">
                <div class="flex items-center sm:justify-end gap-1">
                    <span v-for="star in 5" :key="star" class="text-yellow-400 text-lg">
                        {{ star <= Math.round(material.average_rating || 0) ? '★' : '☆' }} </span>
                            <span class="text-sm text-gray-500">({{ material.rating_count || 0 }})</span>
                </div>
                <div>
                    <p class="text-sm text-gray-500 mt-2">Broj preuzimanja: {{ material.number_of_downloads || 0 }}</p>
                </div>
            </div>
            <div class="flex flex-col gap-2 w-full items-stretch" @click.stop>
                <template v-if="pending">
                    <button @click="$emit('approve', material.id)"
                        class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2">
                        ✓ Odobri
                    </button>
                    <button @click="$emit('reject', material.id)"
                        class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2">
                        ✕ Odbij
                    </button>
                </template>
                <template v-else>
                    <DownloadButton :material-id="material.id" class="w-full" />
                    <DeleteMaterialButton :material="material" @deleted="$emit('deleted', material.id)" @click.stop
                        class="w-full" />
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import DownloadButton from './DownloadButton.vue'
import DeleteMaterialButton from './DeleteMaterialButton.vue'

defineProps({
    material: {
        type: Object,
    },
    pending: {
        type: Boolean,
        default: false
    }

})

defineEmits(['click', 'deleted', 'approve', 'reject'])

function formatDate(dateStr) {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>