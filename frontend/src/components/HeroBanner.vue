<template>
  <div class="relative bg-orange-500 text-white py-6 px-6 shadow-sm overflow-hidden">
    <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none"></div>

    <div class="relative max-w-6xl mx-auto flex items-center justify-between gap-6">
      
      <div class="flex items-center gap-4 text-left">
        <div class="shrink-0 w-12 h-12 border-2 border-white/40 bg-white/10 rounded-xl flex items-center justify-center font-black text-lg tracking-wider select-none">
          TK
        </div>
        
        <div>
          <h1 class="text-2xl lg:text-3xl font-extrabold tracking-tight leading-tight">
            Aktuelne prilike
          </h1>
          <p class="text-orange-100/80 text-xs md:text-sm mt-0.5 font-normal tracking-wide max-w-md hidden sm:block">
            Filtriraj prakse, edukacije i stipendije prema TK oblasti
          </p>
        </div>
      </div>


    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroBanner'
}
</script>