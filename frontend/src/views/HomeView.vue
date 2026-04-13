<template>
  <div class="text-center py-20">
    <h1 class="text-4xl font-bold text-primary mb-4">
      Dobrodošli u TK Student Hub
    </h1>
    <p class="text-lg text-gray-500 max-w-xl mx-auto mb-8">
      Platforma za studente telekomunikacija — pronađi materijale, prijavi se na događaje, pristupi resursima i poveži se sa kolegama.
    </p>
    <div class="flex justify-center gap-4">
      <router-link to="/register" class="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary/90 transition font-medium">
        Pridruži se
      </router-link>
      <router-link to="/workshops" class="border border-primary text-primary px-6 py-3 rounded-lg hover:bg-primary hover:text-white transition font-medium">
        Pregledaj događaje
      </router-link>
    </div>
  </div>
</template>