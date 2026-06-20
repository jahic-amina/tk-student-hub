<template>
  <div class="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-[10px] overflow-hidden flex-shrink-0">
    <img 
      v-if="avatarUrl" 
      :src="fullAvatarUrl" 
      class="w-full h-full object-cover" 
      alt="Avatar"
      @error="handleImgError"
    />
    <span v-else>{{ initials }}</span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  author: {
    type: Object,
    required: true
  }
})

const avatarUrl = ref(null)
const hasError = ref(false)

// Računanje inicijala
const initials = computed(() => {
  if (!props.author?.full_name) return '?'
  return props.author.full_name
    .split(' ')
    .map(part => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()
})

// Pametno spajanje URL-a (da se ne dupla http://localhost:8000 ako backend nekad vrati puni link)
const fullAvatarUrl = computed(() => {
  if (!avatarUrl.value) return ''
  if (avatarUrl.value.startsWith('http://') || avatarUrl.value.startsWith('https://')) {
    return avatarUrl.value
  }
  return `http://localhost:8000${avatarUrl.value}`
})

// Provjera i dobavljanje slike sa javnog profila uz slanje tokena
async function checkAndFetchAvatar() {
  // Ako backend unutar topica već šalje url, iskoristi ga odmah
  if (props.author?.profilna_slika_url) {
    avatarUrl.value = props.author.profilna_slika_url
    return
  }

  // Ako ne šalje, a imamo ID autora, pitamo rutu ali ovaj put sa tokenom!
  if (props.author?.id && !hasError.value) {
    try {
      // Čupamo token iz localStorage-a isto kao u glavnoj komponenti
      const token = localStorage.getItem('token') || localStorage.getItem('access_token')
      
      const config = {}
      if (token) {
        config.headers = { Authorization: `Bearer ${token}` }
      }

      const res = await axios.get(`http://127.0.0.1:8000/profiles/${props.author.id}/public`, config)
      
      if (res.data && res.data.profilna_slika_url) {
        avatarUrl.value = res.data.profilna_slika_url
      }
    } catch (err) {
      console.error("Nije moguće učitati avatar za korisnika:", props.author.id)
    }
  }
}

// Ako slika baci 404, vrati na inicijale
function handleImgError() {
  avatarUrl.value = null
  hasError.value = true
}

onMounted(() => {
  checkAndFetchAvatar()
})

// Prati izmjene ako se komponenta ponovo iskoristi u listi (npr. pri promjeni rute)
watch(() => props.author, () => {
  avatarUrl.value = null // Resetuj prije nove provjere
  hasError.value = false
  checkAndFetchAvatar()
}, { deep: true })
</script>