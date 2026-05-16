<template>
  <div>
    
    <button
      @click="showForm = true"
      class="bg-primary text-white px-6 py-3 rounded-lg font-semibold
             hover:bg-orange-600 hover:shadow-md transition-all duration-200"
    >
      + DODAJTE MATERIJAL
    </button>

    
    <div v-if="showForm" class="bg-white rounded-lg shadow p-6 mt-6">
      
      <!-- Naslov -->
      <h2 class="text-xl font-bold mb-6">Dodajte novi materijal</h2>

      <!-- Marinela dodaje polja ovdje -->
      <slot />

      <!-- NEDOVRŠENO:poruka uspjeha -->
      <p v-if="successMessage" class="text-green-600 font-medium mb-4">
        {{ successMessage }}
      </p>

      <!-- NEDOVRŠENO: greška -->
      <p v-if="uploadError" class="text-red-500 font-medium mb-4">
        {{ uploadError }}
      </p>

      
      <div class="flex gap-3 mt-6">
        <button
          @click="$emit('submit')"
          :disabled="isSubmitting"
          class="bg-primary text-white px-6 py-2 rounded-lg font-semibold
                 hover:bg-orange-600 transition-all duration-200 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Slanje...' : '+Dodaj materijal' }}
        </button>
        <button
          @click="showForm = false"
          class="border border-gray-300 px-6 py-2 rounded-lg
                 hover:bg-gray-50 transition-all duration-200"
        >
          Odustani
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showForm = ref(false)
const successMessage = ref('')
const uploadError = ref('')
const isSubmitting = ref(false)
</script>