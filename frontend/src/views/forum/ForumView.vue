<script setup>
import { ref, onMounted, watch, computed, reactive } from 'vue';
import ForumSidebar from '../../components/ForumSidebar.vue';
import ForumTopicCard from '../../components/ForumTopicCard.vue';
import { useForumLazyLoading, updateTopicLikeInList } from '../../composables/useForumExtras.js';
import ForumSearchDropdown from '../../components/ForumSearchDropdown.vue';
import ForumFilters from '../../components/ForumFilters.vue';
import ForumWidgets from '../../components/ForumWidgets.vue';
import { 
  getTopics, 
  getCategories, 
  deleteTopic as deleteTopicApi, 
  getActiveAnnouncements, 
  getActiveReports, 
  handleReportAction 
} from '../../services/forum.js';
import {
  getReports as getAdminReports,
  dismissReport as dismissAdminReport,
  createAnnouncement
} from '../../services/forum_admin.js';
import AdminAnnouncementBanner from '../../components/ForumAdminAnnouncementBanner.vue';

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
const currentMode = ref('topics'); 
const isLoadingReports = ref(false);

const showModalAnnouncement = ref(false);
const newAnnouncementTitle = ref('');
const newAnnouncementContent = ref('');
const newAnnouncementDuration = ref(7); 
const isSubmittingAnnouncement = ref(false);

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

const formatirajDatum = (datumString) => {
  if (!datumString) return 'Nedavno';
  const d = new Date(datumString);
  return isNaN(d.getTime()) ? 'Nedavno' : d.toLocaleDateString('bs');
};

const filtriranePrijave = computed(() => {
  if (!Array.isArray(svePrijave.value)) return [];
  if (currentMode.value === 'active_reports') {
    return svePrijave.value.filter(p => p.status === 'pending' || !p.status || p.status === 'active');
  }
  if (currentMode.value === 'solved_reports') {
    return svePrijave.value.filter(p => p.status === 'resolved' || p.status === 'dismissed' || p.status === 'handled');
  }
  return [];
});

const ucitajTeme = async (append = false) => {
  if (!append) isLoading.value = true;

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
      teme.value = append ? [...teme.value, ...data.items] : data.items;
      ukupnoTema.value = data.total;
    } else if (Array.isArray(data)) {
      teme.value = append ? [...teme.value, ...data] : data;
      ukupnoTema.value = data.length;
    }
  } catch (error) {
    console.warn("Greška ili učitavanje demo podataka...", error);
    if (!append) {
      teme.value = [{ 
        id: 1, 
        title: "Dobrodošli na TK Student Hub forum", 
        content: "...", 
        views_count: 42, 
        comments_count: 3,
        likes_count: 0,
        category: { name: "Opšta diskusija" }, 
        author: { full_name: "Admin Hub" }, 
        created_at: new Date() 
      }];
      ukupnoTema.value = 1;
    }
  } finally {
    if (!append) isLoading.value = false;
  }
};

const ucitajPrijave = async (status) => {
  isLoadingReports.value = true;
  try {
    const data = await getAdminReports(status);
    if (data && data.reports) {
      svePrijave.value = data.reports;
    } else if (data && data.items) {
      svePrijave.value = data.items;
    } else if (Array.isArray(data)) {
      svePrijave.value = data;
    } else {
      svePrijave.value = [];
    }
  } catch (error) {
    console.error("Greška pri učitavanju prijava:", error);
    svePrijave.value = [];
  } finally {
    isLoadingReports.value = false;
  }
};

onMounted(async () => {
  await ucitajTeme();
  try { sveKategorije.value = await getCategories(); } catch (e) { console.error(e); }
  try { announcements.value = await getActiveAnnouncements(); } catch (e) { console.error(e); }
});

watch(odabraniKategorijaId, () => { 
  currentMode.value = 'topics';
  trenutnaStranica.value = 1; 
  ucitajTeme(); 
});

const filtrirajPoKategoriji = (id) => odabraniKategorijaId.value = id;

const handleSearchSubmitted = (query) => {
  search.value = query;
  trenutnaStranica.value = 1;
  ucitajTeme();
};

const handleFiltersChanged = (noviFilteri) => {
  aktivniFilteri.sort_by = noviFilteri.sort_by;
  aktivniFilteri.unanswered = noviFilteri.unanswered;
  aktivniFilteri.days_old = noviFilteri.days_old;
  trenutnaStranica.value = 1; 
  ucitajTeme();
};

