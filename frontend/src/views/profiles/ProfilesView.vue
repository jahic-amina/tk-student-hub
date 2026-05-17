<template>
  <div class="max-w-4xl mx-auto py-8 px-4">

    <div v-if="loading" class="text-center py-20 text-gray-400"> Učitavanje...</div>

    <div v-else-if="error" class="bg-red-100 text-red-600 p-4 rounded-lg">
       {{ error }} </div>
    
    <div v-else-if="profile">
      <UserProfileCard :profile="profile" />
      <div class="bg-white rounded-xl shadow p-6 mb-6">
        <h2 class="text-lg font-bold mb-3">O meni</h2>
        <p class="text-gray-600 text-sm">{{ profile.biografija || 'Nije unesena biografija.' }}</p>
      </div>

      <div class="grid grid-cols-2 gap-6">
       <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-lg font-bold mb-4">Trenutne prakse</h2>
          <p class="text-gray-400 text-sm">Nema trenutnih praksi.</p>
        </div>

        <div class="bg-white rounded-xl shadow p-6">
          <h2 class="text-lg font-bold mb-4">Nedavna aktivnost</h2>
          <p class="text-gray-400 text-sm">Nema nedavne aktivnosti.</p>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import UserProfileCard from '../../components/UserProfileCard.vue'
import { getMyProfile } from '../../services/api.js'

const profile = ref(null)
const loading = ref(false)
const error = ref(null)
const token = localStorage.getItem('token')

async function fetchProfile() {
  loading.value = true
  error.value = null
  try {
    const data = await getMyProfile(token)
    profile.value = data
  } catch (err) {
    error.value = "Greška pri učitavanju profila. Molimo pokušajte ponovo."
  } finally {
    loading.value = false
  }
}
onMounted(fetchProfile)
</script>

