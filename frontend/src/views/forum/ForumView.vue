<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import ForumSidebar from '../../components/ForumSidebar.vue';
import ForumTopicCard from '../../components/ForumTopicCard.vue'; // Nova komponenta
import ForumPagination from '../../components/ForumPagination.vue'; // Nova komponenta
import { getTopics, getCategories, deleteTopic as deleteTopicApi } from '../../services/forum.js';

const teme = ref([]);
const sveKategorije = ref([]); 
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);
const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;
const search = ref("");

const ukupnoStranica = computed(() => Math.ceil(ukupnoTema.value / velicinaStranice) || 1);
const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

const trenutnaKategorija = computed(() => {
  if (!odabraniKategorijaId.value) return { name: 'General (Sve teme)', color: '#64748b' };
  return sveKategorije.value.find(c => c.id === odabraniKategorijaId.value) || { name: 'Kategorija', color: '#ff7a00' };
});

const ucitajTeme = async () => {
  isLoading.value = true;
  try {
    const data = await getTopics({
      category_id: odabraniKategorijaId.value,
      page: trenutnaStranica.value,
      per_page: velicinaStranice,
      search: search.value
    }); 
    if (data && data.items) {
      teme.value = data.items;      
      ukupnoTema.value = data.total;  
    } else if (Array.isArray(data)) {
      teme.value = data;
      ukupnoTema.value = data.length;
    }
  } catch (error) {
    console.warn("Učitavam demo podatke...");
    teme.value = [{ id: 1, title: "Dobrodošli na TK Student Hub forum", content: "...", views_count: 42, comments_count: 3, category: { name: "Opšta diskusija" }, author: { full_name: "Admin Hub" }, created_at: new Date() }];
    ukupnoTema.value = 1;
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await ucitajTeme();
  try { sveKategorije.value = await getCategories(); } catch (e) { console.error(e); }
});

watch(odabraniKategorijaId, () => { trenutnaStranica.value = 1; ucitajTeme(); });
watch(trenutnaStranica, () => ucitajTeme());

const filtrirajPoKategoriji = (id) => odabraniKategorijaId.value = id;
const applySearch = () => { trenutnaStranica.value = 1; ucitajTeme(); };

const obrisiTemu = async (temaId) => {
  if (!confirm('Da li ste sigurni da želite obrisati ovu temu?')) return;
  try {
    await deleteTopicApi(temaId);
    teme.value = teme.value.filter(t => t.id !== temaId);
    ukupnoTema.value = Math.max(0, ukupnoTema.value - 1);
  } catch (error) { alert(error.message || 'Greška.'); }
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-slate-900 p-6">
    <div class="max-w-7xl mx-auto">
      
      <div class="flex justify-between items-center mb-8 border-b border-gray-200 pb-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-800">Studentski Forum</h1>
          <p class="text-slate-500 mt-1">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>
        <router-link to="/forum/nova-tema" class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md text-sm">
          Nova tema
        </router-link>
      </div>

      <div class="flex flex-col md:flex-row gap-8 items-start">
        <div class="w-full md:w-72 flex-shrink-0">
          <ForumSidebar :aktivna-kategorija-id="odabraniKategorijaId" @kategorija-izabrana="filtrirajPoKategoriji" />
        </div>

        <div class="flex-1 w-full">
          <div class="flex flex-col justify-between min-h-[500px]">
            <div>
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <span class="px-4 py-1.5 font-extrabold text-xs rounded-full border shadow-sm transition-all duration-300"
                  :style="{ backgroundColor: trenutnaKategorija.color + '15', borderColor: trenutnaKategorija.color, color: trenutnaKategorija.color }">
                  {{ trenutnaKategorija.name }}
                </span>

                <div class="flex gap-2 w-full sm:w-80">
                  <input v-model="search" type="text" placeholder="Pretraži teme..." @keyup.enter="applySearch"
                    class="w-full border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 bg-white" />
                  <button @click="applySearch" class="bg-slate-800 text-white text-xs px-4 rounded-lg font-bold hover:bg-slate-700">Traži</button>
                </div>
              </div>

              <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
                <p class="text-slate-500 italic text-sm">Učitavanje tema...</p>
              </div>

              <div v-else-if="teme.length === 0" class="text-center py-12 bg-white rounded-xl border border-gray-200 p-8 shadow-sm">
                <p class="text-slate-500 text-sm mb-4">Trenutno nema tema u ovoj kategoriji. Započni temu!</p>
                <router-link :to="{ name: 'create-topic', query: odabraniKategorijaId ? { categoryId: odabraniKategorijaId } : {} }"
                  class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2 rounded-lg text-xs shadow-md">
                  Započni temu
                </router-link>
              </div>

              <div v-else class="space-y-4">
                <ForumTopicCard 
                  v-for="tema in teme" 
                  :key="tema.id" 
                  :tema="tema" 
                  :is-admin="isAdmin"
                  @obrisi="obrisiTemu"
                />
              </div>
            </div>

            <ForumPagination 
              v-if="teme.length > 0 && !isLoading"
              :trenutna-stranica="trenutnaStranica"
              :ukupno-stranica="ukupnoStranica"
              :prikazano-tema="teme.length"
              :ukupno-tema="ukupnoTema"
              @promijeniStranicu="(novaStr) => trenutnaStranica = novaStr"
            />

          </div>
        </div>
      </div>
    </div>
  </div>
</template>