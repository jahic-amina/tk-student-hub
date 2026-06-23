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
  getActiveAnnouncements
} from '../../services/forum.js';
import {
  getReports as getAdminReports,
  createAnnouncement,
  resolveReport
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

const showReportModal = ref(false);
const handlingReportId = ref(null);
const handlingAction = ref(''); 
const adminExplanation = ref('');

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
      teme.value = [{ id: 1, title: "Dobrodošli na TK Student Hub forum", content: "...", views_count: 42, comments_count: 3, likes_count: 0, category: { name: "Opšta diskusija" }, author: { full_name: "Admin Hub" }, created_at: new Date() }];
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
    svePrijave.value = data?.reports || data?.items || (Array.isArray(data) ? data : []);
  } catch (error) {
    console.error("Greška pri učitavanju prijava:", error);
    svePrijave.value = [];
  } finally {
    isLoadingReports.value = false;
  }
};

onMounted(async () => {
  await ucitajTeme();
  try { sveKategorije.value = await getCategories(); } catch (e) {}
  try { announcements.value = await getActiveAnnouncements(); } catch (e) {}
});

watch(odabraniKategorijaId, () => { 
  currentMode.value = 'topics';
  trenutnaStranica.value = 1; 
  ucitajTeme(); 
});

const filtrirajPoKategoriji = (id) => odabraniKategorijaId.value = id;
const handleSearchSubmitted = (query) => { search.value = query; trenutnaStranica.value = 1; ucitajTeme(); };
const handleFiltersChanged = (noviFilteri) => {
  aktivniFilteri.sort_by = noviFilteri.sort_by;
  aktivniFilteri.unanswered = noviFilteri.unanswered;
  aktivniFilteri.days_old = noviFilteri.days_old;
  trenutnaStranica.value = 1; 
  ucitajTeme();
};

async function podnesiNovoObavjestenje() {
  if (!newAnnouncementTitle.value.trim() || !newAnnouncementContent.value.trim()) {
    alert("Naslov i sadržaj obavještenja su obavezni!");
    return;
  }
  isSubmittingAnnouncement.value = true;
  try {
    await createAnnouncement(
      newAnnouncementTitle.value.trim(), 
      newAnnouncementContent.value.trim(), 
      newAnnouncementDuration.value
    );
    showModalAnnouncement.value = false;
    newAnnouncementTitle.value = ''; 
    newAnnouncementContent.value = '';
    newAnnouncementDuration.value = 7;
    announcements.value = await getActiveAnnouncements();
    alert("Obavještenje uspješno objavljeno!");
  } catch (error) { 
    alert("Greška: " + error.message); 
  } finally { 
    isSubmittingAnnouncement.value = false; 
  }
}

const obrisiTemu = async (temaId) => {
  if (!confirm('Da li ste sigurni?')) return;
  try {
    await deleteTopicApi(temaId);
    if (currentMode.value === 'active_reports' || currentMode.value === 'solved_reports') {
      const uvezanaPrijava = svePrijave.value.find(p => p.topic?.id === temaId);
      if (uvezanaPrijava) {
        await resolveReport(uvezanaPrijava.report_id || uvezanaPrijava.id, 'accept', 'Tema obrisana direktno iz foruma.');
        svePrijave.value = svePrijave.value.filter(p => p.topic?.id !== temaId);
      }
    } else {
      teme.value = teme.value.filter(t => t.id !== temaId);
      ukupnoTema.value = Math.max(0, ukupnoTema.value - 1);
    }
  } catch (error) { alert(error.message); }
};

const openReportModal = (reportId, action) => {
  handlingReportId.value = reportId;
  handlingAction.value = action;
  adminExplanation.value = '';
  showReportModal.value = true;
};

const closeReportModal = () => {
  showReportModal.value = false;
  handlingReportId.value = null;
  handlingAction.value = '';
  adminExplanation.value = '';
};

const submitReportAction = async () => {
  if (!adminExplanation.value.trim()) {
    alert('Morate unijeti obrazloženje akcije.');
    return;
  }
  
  try {
    await resolveReport(handlingReportId.value, handlingAction.value, adminExplanation.value);
    
    svePrijave.value = svePrijave.value.map(p => 
      (p.report_id || p.id) === handlingReportId.value 
        ? { ...p, status: handlingAction.value === 'dismiss' ? 'dismissed' : 'resolved' } 
        : p
    );
    
    closeReportModal();
    alert('Prijava je uspješno riješena.');
  } catch (error) {
    alert('Došlo je do greške: ' + error.message);
  }
};

const handleLikeUpdated = (payload) => { updateTopicLikeInList(teme, payload); };

const { isLoadingMore, imaJosTema } = useForumLazyLoading({ teme, ukupnoTema, trenutnaStranica, prikaziPrijave, ucitajTeme });

