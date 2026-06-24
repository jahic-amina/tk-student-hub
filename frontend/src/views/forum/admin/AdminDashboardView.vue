<script setup>
import { ref, onMounted, computed } from 'vue'; 
import { useRouter } from 'vue-router';
import { 
  getUsers, 
  changeUserRole, 
  getReports, 
  dismissReport, 
  createAnnouncement, 
  deleteAnnouncement,
  getAllAnnouncements,   
  updateAnnouncement,
  getHandledReports,
  reopenReport,
  resolveReport     
} from '../../../services/forum_admin.js'; 

const router = useRouter();

const activeTab = ref('reports');
const users = ref([]);
const reports = ref([]);
const handledReports = ref([]); 
const announcements = ref([]); 

const showAnnouncementModal = ref(false);
const newAnnTitle = ref('');
const newAnnContent = ref('');
const durationDays = ref(0); 

const editingAnn = ref(null);  

const showReportModal = ref(false);
const handlingReportId = ref(null);
const handlingAction = ref(''); 
const adminExplanation = ref('');
const reopeningId = ref(null);

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

// Search query
const searchQuery = ref('');

const loadData = async () => {
  try {
    if (activeTab.value === 'users') users.value = await getUsers() || [];
    if (activeTab.value === 'reports') reports.value = await getReports('pending') || []; 
    if (activeTab.value === 'announcements') announcements.value = await getAllAnnouncements() || [];
    if (activeTab.value === 'handled_reports') handledReports.value = await getHandledReports() || [];
  } catch (error) {
    console.error("Greška pri učitavanju podataka:", error);
  }
};

onMounted(() => loadData());