async function podnesiNovoObavjestenje() {
  if (!newAnnouncementTitle.value.trim() || !newAnnouncementContent.value.trim()) {
    alert("Molimo unesite naslov i sadržaj obavještenja.");
    return;
  }
  isSubmittingAnnouncement.value = true;
  try {
    await createAnnouncement(
      newAnnouncementTitle.value.trim(),
      newAnnouncementContent.value.trim(),
      newAnnouncementDuration.value
    );
    alert("Obavještenje uspješno kreirano i aktivirano!");
    showModalAnnouncement.value = false;
    
    newAnnouncementTitle.value = '';
    newAnnouncementContent.value = '';
    newAnnouncementDuration.value = 7;

    announcements.value = await getActiveAnnouncements();
  } catch (error) {
    alert("Greška: " + error.message);
  } finally {
    isSubmittingAnnouncement.value = false;
  }
}

const obrisiTemu = async (temaId) => {
  if (!confirm('Da li ste sigurni da želite obrisati ovu temu?')) return;
  try {
    await deleteTopicApi(temaId);
    
    if (currentMode.value === 'active_reports' || currentMode.value === 'solved_reports') {
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

const procesuirajPrijavu = async (reportId, akcija) => {
  try {
    await handleReportAction(reportId, akcija);
    svePrijave.value = svePrijave.value.map(p => {
      if (p.report_id === reportId) {
        return { ...p, status: akcija === 'dismiss' ? 'dismissed' : 'resolved' };
      }
      return p;
    });
    alert(akcija === 'dismiss' ? "Prijava uspješno odbačena." : "Prijava označena kao riješena.");
  } catch (error) {
    alert("Greška: " + error.message);
  }
};

const handleLikeUpdated = (payload) => {
  updateTopicLikeInList(teme, payload);
};

const { isLoadingMore, imaJosTema } = useForumLazyLoading({
  teme,
  ukupnoTema,
  trenutnaStranica,
  prikaziPrijave,
  ucitajTeme
});

watch(currentMode, (newMode) => {
  prikaziPrijave.value = (newMode === 'active_reports' || newMode === 'solved_reports');
  trenutnaStranica.value = 1;
  
  if (newMode === 'active_reports') {
    ucitajPrijave('pending');
  } else if (newMode === 'solved_reports') {
    ucitajPrijave('resolved');
  } else if (newMode === 'topics') {
    ucitajTeme();
  }
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-3 transition-colors duration-200">
    <div class="max-w-7xl mx-auto">

      <div class="flex justify-between items-center mb-4 border-b border-gray-200 dark:border-slate-800 py-2 pt-4 -mt-2">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-800 dark:text-white">Studentski Forum</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>

        <div>
          <button 
            v-if="isAdmin" 
            @click="showModalAnnouncement = true"
            class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg text-xs shadow-md transition-all flex items-center gap-1.5"
          >
            📢 Admin obavještenje
          </button>
        </div>
      </div>

      <AdminAnnouncementBanner :announcements="announcements" />

      <div class="sticky top-[72px] z-30 bg-gray-50 dark:bg-slate-900 pb-2 mb-3 border-b border-gray-200 dark:border-slate-800">

        <div v-if="isAdmin" class="flex gap-1 bg-gray-100 dark:bg-slate-800 p-1 rounded-xl max-w-lg mt-2 mb-2 border border-gray-200 dark:border-slate-700 select-none">
          <button 
            @click="currentMode = 'topics'"
            :class="currentMode === 'topics' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'"
            class="flex-1 py-1.5 text-xs rounded-lg transition-all"
          >
            Sve teme
          </button>
          <button 
            @click="currentMode = 'active_reports'"
            :class="currentMode === 'active_reports' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'"
            class="flex-1 py-1.5 text-xs rounded-lg transition-all relative"
          >
            Aktivne prijave
            <span v-if="currentMode !== 'active_reports' && svePrijave.length > 0" class="absolute top-1.5 right-2 flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
          </button>
          <button 
            @click="currentMode = 'solved_reports'"
            :class="currentMode === 'solved_reports' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'"
            class="flex-1 py-1.5 text-xs rounded-lg transition-all"
          >
            Riješene prijave
          </button>
        </div>

        <div v-if="currentMode === 'topics'" class="flex flex-col md:flex-row md:items-center justify-between gap-2 mt-2 w-full">
          <div class="flex-shrink-0">
            <span class="px-3 py-1 font-extrabold text-xs rounded-full border dark:border-slate-700 shadow-sm transition-all duration-300"
              :style="{ backgroundColor: trenutnaKategorija.color + '15', borderColor: trenutnaKategorija.color, color: trenutnaKategorija.color }">
              {{ trenutnaKategorija.name }}
            </span>
          </div>

          <div class="flex-1 w-full max-w-xl mx-auto flex gap-1.5 items-center">
            <ForumSearchDropdown @search-submitted="handleSearchSubmitted" />
            <ForumFilters @filters-changed="handleFiltersChanged" />
          </div>

          <div class="flex-shrink-0">
            <router-link 
              v-if="!isAdmin" 
              to="/forum/nova-tema" 
              class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-5 py-2 rounded-lg transition-colors shadow-md text-xs whitespace-nowrap"
            >
              Nova tema
            </router-link>
            <div v-else class="hidden md:block w-6"></div>
          </div>
        </div>

      </div>
      
      <div class="grid grid-cols-12 gap-2 items-start w-full">

        <div 
          class="col-span-12 md:col-span-3 lg:col-span-3 xl:col-span-3"
          style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;"
        >
          <ForumSidebar :aktivna-kategorija-id="odabraniKategorijaId" @kategorija-izabrana="filtrirajPoKategoriji" />
        </div>

        <div class="col-span-12 md:col-span-6 lg:col-span-6 xl:col-span-6 w-full">
          <div class="flex flex-col justify-between min-h-[500px]">
            <div>

              <div v-if="isLoading || isLoadingReports" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-[#ff7a00] mb-3"></div>
                <p class="text-slate-500 dark:text-slate-400 italic text-xs">Učitavanje podataka...</p>
              </div>

              <div v-else-if="currentMode === 'topics'">
                <div v-if="teme.length === 0" class="text-center py-8 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 shadow-sm">
                  <p class="text-slate-500 dark:text-slate-400 text-xs mb-3">Trenutno nema tema u ovoj kategoriji ili pretrazi. Započni temu!</p>
                  <router-link v-if="!isAdmin" :to="{ name: 'create-topic', query: odabraniKategorijaId ? { categoryId: odabraniKategorijaId } : {} }"
                    class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-5 py-1.5 rounded-lg text-xs shadow-md">
                    Započni temu
                  </router-link>
                </div>

                <div v-else class="space-y-2">
                  <ForumTopicCard
                    v-for="tema in teme"
                    :key="tema.id"
                    :tema="tema"
                    :is-admin="isAdmin"
                    @obrisi="obrisiTemu"
                    @like-updated="handleLikeUpdated"
                  />
                </div>
              </div>

              <div v-else-if="currentMode === 'active_reports' || currentMode === 'solved_reports'">
                <div v-if="filtriranePrijave.length === 0" class="text-center py-8 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 p-6 shadow-sm">
                  <p class="text-emerald-600 dark:text-emerald-400 font-medium text-xs">
                    {{ currentMode === 'active_reports' ? '🎉 Odlično! Trenutno nema neriješenih prijava korisnika.' : 'Nema riješenih prijava u arhivi.' }}
                  </p>
                </div>
                
                <div v-else class="space-y-2">
                  <div 
                    v-for="prijava in filtriranePrijave" 
                    :key="prijava.report_id" 
                    class="bg-white dark:bg-slate-800 p-3 rounded-xl border border-gray-100 dark:border-slate-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3 transition-all"
                  >
                    <div class="flex-1 w-full">
                      <div class="flex items-center gap-2 flex-wrap">
                        <span class="text-[9px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-wider" 
                              :class="prijava.status === 'resolved' || prijava.status === 'dismissed' ? 'bg-green-50 text-green-600 dark:bg-green-950/30 dark:text-green-400' : 'bg-red-50 text-red-600 dark:bg-red-950/30 dark:text-red-400'">
                          {{ prijava.status === 'resolved' || prijava.status === 'dismissed' ? 'Arhivirano' : 'Čeka pregled' }}
                        </span>
                        <span class="text-[11px] text-slate-400 dark:text-slate-500">{{ formatirajDatum(prijava.created_at) }}</span>
                      </div>
                      <h4 class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-1">
                        Tema: <router-link v-if="prijava.topic" :to="`/forum/tema/${prijava.topic.id}`" class="text-orange-500 hover:underline">{{ prijava.topic.title }}</router-link>
                        <span v-else class="text-red-400 italic font-normal">(Tema je već izbrisana)</span>
                      </h4>
                      <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5 italic bg-gray-50 dark:bg-slate-700/50 p-1.5 rounded-lg border border-gray-100 dark:border-slate-700">
                        Razlog prijave: "{{ prijava.reason }}" <span v-if="prijava.reporter_name" class="font-semibold text-slate-400 not-italic">(Prijavio: {{ prijava.reporter_name }})</span>
                      </p>
                    </div>
                    
                    <div v-if="prijava.status !== 'resolved' && prijava.status !== 'dismissed'" class="flex items-center gap-1.5 w-full md:w-auto justify-end">
                      <button 
                        @click="procesuirajPrijavu(prijava.report_id, 'dismiss')"
                        class="bg-white dark:bg-slate-700 hover:bg-slate-100 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-[11px] font-semibold px-2.5 py-1.5 rounded-lg border border-slate-300 dark:border-slate-600 transition-colors shadow-sm"
                      >
                        Zanemari
                      </button>
                      <button 
                        @click="procesuirajPrijavu(prijava.report_id, 'resolve')"
                        class="bg-emerald-500 hover:bg-emerald-600 text-white text-[11px] font-bold px-2.5 py-1.5 rounded-lg transition-colors shadow-sm whitespace-nowrap"
                      >
                        Označi riješeno
                      </button>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <div v-if="currentMode === 'topics' && teme.length > 0" class="mt-4 text-center text-[11px] text-slate-500 dark:text-slate-400">
              <div v-if="isLoadingMore" class="py-2 flex justify-center">
                <div class="w-6 h-6 border-3 border-gray-300 border-t-[#ff7a00] rounded-full animate-spin"></div>
              </div>
              <div v-else-if="!imaJosTema" class="py-1">
                Prikazane su sve teme.
              </div>
            </div>

          </div>
        </div>

        <div 
          class="col-span-12 md:col-span-3 lg:col-span-3 xl:col-span-3"
          style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;"
        >
          <ForumWidgets />
        </div>

      </div>
    </div>

    <div v-if="showModalAnnouncement" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-opacity">
      <div class="bg-white dark:bg-slate-900 w-full max-w-xl rounded-2xl shadow-2xl border border-gray-100 dark:border-slate-800 overflow-hidden transform transition-all animate-in fade-in zoom-in-95 duration-200">
        
        <div class="px-5 py-3 border-b border-gray-100 dark:border-slate-800 flex justify-between items-center bg-gray-50/50 dark:bg-slate-800/40">
          <div class="flex items-center gap-2">
            <span class="text-lg select-none">📢</span>
            <h3 class="text-sm font-bold text-slate-800 dark:text-slate-100">Novo admin obavještenje</h3>
          </div>
          <button @click="showModalAnnouncement = false" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors text-xs font-bold">✕</button>
        </div>
        
        <div class="p-5 space-y-3">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Naslov obavještenja</label>
            <input 
              v-model="newAnnouncementTitle" 
              type="text" 
              placeholder="Npr. Obavještenje o održavanju servera..."
              class="w-full px-3 py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-transparent text-xs focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-800 dark:text-slate-100"
            />
          </div>
          
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Sadržaj poruke</label>
            <textarea 
              v-model="newAnnouncementContent" 
              rows="3" 
              placeholder="Unesite detaljan tekst obavještenja..."
              class="w-full px-3 py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-transparent text-xs focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-800 dark:text-slate-100 resize-none"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Trajanje vidljivosti</label>
            <select 
              v-model="newAnnouncementDuration"
              class="w-full px-3 py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-slate-800 dark:text-slate-100"
            >
              <option :value="1">1 Dan</option>
              <option :value="3">3 Dana</option>
              <option :value="7">7 Dana</option>
              <option :value="14">14 Dana</option>
              <option :value="30">30 Dana</option>
              <option :value="365">Trajno (Godinu dana)</option>
            </select>
          </div>
        </div>
        
        <div class="px-5 py-3 bg-gray-50 dark:bg-slate-800/40 border-t border-gray-100 dark:border-slate-800 flex items-center justify-end gap-2">
          <button @click="showModalAnnouncement = false" class="px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 transition-all">
            Otkaži
          </button>
          <button 
            @click="podnesiNovoObavjestenje"
            :disabled="isSubmittingAnnouncement"
            class="px-4 py-1.5 rounded-xl text-xs font-bold text-white bg-orange-500 hover:bg-orange-600 disabled:bg-orange-400 disabled:cursor-not-allowed shadow transition-all flex items-center gap-1.5"
          >
            <span v-if="isSubmittingAnnouncement" class="w-2.5 h-2.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Objavi
          </button>
        </div>
      </div>
    </div>

  </div>
</template>