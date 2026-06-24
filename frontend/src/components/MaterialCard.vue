<template>
    <div
    class="relative flex flex-col sm:flex-row sm:items-center justify-between border rounded-xl p-4 shadow-sm hover:shadow-md transition gap-4 dark:bg-slate-800 dark:border-slate-700"
>
       <button 
    v-if="userRole !== 'admin'"
    type="button"
    @click.stop="$emit('toggle-bookmark', material.id)"
    class="absolute top-0 right-0 z-10 group"
>
    <div 
        :class="[
            'w-8 h-10 transition-all duration-300 flex items-center justify-center rounded-tr-xl',
            material.is_bookmarked ? 'bg-amber-400 shadow-md' : 'bg-gray-200 hover:bg-gray-300'
        ]"
        style="clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 50% 80%, 0% 100%);"
    >
        <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="16" height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            :stroke="material.is_bookmarked ? 'white' : '#9ca3af'" 
            stroke-width="3"
        >
            <path d="M19 21l-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"></path>
        </svg>
    </div>
</button>
        <div class="flex flex-col sm:flex-row items-start gap-4 flex-1 cursor-pointer min-w-0" @click="$emit('click', material.id)">
        <div :class="['p-1 rounded-lg shrink-0 overflow-hidden w-20 h-24 flex items-center justify-center', material.thumbnail_path ? 'bg-gray-100' : 'bg-red-100 text-red-500']">
    <img 
    v-if="material.thumbnail_path" 
    :src="`http://127.0.0.1:8000/thumbnails/${material.thumbnail_path.split('/').pop()}`"
    class="w-full h-full object-contain rounded"
    alt="thumbnail"
    />
    <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        class="lucide lucide-file-text w-8 h-8 text-destructive">
        <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"></path>
        <path d="M14 2v4a2 2 0 0 0 2 2h4"></path>
        <path d="M10 9H8"></path>
        <path d="M16 13H8"></path>
        <path d="M16 17H8"></path>
    </svg>
</div>
            
         <div class="min-w-0 overflow-hidden flex-1">
   <p class="font-semibold text-gray-800 dark:text-slate-100 truncate">{{ material.title }}</p>
   <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Postavio: {{ material.user?.full_name || 'Nepoznato' }}</p>
   <p class="text-sm text-gray-500 dark:text-slate-400">Datum postavljanja: {{ formatDate(material.created_at) }}</p>
   <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">{{ material.subject?.name }}</p>
 </div>
    <div class="flex flex-col items-start sm:items-center justify-center shrink-0 sm:px-4">
    <div class="flex items-center gap-1">
        <span v-for="star in 5" :key="star" class="text-yellow-400 text-lg">
            {{ star <= Math.round(material.average_rating || 0) ? '★' : '☆' }}
        </span>
        <span class="text-sm text-gray-500 dark:text-slate-400">({{ material.rating_count || 0 }})</span>
    </div>
    <p class="text-sm text-gray-500 dark:text-slate-400 mt-1">Broj preuzimanja: {{ material.number_of_downloads || 0 }}</p>
</div>
    </div>
        <div class="flex flex-col gap-2 shrink-0 mr-8" @click.stop>
                <template v-if="pending">
                <p v-if="!hasDownloaded" class="text-xs text-gray-500 dark:text-slate-400 mb-1 w-32">
                    Preuzmite materijal prije odobrenja i odbijanja.
                </p>
                <button @click="$emit('approve', material.id)" :disabled="!hasDownloaded"
                    class="w-32 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                    ✓ Odobri
                </button>
                <button @click="$emit('reject', material.id)" :disabled="!hasDownloaded"
                    class="w-32 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                    ✕ Odbij
                </button>
            </template>
                <template v-else>
                   <DownloadButton :material-id="material.id" class="w-full" @downloaded="$emit('downloaded', material.id)" />
                   <DeleteMaterialButton v-if="userRole === 'admin' || material.user?.id === currentUserId" :material="material" @deleted="$emit('deleted', material.id)" @click.stop class="w-full" />
                </template>
            </div>
    </div>

</template>

<script setup>
import DownloadButton from './DownloadButton.vue'
import DeleteMaterialButton from './DeleteMaterialButton.vue'
const currentUserId = Number(localStorage.getItem('user_id'))

defineProps({
    material: {
        type: Object,
    },
    pending: {
        type: Boolean,
        default: false
    },
    userRole: {
        type: String,
        default: 'member'
    },
    hasDownloaded: {
        type: Boolean,
        default: false
    }
})

defineEmits(['click', 'deleted', 'approve', 'reject', 'toggle-bookmark', 'downloaded' ])

function formatDate(dateStr) {
    if (!dateStr) return 'N/A'
    const date = new Date(dateStr)
    return date.toLocaleDateString('bs-BA')
}


</script>