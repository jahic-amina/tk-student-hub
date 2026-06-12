<template>
  <div class="w-full flex flex-col gap-5 select-none animate-in fade-in duration-300">
    
    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm transition-all hover:shadow-md">
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-amber-500">⭐</span>
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          Preporučene teme
        </h3>
      </div>

      <div class="space-y-3.5">
        <div v-for="i in 3" :key="i" class="group cursor-pointer">
          <div class="text-xs font-bold text-slate-800 dark:text-slate-200 group-hover:text-orange-500 transition-colors line-clamp-2 leading-snug">
            {{ i === 1 ? 'Kako se spremiti za ispit iz Naprednih Baza Podataka?' : i === 2 ? 'Iskustva sa praksom u lokalnim IT firmama (Sarajevo/Tuzla)' : 'Materijali i skripte za III godinu - Linkovi' }}
          </div>
          
          <div class="flex items-center gap-3 mt-1.5 text-[10px] text-slate-400 dark:text-slate-500 font-medium">
            <span class="flex items-center gap-1">👁️ {{ 150 * i }} pregleda</span>
            <span class="flex items-center gap-1">💬 {{ 4 * i }} odgovora</span>
            <span class="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 font-semibold">
              {{ i === 1 ? 'Ispiti' : i === 2 ? 'Praksa' : 'Materijali' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm">
      <div class="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-blue-500">📊</span>
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          Statistika zajednice
        </h3>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="bg-gray-50 dark:bg-slate-700/40 p-2.5 rounded-xl border border-gray-100 dark:border-slate-700 text-center">
          <div class="text-sm font-black text-slate-800 dark:text-white">1,240</div>
          <div class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider mt-0.5">Članova</div>
        </div>
        <div class="bg-gray-50 dark:bg-slate-700/40 p-2.5 rounded-xl border border-gray-100 dark:border-slate-700 text-center">
          <div class="text-sm font-black text-slate-800 dark:text-white">4,821</div>
          <div class="text-[10px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider mt-0.5">Teme</div>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-slate-700 p-4 shadow-sm">
      <div class="flex items-center gap-2 mb-3 pb-2 border-b border-gray-100 dark:border-slate-700">
        <span class="text-base text-emerald-500">🟢</span>
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          Aktivne kolege
        </h3>
      </div>

      <div class="flex flex-wrap gap-2 pt-1">
        <div v-for="user in ['amar', 'tarik', 'amina', 'elma', 'kenan']" :key="user" class="relative group cursor-pointer">
          <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-400 to-amber-500 text-white font-bold text-xs flex items-center justify-center uppercase border-2 border-white dark:border-slate-800 shadow-sm">
            {{ user.substring(0, 2) }}
          </div>
          <span class="absolute bottom-0 right-0 block h-2 w-2 rounded-full bg-emerald-500 ring-2 ring-white dark:ring-slate-800"></span>
          
          <span class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1.5 hidden group-hover:block bg-slate-900 text-white text-[10px] px-2 py-0.5 rounded shadow-md whitespace-nowrap z-30">
            {{ user }}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
// Trenutno čist vizuelni mockup, logika za prihvatanje pravih podataka ide kasnije
</script>