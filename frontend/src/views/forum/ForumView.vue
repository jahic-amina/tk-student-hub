<script setup>
import { ref, onMounted, watch, computed, reactive } from 'vue';
import ForumSidebar from '../../components/ForumSidebar.vue';
import ForumTopicCard from '../../components/ForumTopicCard.vue';
import ForumPagination from '../../components/ForumPagination.vue'; 
import ForumSearchDropdown from '../../components/ForumSearchDropdown.vue';
import ForumFilters from '../../components/ForumFilters.vue';
import { 
  getTopics, 
  getCategories, 
  deleteTopic as deleteTopicApi, 
  getActiveAnnouncements, 
  getActiveReports, 
  handleReportAction 
} from '../../services/forum.js';

const teme = ref([]);
const sveKategorije = ref([]); 
const isLoading = ref(true);
const odabraniKategorijaId = ref(null);
const trenutnaStranica = ref(1);
const ukupnoTema = ref(0);
const velicinaStranice = 5;
const search = ref("");
const announcements = ref([]);
const prikaziPrijave = ref(false); 
const svePrijave = ref([]);

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

// Funkcija koja šalje i parametre iz aktivniFilteri objekta u backend servis
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

const ucitajPrijave = async () => {
  isLoading.value = true;
  try {
    svePrijave.value = await getActiveReports();
  } catch (error) {
    console.error("Greška pri učitavanju prijava:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await ucitajTeme();
  try { sveKategorije.value = await getCategories(); } catch (e) { console.error(e); }
  try { announcements.value = await getActiveAnnouncements(); } catch (e) { console.error(e); }
});

// Osluškivanje promjena za kategoriju i stranicu (Spojeno u čistu logiku)
watch(odabraniKategorijaId, () => { 
  prikaziPrijave.value = false;
  trenutnaStranica.value = 1; 
  ucitajTeme(); 
});

watch(trenutnaStranica, () => {
  if (!prikaziPrijave.value) {
    ucitajTeme();
  }
});

const filtrirajPoKategoriji = (id) => odabraniKategorijaId.value = id;

// Rukovanje pretragom koja dolazi iz ForumSearchDropdown komponente
const handleSearchSubmitted = (query) => {
  search.value = query;
  trenutnaStranica.value = 1;
  ucitajTeme();
};

// Funkcija koja prihvata promjene filtera i ponovo povlači podatke
const handleFiltersChanged = (noviFilteri) => {
  aktivniFilteri.sort_by = noviFilteri.sort_by;
  aktivniFilteri.unanswered = noviFilteri.unanswered;
  aktivniFilteri.days_old = noviFilteri.days_old;
  trenutnaStranica.value = 1; 
  ucitajTeme();
};

const obrisiTemu = async (temaId) => {
  if (!confirm('Da li ste sigurni da želite obrisati ovu temu?')) return;
  try {
    await deleteTopicApi(temaId);
    
    if (prikaziPrijave.value) {
      const uvezanaPrijava = svePrijave.value.find(p => p.topic && p.topic.id === temaId);
      if (uvezanaPrijava) {
        await handleReportAction(uvezanaPrijava.report_id, 'resolve');
        svePrijave.value = svePrijave.value.filter(p => p.topic && p.topic.id !== temaId);
      }
    } else {
      teme.value = teme.value.filter(t => t.id !== temaId);
      ukupnoTema.value = Math.max(0, ukupnoTema.value - 1);
    }
    alert('Tema uspješno obrisana.');
  } catch (error) { 
    alert(error.message || 'Greška pri brisanju teme.'); 
  }
};

const toggleModPrijava = (status) => {
  prikaziPrijave.value = status;
  trenutnaStranica.value = 1;
  if (status === true) {
    ucitajPrijave();
  } else {
    ucitajTeme();
  }
};

const procesuirajPrijavu = async (reportId, akcija) => {
  try {
    await handleReportAction(reportId, akcija);
    svePrijave.value = svePrijave.value.filter(p => p.report_id !== reportId);
    alert(akcija === 'dismiss' ? "Prijava uspješno odbačena." : "Prijava označena kao riješena.");
  } catch (error) {
    alert("Greška: " + error.message);
  }
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
        <router-link v-if="!isAdmin" to="/forum/nova-tema" class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-6 py-2.5 rounded-lg transition-colors shadow-md text-sm">
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
              
              <div v-if="announcements && announcements.length > 0" class="mb-6 space-y-3">
                <div v-for="ann in announcements" :key="ann.id" class="bg-red-50 dark:bg-red-950/20 border-l-4 border-red-500 p-4 rounded-xl shadow-sm flex items-start gap-3">
                  <span class="text-red-500 text-xl">📢</span>
                  <p class="text-red-800 dark:text-red-200 font-medium text-sm">{{ ann.content }}</p>
                </div>
              </div>

              <div v-if="isAdmin" class="flex gap-2 mb-5 bg-slate-200/60 dark:bg-slate-800 p-1 rounded-xl border border-slate-300/40 dark:border-slate-700 max-w-xs">
                <button 
                  @click="toggleModPrijava(false)"
                  :class="!prikaziPrijave ? 'bg-white dark:bg-slate-700 text-slate-800 dark:text-white shadow-sm font-semibold' : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'"
                  class="flex-1 py-1.5 px-3 rounded-lg text-xs transition-all"
                >
                  Sve teme
                </button>
                <button 
                  @click="toggleModPrijava(true)"
                  :class="prikaziPrijave ? 'bg-red-500 text-white shadow-sm font-bold' : 'text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30'"
                  class="flex-1 py-1.5 px-3 rounded-lg text-xs transition-all flex items-center justify-center gap-1"
                >
                  ⚠️ Prijave
                </button>
              </div>

              <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 w-full">
                <div class="flex-shrink-0">
                  <span class="px-4 py-1.5 font-extrabold text-xs rounded-full border dark:border-slate-700 shadow-sm transition-all duration-300"
                    :style="{ backgroundColor: trenutnaKategorija.color + '15', borderColor: trenutnaKategorija.color, color: trenutnaKategorija.color }">
                    {{ prikaziPrijave ? 'Moderacija (Prijavljeni sadržaj)' : trenutnaKategorija.name }}
                  </span>
                </div>

                <div v-if="!prikaziPrijave" class="flex-1 w-full max-w-xl mx-auto flex gap-2 items-center">
                  <ForumSearchDropdown @search-submitted="handleSearchSubmitted" />
                  <ForumFilters @filters-changed="handleFiltersChanged" />
                </div>
                
                <div class="hidden md:block w-10"></div>
              </div>

              <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#ff7a00] mb-4"></div>
                <p class="text-slate-500 dark:text-slate-400 italic text-sm">Učitavanje podataka...</p>
              </div>

              <div v-else-if="prikaziPrijave" class="space-y-4">
                <div v-if="svePrijave.length === 0" class="text-center py-12 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-8 shadow-sm">
                  <p class="text-emerald-600 dark:text-emerald-400 font-medium text-sm">🎉 Odlično! Trenutno nema neriješenih prijava korisnika.</p>
                </div>
                
                <div 
                  v-for="prijava in svePrijave" 
                  :key="prijava.report_id" 
                  class="bg-red-50/40 dark:bg-red-950/10 border border-red-200/80 dark:border-red-900/50 rounded-xl p-4 shadow-sm space-y-3"
                >
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-red-100/60 dark:bg-red-950/40 px-3 py-2 rounded-lg text-xs border border-red-200/40 dark:border-red-900/30">
                    <div class="flex flex-wrap gap-x-4 gap-y-1">
                      <div>
                        <span class="font-semibold text-red-800 dark:text-red-300">Prijavio:</span> 
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">{{ prijava.reporter_name }}</span>
                      </div>
                      <div>
                        <span class="font-semibold text-red-800 dark:text-red-300">Razlog:</span> 
                        <span class="bg-red-200/80 dark:bg-red-900/60 text-red-900 dark:text-red-200 px-2 py-0.5 rounded font-bold ml-1">{{ prijava.reason }}</span>
                      </div>
                    </div>
                    <div class="flex gap-2 self-end sm:self-auto">
                      <button 
                        @click="procesuirajPrijavu(prijava.report_id, 'dismiss')"
                        class="bg-white dark:bg-slate-700 hover:bg-slate-100 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-[11px] font-semibold px-2 py-1 rounded border border-slate-300 dark:border-slate-600 transition-colors"
                      >
                        Zanemari prijavu
                      </button>
                      <button 
                        @click="procesuirajPrijavu(prijava.report_id, 'resolve')"
                        class="bg-emerald-600 hover:bg-emerald-500 text-white text-[11px] font-semibold px-2 py-1 rounded transition-colors"
                      >
                        Riješeno (Zatvori)
                      </button>
                    </div>
                  </div>

                  <ForumTopicCard 
                    v-if="prijava.topic"
                    :tema="prijava.topic" 
                    :is-admin="isAdmin"
                    @obrisi="obrisiTemu"
                  />
                </div>
              </div>

              <div v-else>
                <div v-if="teme.length === 0" class="text-center py-12 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-8 shadow-sm">
                  <p class="text-slate-500 dark:text-slate-400 text-sm mb-4">Trenutno nema tema u ovoj kategoriji ili pretrazi. Započni temu!</p>
                  <router-link v-if="!isAdmin" :to="{ name: 'create-topic', query: odabraniKategorijaId ? { categoryId: odabraniKategorijaId } : {} }"
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

            </div>

            <ForumPagination 
              v-if="teme.length > 0 && !isLoading && !prikaziPrijave"
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