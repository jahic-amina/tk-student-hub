<script setup>
import { ref, onMounted, watch, computed, reactive } from 'vue'; // Dodat reactive
import ForumSidebar from '../../components/ForumSidebar.vue';
import ForumTopicCard from '../../components/ForumTopicCard.vue';
import ForumPagination from '../../components/ForumPagination.vue';
import ForumSearchDropdown from '../../components/ForumSearchDropdown.vue';
import ForumFilters from '../../components/ForumFilters.vue'; // Uvezena komponenta za filtere
import { getTopics, getCategories, deleteTopic as deleteTopicApi } from '../../services/forum.js';

const teme = ref([]);
const sveKategorije = ref([]); 
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);
const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;
const search = ref("");

// Reaktivno stanje za praćenje izabranih filtera iz ForumFilters komponente
const aktivniFilteri = reactive({
  sort_by: 'najnovije',
  unanswered: false,
  days_old: null
});

const ukupnoStranica = computed(() => Math.ceil(ukupnoTema.value / velicinaStranice) || 1);
const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

const trenutnaKategorija = computed(() => {
  if (!odabraniKategorijaId.value) return { name: 'General (Sve teme)', color: '#64748b' };
  return sveKategorije.value.find(c => c.id === odabraniKategorijaId.value) || { name: 'Kategorija', color: '#ff7a00' };
});

// Ažurirana funkcija koja sada šalje i parametre iz aktivniFilteri objekta u backend servis
const ucitajTeme = async () => {
  isLoading.value = true;
  try {
    const data = await getTopics({
      category_id: odabraniKategorijaId.value,
      page: trenutnaStranica.value,
      per_page: velicinaStranice,
      search: search.value,
      sort_by: aktivniFilteri.sort_by,
      unanswered: aktivniFilteri.unanswered,
      days_old: aktivniFilteri.days_old
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

// Osluškivanje promjena za kategoriju i stranicu
watch(odabraniKategorijaId, () => { trenutnaStranica.value = 1; ucitajTeme(); });
watch(trenutnaStranica, () => ucitajTeme());

const filtrirajPoKategoriji = (id) => odabraniKategorijaId.value = id;

// Rukovanje pretragom koja dolazi iz ForumSearchDropdown komponente
const handleSearchSubmitted = (query) => {
  search.value = query;
  trenutnaStranica.value = 1;
  ucitajTeme();
};

// Funkcija koja prihvata promjene filtera i ponovo povlači podatke od prve stranice
const handleFiltersChanged = (noviFilteri) => {
  aktivniFilteri.sort_by = noviFilteri.sort_by;
  aktivniFilteri.unanswered = noviFilteri.unanswered;
  aktivniFilteri.days_old = noviFilteri.days_old;
  trenutnaStranica.value = 1; // Vrati na prvu stranicu pri filtriranju
  ucitajTeme();
};

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
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-6 transition-colors duration-200">
    <div class="max-w-7xl mx-auto">
      
      <div class="flex justify-between items-center mb-8 border-b border-gray-200 dark:border-slate-800 pb-4">
        <div>
          <h1 class="text-3xl font-bold tracking-tight text-slate-800 dark:text-white">Studentski Forum</h1>
          <p class="text-slate-500 dark:text-slate-400 mt-1">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
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
              
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 w-full">
                
                <div class="flex-shrink-0">
                  <span class="px-4 py-1.5 font-extrabold text-xs rounded-full border dark:border-slate-700 shadow-sm transition-all duration-300"
                    :style="{ backgroundColor: trenutnaKategorija.color + '15', borderColor: trenutnaKategorija.color, color: trenutnaKategorija.color }">
                    {{ trenutnaKategorija.name }}
                  </span>
                </div>

                <div class="flex-1 w-full max-w-xl mx-auto flex gap-2 items-center">
                  <ForumSearchDropdown @search-submitted="handleSearchSubmitted" />
                  <ForumFilters @filters-changed="handleFiltersChanged" />
                </div>
                
                <div class="hidden md:block w-10"></div>
              </div>

              <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
                <p class="text-slate-500 dark:text-slate-400 italic text-sm">Učitavanje tema...</p>
              </div>

              <div v-else-if="teme.length === 0" class="text-center py-12 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-8 shadow-sm">
                <p class="text-slate-500 dark:text-slate-400 text-sm mb-4">Trenutno nema tema u ovoj kategoriji ili pretrazi. Započni temu!</p>
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
                  @obrisi="(id) => obrisiTemu(id)"
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