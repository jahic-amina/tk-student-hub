<template>
  <div class="bg-white rounded-xl shadow p-6 mb-6">
    <div class="flex items-start gap-6">
      <div class="relative flex-shrink-0">
        <div class="w-20 h-20 rounded-full bg-gray-300 flex items-center justify-center overflow-hidden">
          <img
            v-if="profile.profilna_slika_url"
            :src="`http://localhost:8000${profile.profilna_slika_url}`"
            class="w-full h-full object-cover"/>
          <span v-else class="text-white text-2xl font-bold">{{ initials }}</span>
        </div>
        <div class="absolute bottom-0 right-0 bg-primary rounded-full w-6 h-6 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
      </div>