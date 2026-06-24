<script setup>
const props = defineProps({
  username: {
    type: String,
    required: true
  }
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 p-6">
    <div class="max-w-3xl mx-auto bg-white dark:bg-slate-800 rounded-xl shadow p-6">
      <h1 class="text-2xl font-bold text-slate-800 dark:text-white">
        Profil korisnika
      </h1>

      <p class="mt-2 text-slate-600 dark:text-slate-300">
        @{{ username }}
      </p>
    </div>
  </div>
</template>