// Computed za pretragu
const filteredReports = computed(() => {
  const lista = Array.isArray(reports.value) ? reports.value : [];
  if (!searchQuery.value) return lista;
  return lista.filter(r => 
    r.topic?.title?.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
    r.reason?.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const filteredHandledReports = computed(() => {
  const lista = Array.isArray(handledReports.value) ? handledReports.value : [];
  if (!searchQuery.value) return lista;
  return lista.filter(r => 
    r.topic?.title?.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
    r.reason?.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const setRole = async (userId, role) => {
  await changeUserRole(userId, role);
  await loadData();
};

const postAnnouncement = async () => {
  if (!newAnnTitle.value.trim() || !newAnnContent.value.trim()) {
      alert("Naslov i sadržaj su obavezni!");
      return;
  }
  await createAnnouncement(newAnnTitle.value, newAnnContent.value, durationDays.value);
  newAnnTitle.value = '';
  newAnnContent.value = '';
  durationDays.value = 0;
  showAnnouncementModal.value = false;
  alert('Globalno obavještenje uspješno objavljeno!');
  await loadData();
};


const submitReportAction = async () => {
  if (!adminExplanation.value.trim()) {
    alert('Morate unijeti obrazloženje akcije.');
    return;
  }
  
  try {
    const targetId = handlingReportId.value;
    await resolveReport(targetId, handlingAction.value, adminExplanation.value);
    closeReportModal();
    reports.value = await getReports('pending') || [];
    handledReports.value = await getHandledReports() || [];
  } catch (error) {
    alert('Došlo je do greške: ' + error.message);
  }
};

const handleReopenReport = async (reportId) => {
  if (!confirm('Vratiti ovu prijavu u aktivne? Obrazloženje i akcija će biti obrisani.')) return;
  reopeningId.value = reportId;
  try {
    await reopenReport(reportId);
    reports.value = await getReports('pending') || [];
    handledReports.value = await getHandledReports() || [];
  } catch (e) {
    alert(e.message || 'Greška pri vraćanju prijave.');
  } finally {
    reopeningId.value = null;
  }
};

const goToTopic = (topicId) => {
  if (topicId) {
    router.push(`/forum/tema/${topicId}`);
  } else {
    alert('Nije moguće otvoriti ovu temu jer je trajno uklonjena iz baze bez sačuvanog ID-a.');
  }
};

</script>


<template>
  <div class="p-6 max-w-7xl mx-auto min-h-screen">
    <div class="flex items-center justify-between mb-8 bg-slate-900 text-white p-6 rounded-xl shadow-lg border-l-8 border-orange-500">
      <div class="flex items-center gap-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        <div>
          <h1 class="text-3xl font-black uppercase tracking-widest">Admin Panel</h1>
          <p class="text-slate-400 text-sm">Upravljanje platformom i korisnicima</p>
        </div>
      </div>
      <button @click="showAnnouncementModal = true" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-6 rounded-lg shadow transition-colors flex gap-2 items-center cursor-pointer">
        <span>📢</span> Globalno obavještenje
      </button>
    </div>

    <div class="flex gap-4 mb-6 border-b border-gray-200 pb-2">
      <button 
        @click="activeTab = 'reports'; loadData()" 
        class="pb-2 text-sm font-semibold transition-colors cursor-pointer bg-transparent border-none"
        :class="activeTab === 'reports' ? 'border-b-2 border-orange-500 text-orange-600' : 'text-gray-500 hover:text-slate-700'"
      >
        Aktivne Prijave
        <span v-if="reports.length" class="ml-1.5 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">
          {{ reports.length }}
        </span>
      </button>
      <button 
        @click="activeTab = 'handled_reports'; loadData()" 
        class="pb-2 text-sm font-semibold transition-colors cursor-pointer bg-transparent border-none"
        :class="activeTab === 'handled_reports' ? 'border-b-2 border-orange-500 text-orange-600' : 'text-gray-500 hover:text-slate-700'"
      >
        Riješene Prijave
      </button>
    </div>

    <div v-if="activeTab === 'reports' || activeTab === 'handled_reports'" class="mb-6">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Pretraži prijave i teme..." 
        class="w-full p-3 rounded-lg border border-gray-300 dark:border-slate-600 focus:ring-2 focus:ring-orange-400 focus:outline-none text-sm" 
      />
    </div>

    <div v-if="activeTab === 'reports'">
      <div v-if="filteredReports.length === 0" class="text-center py-12 text-gray-400">
        <p class="text-4xl mb-3">✅</p>
        <p class="font-semibold">Nema aktivnih prijava.</p>
      </div>

      <div 
        v-for="report in filteredReports" 
        :key="report.report_id || report.id" 
        class="p-4 bg-white shadow-sm rounded-xl mb-4 border-l-4 border-red-500 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <button 
              @click="goToTopic(report.topic?.id || report.topic_id)"
              class="font-bold text-base text-slate-800 hover:text-orange-600 transition-colors text-left bg-transparent border-none p-0 cursor-pointer"
            >
              {{ report.topic?.title || report.topic_title || 'Nepoznata tema' }}
              <span class="ml-1 text-xs text-orange-400">↗</span>
            </button>
            <p class="text-sm text-gray-600 mt-1"><b>Razlog:</b> {{ report.reason }}</p>
            <div class="flex items-center gap-2 mt-2 text-xs text-gray-500">
              <span>⚠️ Prijavio/la:</span>
              <span class="font-semibold text-orange-600 bg-orange-50 px-2 py-0.5 rounded">
                {{ report.reporter_name || 'Nepoznato' }}
              </span>
            </div>
          </div>
        </div>

        <div class="mt-3 flex gap-2">
          <button 
            @click="openReportModal(report.report_id || report.id, 'accept')" 
            class="text-sm font-medium border border-green-500 bg-green-50 text-green-700 hover:bg-green-100 px-4 py-1.5 rounded-lg transition-colors cursor-pointer"
          >
            ✅ Prihvati
          </button>
          <button 
            @click="openReportModal(report.report_id || report.id, 'dismiss')" 
            class="text-sm font-medium border border-slate-300 bg-slate-50 text-slate-600 hover:bg-slate-100 px-4 py-1.5 rounded-lg transition-colors cursor-pointer"
          >
            ❌ Zanemari
          </button>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'handled_reports'">
      <div v-if="filteredHandledReports.length === 0" class="text-center py-12 text-gray-400">
        <p class="text-4xl mb-3">📋</p>
        <p class="font-semibold">Nema riješenih prijava.</p>
      </div>

      <div 
        v-for="report in filteredHandledReports" 
        :key="report.id || report.report_id" 
        class="p-4 border rounded-xl shadow-sm mb-4 bg-white hover:shadow-md transition-shadow"
        :class="report.action_taken === 'accept' ? 'border-l-4 border-green-400' : 'border-l-4 border-slate-300'"
      >
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <button 
              @click="goToTopic(report.topic?.id || report.topic_id)"
              class="font-bold text-base text-slate-800 hover:text-orange-600 transition-colors text-left bg-transparent border-none p-0 cursor-pointer"
            >
              {{ report.topic?.title || report.topic_title || 'Obrisana tema' }}
              <span class="ml-1 text-xs text-orange-400">↗</span>
            </button>

            <div class="flex items-center gap-2 mt-1.5 text-xs text-gray-500">
              <span>👤 Prijavio/la:</span>
              <span class="font-medium text-slate-700 bg-gray-100 px-2 py-0.5 rounded">
                {{ report.reporter_name || 'Nepoznato' }}
              </span>
            </div>

            <p class="text-sm text-gray-700 mt-1">
              <strong>Razlog prijave:</strong> {{ report.reason }}
            </p>

            <div 
              class="mt-3 p-3 rounded-lg" 
              :class="report.action_taken === 'accept' ? 'bg-green-50 border border-green-200' : 'bg-slate-50 border border-slate-200'"
            >
              <p class="text-sm font-semibold" :class="report.action_taken === 'accept' ? 'text-green-700' : 'text-slate-600'">
                {{ report.action_taken === 'accept' ? '✅ Prihvaćeno — tema obrisana' : '❌ Zanemareno' }}
              </p>
              <p class="text-sm italic mt-1 text-gray-700">
                <strong>Obrazloženje:</strong> {{ report.admin_explanation }}
              </p>
            </div>
          </div>

          <div class="flex-shrink-0">
            <button
              @click="handleReopenReport(report.id || report.report_id)"
              :disabled="reopeningId === (report.id || report.report_id)"
              class="flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg border border-amber-300 text-amber-600 bg-amber-50 hover:bg-amber-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap cursor-pointer"
              title="Vrati ovu prijavu u aktivne za ponovni pregled"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M7.793 2.232a.75.75 0 0 1-.025 1.06L3.622 7.25h10.003a5.375 5.375 0 0 1 0 10.75H10.75a.75.75 0 0 1 0-1.5h2.875a3.875 3.875 0 0 0 0-7.75H3.622l4.146 3.957a.75.75 0 0 1-1.036 1.085l-5.5-5.25a.75.75 0 0 1 0-1.085l5.5-5.25a.75.75 0 0 1 1.06.025Z" clip-rule="evenodd" />
              </svg>
              {{ reopeningId === (report.id || report.report_id) ? 'Vraćam...' : 'Vrati u aktivne' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showAnnouncementModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl w-96 max-w-full shadow-2xl">
        <h2 class="text-xl font-bold mb-4 flex gap-2"><span>📢</span> Novo Obavještenje</h2>
        <label class="block mb-2 text-sm font-bold text-gray-700">Naslov</label>
        <input v-model="newAnnTitle" type="text" class="w-full border rounded p-2 mb-4 focus:ring-2 focus:ring-orange-400 outline-none" placeholder="Kratak naslov" />
        <label class="block mb-2 text-sm font-bold text-gray-700">Sadržaj</label>
        <textarea v-model="newAnnContent" class="w-full border rounded p-2 mb-4 h-24 focus:ring-2 focus:ring-orange-400 outline-none" placeholder="Tekst obavještenja..."></textarea>
        <label class="block mb-2 text-sm font-bold text-gray-700">Trajanje (u danima)</label>
        <input v-model.number="durationDays" type="number" min="0" class="w-full border rounded p-2 mb-6 focus:ring-2 focus:ring-orange-400 outline-none" placeholder="0 = Beskonačno" />
        <div class="flex justify-end gap-3">
          <button @click="showAnnouncementModal = false" class="px-4 py-2 bg-gray-200 rounded text-gray-800 hover:bg-gray-300 transition-colors cursor-pointer border-none">Otkaži</button>
          <button @click="postAnnouncement" class="px-4 py-2 bg-orange-500 text-white rounded font-bold hover:bg-orange-600 transition-colors cursor-pointer border-none">Objavi</button>
        </div>
      </div>
    </div>

    <div v-if="showReportModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl w-full max-w-md shadow-2xl">
        <h2 class="text-xl font-bold mb-4">
          {{ handlingAction === 'accept' ? '✅ Prihvati prijavu' : '❌ Zanemari prijavu' }}
        </h2>
        <p class="text-sm text-gray-600 mb-4">
          Molimo vas da unesete obrazloženje zašto ste odlučili da 
          {{ handlingAction === 'accept' ? 'prihvatite (i obrišete temu)' : 'zanemarite' }} ovu prijavu.
          Ovo će biti sačuvano u evidenciji.
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
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded font-medium transition-colors cursor-pointer border-none"
          >
            Otkaži
          </button>
          <button 
            @click="submitReportAction" 
            class="px-5 py-2 text-white rounded font-bold transition-colors cursor-pointer border-none"
            :class="handlingAction === 'accept' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'"
          >
            Završi
          </button>
        </div>
      </div>
    </div>
  </div>
</template>