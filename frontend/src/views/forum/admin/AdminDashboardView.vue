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
} from '../../services/forum_admin.js'; 

import { handleReportAction } from '../../services/forum.js';

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

const resolveReport = async (reportId, action) => {
  await handleReportAction(reportId, action);
  await loadData(); 
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
              <button @click="resolveReport(report.report_id, 'resolve')" class="bg-green-500 text-white px-4 py-1 rounded text-sm">Prihvati (Obrisat će/Sankcionisati)</button>
              <button @click="resolveReport(report.report_id, 'dismiss')" class="bg-gray-500 text-white px-4 py-1 rounded text-sm">Odbaci</button>
           </div>
       </div>
    </div>

    <div v-if="activeTab === 'handled_reports'">
       <div v-for="report in filteredHandledReports" :key="report.report_id" class="p-4 bg-gray-50 shadow rounded mb-4 border-l-4 border-gray-400">
           <h3 class="font-bold text-lg text-gray-700">{{ report.topic?.title }}</h3>
           <p class="text-sm text-gray-600 mt-1"><b>Razlog:</b> {{ report.reason }}</p>
           <p class="text-xs font-bold mt-2 uppercase" :class="report.status === 'resolved' ? 'text-green-600' : 'text-gray-500'">Status: {{ report.status }}</p>
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
  </div>
</template>