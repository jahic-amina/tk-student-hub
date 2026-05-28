<template>
    <div class="border rounded-xl p-4 shadow-sm bg-white">
        <div class="flex items-center justify-between mb-2">
            <span class="font-semibold text-gray-800">{{ comment.user?.full_name || 'Nepoznato' }}</span>
            <span class="text-xs text-gray-400">{{ relativnoVrijeme(comment.created_at) }}</span>
        </div>
        <p class="text-gray-600 text-sm leading-relaxed">{{ comment.content }}</p>
    </div>
</template>

<script setup>
defineProps({
    comment: {
        type: Object,
        required: true
    }
})

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