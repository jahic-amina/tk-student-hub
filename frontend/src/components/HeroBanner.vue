<template>
  <div class="relative bg-orange-500 text-white py-14 px-6 shadow-sm overflow-hidden">
    <div class="absolute inset-0 opacity-20 pointer-events-none">
      <svg width="100%" height="100%" viewBox="0 0 1200 220" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
        <line x1="200" y1="-20" x2="600" y2="240" stroke="white" stroke-width="1.5"/>
        <line x1="350" y1="-20" x2="750" y2="240" stroke="white" stroke-width="1.5"/>
        <line x1="500" y1="-20" x2="100" y2="240" stroke="white" stroke-width="1.5"/>
        <line x1="700" y1="-20" x2="300" y2="240" stroke="white" stroke-width="1.5"/>
        <line x1="900" y1="-20" x2="1300" y2="240" stroke="white" stroke-width="1.5"/>
        <line x1="1050" y1="-20" x2="650" y2="240" stroke="white" stroke-width="1.5"/>
      </svg>
    </div>

    <div class="relative max-w-6xl mx-auto flex flex-col items-center justify-center text-center">
      <div class="flex flex-col items-center gap-3">
        <div class="w-16 h-16 border-2 border-white/40 bg-white/10 rounded-2xl flex items-center justify-center font-black text-xl tracking-wider select-none">
          TK
        </div>
        <h1 class="text-4xl lg:text-5xl font-extrabold tracking-tight mt-1">
          Aktuelne prilike
        </h1>
      </div>
      <p class="text-orange-100/90 text-base md:text-lg mt-3 font-normal tracking-wide max-w-xl">
        Filtriraj prakse, edukacije i stipendije prema TK oblasti
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroBanner'
}
</script>