<template>
    <div class="flex flex-col sm:flex-row sm:items-center justify-between border rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition gap-4"
        @click="$emit('click', material.id)">
        <div class="flex items-start gap-4">
            <div class="bg-red-100 text-red-500 p-3 rounded-lg shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide lucide-file-text w-8 h-8 text-destructive"
                    data-fg-d3bl92="0.8:79.665:/src/app/App.tsx:474:21:17880:49:e:FileText::::::B1i5"
                    data-fgid-d3bl92=":r22:">
                    <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
                    <path d="M14 2v4a2 2 0 0 0 2 2h4"></path>
                    <path d="M10 9H8"></path>
                    <path d="M16 13H8"></path>
                    <path d="M16 17H8"></path>
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
                    Ko je postavio: {{ material.user.full_name }} &nbsp;
                    Datum postavljanja: {{ formatDate(material.created_at) }}
                </p>
            </div>
        </div>

        <div class="flex sm:flex-col md:flex-row items-center gap-4 sm:gap-2 md:gap-6 sm:ml-auto">
            <div class="text-left sm:text-right">
                <div class="flex items-center gap-1">
                    <span v-for="star in 5" :key="star" class="text-yellow-400 text-lg">
                        {{ star <= Math.round(material.average_rating) ? '★' : '☆' }} </span>
                            <span class="text-sm text-gray-500">({{ material.rating_count }})</span>
                </div>
                <p class="text-sm text-gray-500 mt-2 flex gap-2 items-center"><svg xmlns="http://www.w3.org/2000/svg"
                        width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-download w-4 h-4"
                        data-fg-d3bl133="0.8:79.665:/src/app/App.tsx:544:25:21266:32:e:Download::::::yh6"
                        data-fgid-d3bl133=":r2p:">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" x2="12" y1="15" y2="3"></line>
                    </svg> {{ material.number_of_downloads }} preuzimanja</p>
            </div>

            <div class="flex sm:flex-row gap-2">
                <button v-if="isAdmin"
                    class="flex items-center gap-1 bg-red-100 text-red-500 px-3 py-1 rounded text-sm hover:bg-red-200"
                    @click.stop>
                    🗑 Obriši
                </button>
                <button class="flex items-center gap-1 border px-3 py-1 rounded text-sm hover:bg-gray-100 bg-gray-200 "
                    @click.stop>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-download w-4 h-4"
                        data-fg-d3bl133="0.8:79.665:/src/app/App.tsx:544:25:21266:32:e:Download::::::yh6"
                        data-fgid-d3bl133=":r2p:">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" x2="12" y1="15" y2="3"></line>
                    </svg>
                    PREUZMI
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    material: {
        type: Object,
        required: true
    }
})

defineEmits(['click'])

function formatDate(dateStr) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}
</script>