watch(currentMode, (newMode) => {
  prikaziPrijave.value = (newMode === 'active_reports' || newMode === 'solved_reports');
  trenutnaStranica.value = 1;
  if (newMode === 'active_reports') ucitajPrijave('pending');
  else if (newMode === 'solved_reports') ucitajPrijave('resolved');
  else if (newMode === 'topics') ucitajTeme();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-3 transition-colors duration-300">
    <div class="max-w-7xl mx-auto">

      <div class="flex justify-between items-center mb-5 border-b border-gray-200 dark:border-slate-800 py-2 pt-4 -mt-2">
        <div>
          <h1 class="text-3xl font-black tracking-tight text-slate-800 dark:text-white">Studentski Forum</h1>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-0.5">Postavi pitanje, podijeli ideju ili pomogni kolegama.</p>
        </div>
        <div>
          <button v-if="isAdmin" @click="showModalAnnouncement = true" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg text-xs shadow-md transition-all">📢 Admin obavještenje</button>
        </div>
      </div>

      <AdminAnnouncementBanner :announcements="announcements" />

      <div class="sticky top-[72px] z-30 bg-gray-50 dark:bg-slate-900 pb-2 mb-4 border-b border-gray-200 dark:border-slate-800">
        <div v-if="isAdmin" class="flex gap-1 bg-gray-100 dark:bg-slate-800 p-1 rounded-xl max-w-lg mt-2 mb-2 border border-gray-200 dark:border-slate-700 select-none">
          <button @click="currentMode = 'topics'" :class="currentMode === 'topics' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400'" class="flex-1 py-1.5 text-xs rounded-lg">Sve teme</button>
          <button @click="currentMode = 'active_reports'" :class="currentMode === 'active_reports' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400'" class="flex-1 py-1.5 text-xs rounded-lg">Aktivne prijave</button>
          <button @click="currentMode = 'solved_reports'" :class="currentMode === 'solved_reports' ? 'bg-white dark:bg-slate-700 shadow text-orange-600 dark:text-orange-400 font-bold' : 'text-slate-600 dark:text-slate-400'" class="flex-1 py-1.5 text-xs rounded-lg">Riješene prijave</button>
        </div>

        <div v-if="currentMode === 'topics'" class="flex flex-col md:flex-row md:items-center justify-between gap-2 mt-2 w-full">
          <div class="flex-shrink-0">
            <span class="px-3 py-1 font-extrabold text-xs rounded-full border dark:border-slate-700 shadow-sm" :style="{ backgroundColor: trenutnaKategorija.color + '15', borderColor: trenutnaKategorija.color, color: trenutnaKategorija.color }">
              {{ trenutnaKategorija.name }}
            </span>
          </div>
          <div class="flex-1 w-full max-w-xl mx-auto flex gap-1.5 items-center">
            <ForumSearchDropdown @search-submitted="handleSearchSubmitted" />
            <ForumFilters @filters-changed="handleFiltersChanged" />
          </div>
          <div class="flex-shrink-0">
            <router-link v-if="!isAdmin" to="/forum/nova-tema" class="bg-[#ff7a00] hover:bg-[#e66e00] text-white font-bold px-5 py-2 rounded-lg transition-colors shadow-md text-xs whitespace-nowrap">Nova tema</router-link>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-12 gap-4 items-start w-full">

        <div class="col-span-12 md:col-span-2 lg:col-span-2 xl:col-span-2" style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;">
          <ForumSidebar :aktivna-kategorija-id="odabraniKategorijaId" @kategorija-izabrana="filtrirajPoKategoriji" />
        </div>

        <div class="col-span-12 md:col-span-7 lg:col-span-7 xl:col-span-7 w-full">
          <div class="flex flex-col justify-between min-h-[500px]">
            <div>
              <div v-if="isLoading || isLoadingReports" class="flex flex-col items-center justify-center py-12">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-[#ff7a00] mb-3"></div>
              </div>

              <div v-else-if="currentMode === 'topics'">
                <div v-if="teme.length === 0" class="text-center py-8 bg-white dark:bg-slate-800 rounded-xl border border-gray-200 p-6 shadow-sm">
                  <p class="text-slate-500 text-xs mb-3">Trenutno nema tema.</p>
                </div>
                <div v-else class="space-y-3">
                  <ForumTopicCard v-for="tema in teme" :key="tema.id" :tema="tema" :is-admin="isAdmin" @obrisi="obrisiTemu" @like-updated="handleLikeUpdated" />
                </div>
              </div>

              <div v-else-if="currentMode === 'active_reports' || currentMode === 'solved_reports'">
                <div v-if="filtriranePrijave.length === 0" class="text-center py-8 bg-white dark:bg-slate-800 rounded-xl p-6 shadow-sm">
                  <p class="text-emerald-600 text-xs font-bold">Nema prijava u ovoj sekciji.</p>
                </div>
                <div v-else class="space-y-2">
                  <div v-for="prijava in filtriranePrijave" :key="prijava.report_id" class="bg-white dark:bg-slate-800 p-3 rounded-xl border border-gray-100 dark:border-slate-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                    <div class="flex-1 w-full">
                      <h4 class="text-xs font-bold text-slate-800 dark:text-slate-200">
                        Tema: <router-link v-if="prijava.topic" :to="`/forum/tema/${prijava.topic.id}`" class="text-orange-500 hover:underline">{{ prijava.topic.title }}</router-link>
                      </h4>
                      <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-1 italic bg-gray-50 dark:bg-slate-700/50 p-2 rounded-lg">Razlog: "{{ prijava.reason }}"</p>
                    </div>
                    <div v-if="prijava.status !== 'resolved' && prijava.status !== 'dismissed'" class="flex items-center gap-1.5 justify-end w-full md:w-auto">
                      <button @click="openReportModal(prijava.report_id || prijava.id, 'accept')" class="font-inherit text-sm font-medium border border-green-500 bg-green-50 text-green-700 hover:bg-green-100 px-4 py-1.5 rounded-lg transition-colors">Prihvati</button>
                      <button @click="openReportModal(prijava.report_id || prijava.id, 'dismiss')" class="font-inherit text-sm font-medium border border-red-500 bg-red-50 text-red-700 hover:bg-red-100 px-4 py-1.5 rounded-lg transition-colors">Zanemari</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 text-center text-[11px] text-slate-500">
              <div v-if="isLoadingMore" class="py-2 flex justify-center"><div class="w-6 h-6 border-3 border-gray-300 border-t-[#ff7a00] rounded-full animate-spin"></div></div>
              <div v-else-if="!imaJosTema && currentMode === 'topics' && teme.length > 0" class="py-1">Prikazane su sve teme.</div>
            </div>
          </div>
        </div>

        <div class="col-span-12 md:col-span-3 lg:col-span-3 xl:col-span-3" style="position: sticky; top: 140px; align-self: flex-start; z-index: 20;">
          <ForumWidgets :selected-category-id="odabraniKategorijaId" />
        </div>

      </div>
    </div>

    <div v-if="showModalAnnouncement" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-all">
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl w-full max-w-md shadow-2xl border border-gray-100 dark:border-slate-700">
        <h2 class="text-xl font-bold mb-4 flex gap-2 text-slate-800 dark:text-white">
          <span>📢</span> Novo Admin Obavještenje
        </h2>
        
        <div class="space-y-4">
          <div>
            <label class="block mb-1 text-xs font-bold text-slate-700 dark:text-slate-300">Naslov obavještenja</label>
            <input 
              v-model="newAnnouncementTitle" 
              type="text" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2.5 text-sm bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none" 
              placeholder="Npr. Važno obavještenje za ispitne rokove" 
            />
          </div>
          
          <div>
            <label class="block mb-1 text-xs font-bold text-slate-700 dark:text-slate-300">Sadržaj (Tekst poruke)</label>
            <textarea 
              v-model="newAnnouncementContent" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2.5 text-sm bg-white dark:bg-slate-700 text-slate-900 dark:text-white h-24 focus:ring-2 focus:ring-amber-500 focus:outline-none resize-none" 
              placeholder="Unesite detalje koje će studenti vidjeti na vrhu foruma..."
            ></textarea>
          </div>
          
          <div>
            <label class="block mb-1 text-xs font-bold text-slate-700 dark:text-slate-300">Trajanje prikaza (u danima)</label>
            <input 
              v-model.number="newAnnouncementDuration" 
              type="number" 
              min="1" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2.5 text-sm bg-white dark:bg-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none" 
            />
          </div>
        </div>
        
        <div class="flex justify-end gap-3 mt-6">
          <button 
            @click="showModalAnnouncement = false" 
            :disabled="isSubmittingAnnouncement"
            class="px-4 py-2 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 rounded-lg text-xs font-medium transition-colors"
          >
            Otkaži
          </button>
          <button 
            @click="podnesiNovoObavjestenje" 
            :disabled="isSubmittingAnnouncement"
            class="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-bold shadow-md transition-colors disabled:opacity-50"
          >
            {{ isSubmittingAnnouncement ? 'Objavljivanje...' : 'Objavi obavještenje' }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="showReportModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white p-6 rounded-xl w-full max-w-md shadow-2xl">
            <h2 class="text-xl font-bold mb-4">
                {{ handlingAction === 'accept' ? '✅ Prihvati prijavu' : '❌ Zanemari prijavu' }}
            </h2>
            
            <p class="text-sm text-gray-600 mb-4">
                Molimo vas da unesete obrazloženje zašto ste odlučili da {{ handlingAction === 'accept' ? 'prihvatite (i obrišete temu)' : 'zanemarite' }} ovu prijavu. Ovo će biti sačuvano u evidenciji.
            </p>

            <label class="block mb-2 text-sm font-bold text-gray-700">Obrazloženje</label>
            <textarea 
                v-model="adminExplanation" 
                class="w-full border rounded p-3 mb-6 h-32 focus:ring focus:ring-orange-300 outline-none" 
                placeholder="Unesite vaše obrazloženje ovdje..."
            ></textarea>
            
            <div class="flex justify-end gap-3">
                <button 
                    @click="closeReportModal" 
                    class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded font-medium transition-colors">
                    Otkaži
                </button>
                <button 
                    @click="submitReportAction" 
                    class="px-5 py-2 text-white rounded font-bold transition-colors"
                    :class="handlingAction === 'accept' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'">
                    Završi
                </button>
            </div>
        </div>
    </div>

  </div>
</template>