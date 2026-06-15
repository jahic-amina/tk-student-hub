<script setup>
import { ref, onMounted, computed } from 'vue'; 
import { 
  getUsers, 
  changeUserRole, 
  getReports, 
  dismissReport, 
  createAnnouncement, 
  deleteAnnouncement,
  getAllAnnouncements,   
  updateAnnouncement,
  getHandledReports     
} from '../../../services/forum_admin.js'; 

import { handleReportAction, getActiveReports } from '../../../services/forum.js';

const activeTab = ref('reports');
const users = ref([]);
const reports = ref([]);
const handledReports = ref([]); 
const announcements = ref([]); 

// Za novo obavještenje
const showAnnouncementModal = ref(false);
const newAnnTitle = ref('');
const newAnnContent = ref('');
const durationDays = ref(0); 

const editingAnn = ref(null);  

const showReportModal = ref(false);
const handlingReportId = ref(null);
const handlingAction = ref(''); 
const adminExplanation = ref('');

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
    if (activeTab.value === 'reports') reports.value = await getActiveReports() || []; 
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
    await handleReportAction(handlingReportId.value, handlingAction.value, adminExplanation.value);
    
    closeReportModal();
    alert('Prijava je uspješno riješena.');
    await loadData(); 
  } catch (error) {
    alert('Došlo je do greške: ' + error.message);
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
      <button @click="showAnnouncementModal = true" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-6 rounded-lg shadow transition-colors flex gap-2 items-center">
        <span>📢</span> Globalno obavještenje
      </button>
    </div>

    <div class="flex gap-4 mb-6 border-b border-gray-200 pb-2">
      <button @click="activeTab = 'reports'; loadData()" :class="activeTab === 'reports' ? 'border-b-2 border-orange-500 text-orange-600 font-bold' : 'text-gray-500'">Aktivne Prijave</button>
      <button @click="activeTab = 'handled_reports'; loadData()" :class="activeTab === 'handled_reports' ? 'border-b-2 border-orange-500 text-orange-600 font-bold' : 'text-gray-500'">Riješene Prijave</button>
      </div>

    <div v-if="activeTab === 'reports' || activeTab === 'handled_reports'" class="mb-6">
       <input type="text" v-model="searchQuery" placeholder="Pretraži prijave i teme..." class="w-full p-3 rounded border border-gray-300 focus:ring-2 focus:ring-orange-500" />
    </div>

    <div v-if="activeTab === 'reports'">
       <div v-for="report in filteredReports" :key="report.report_id" class="p-4 bg-white shadow rounded mb-4 border-l-4 border-red-500">
           <h3 class="font-bold text-lg">{{ report.topic?.title }}</h3>
           <p class="text-sm text-gray-600 mt-1"><b>Razlog:</b> {{ report.reason }} | <b>Prijavio:</b> {{ report.reporter_name }}</p>
           
           <div class="mt-3 flex gap-2">
              <button @click="openReportModal(report.report_id, 'accept')" class="font-inherit text-sm font-medium border border-green-500 bg-green-50 text-green-700 hover:bg-green-100 px-4 py-1.5 rounded-lg transition-colors">Prihvati</button>
              <button @click="openReportModal(report.report_id, 'dismiss')" class="font-inherit text-sm font-medium border border-red-500 bg-red-50 text-red-700 hover:bg-red-100 px-4 py-1.5 rounded-lg transition-colors">Zanemari</button>
           </div>
       </div>
    </div>

    <div v-if="activeTab === 'handled_reports'">
       <div v-for="report in filteredHandledReports" :key="report.id" class="p-4 border rounded shadow-sm mb-4">
    <h3 class="font-bold">Tema: {{ report.topic?.title }}</h3>
    
    <p class="text-sm text-gray-700 mt-2">
        <strong>Prijavio korisnik:</strong> {{ report.user?.full_name || report.user?.username || 'Nepoznat' }}
    </p>
    <p class="text-sm text-gray-700 mt-1">
        <strong>Razlog prijave:</strong> {{ report.reason }}
    </p>
    
    <div class="mt-3 p-3 rounded" :class="report.action_taken === 'accept' ? 'bg-green-50' : 'bg-red-50'">
        <p class="text-sm font-semibold" :class="report.action_taken === 'accept' ? 'text-green-700' : 'text-red-700'">
            Status: {{ report.action_taken === 'accept' ? 'Prihvaćeno (Tema obrisana)' : 'Odbijeno (Zanemareno)' }}
        </p>
        <p class="text-sm italic mt-1 text-gray-800">
            <strong>Adminovo obrazloženje:</strong> {{ report.admin_explanation }}
        </p>
    </div>
</div>
    </div>

    <div v-if="showAnnouncementModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-xl w-96 max-w-full shadow-2xl">
        <h2 class="text-xl font-bold mb-4 flex gap-2"><span>📢</span> Novo Obavještenje</h2>
        
        <label class="block mb-2 text-sm font-bold text-gray-700">Naslov</label>
        <input v-model="newAnnTitle" type="text" class="w-full border rounded p-2 mb-4" placeholder="Kratak naslov" />
        
        <label class="block mb-2 text-sm font-bold text-gray-700">Sadržaj (Body)</label>
        <textarea v-model="newAnnContent" class="w-full border rounded p-2 mb-4 h-24" placeholder="Tekst obavještenja..."></textarea>
        
        <label class="block mb-2 text-sm font-bold text-gray-700">Trajanje (u danima)</label>
        <input v-model.number="durationDays" type="number" min="0" class="w-full border rounded p-2 mb-6" placeholder="0 = Beskonačno" />
        
        <div class="flex justify-end gap-3">
          <button @click="showAnnouncementModal = false" class="px-4 py-2 bg-gray-200 rounded text-gray-800">Otkaži</button>
          <button @click="postAnnouncement" class="px-4 py-2 bg-orange-500 text-white rounded font-bold hover:bg-orange-600">Objavi</button>
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