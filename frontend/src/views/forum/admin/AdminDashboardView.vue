<script setup>
import { ref, onMounted } from 'vue';
import { 
  getUsers, 
  changeUserRole, 
  getReports, 
  dismissReport, 
  createAnnouncement, 
  deleteAnnouncement,
  getAllAnnouncements,   
  updateAnnouncement     
} from '../../services/admin';

const activeTab = ref('reports');
const users = ref([]);
const reports = ref([]);
const announcements = ref([]); //Lista za prikaz u admin panelu

const newAnnouncement = ref('');
const durationDays = ref(0);   //Default: Beskonačno

const editingAnn = ref(null);  //Prati obavještenje koje trenutno editujemo

const loadData = async () => {
  if (activeTab.value === 'users') users.value = await getUsers();
  if (activeTab.value === 'reports') reports.value = await getReports();
  if (activeTab.value === 'announcements') announcements.value = await getAllAnnouncements();
};

onMounted(() => loadData());

const setRole = async (userId, role) => {
  await changeUserRole(userId, role);
  await loadData();
};

const resolveReport = async (reportId) => {
  await dismissReport(reportId);
  await loadData();
};

const postAnnouncement = async () => {
  if (!newAnnouncement.value.trim()) return;
  await createAnnouncement(newAnnouncement.value, durationDays.value);
  newAnnouncement.value = '';
  durationDays.value = 0;
  alert('Globalno obavještenje uspješno objavljeno!');
  await loadData();
};

const handleDeactivate = async (annId) => {
  if (confirm('Da li ste sigurni da želite deaktivirati ovo obavještenje?')) {
    await deleteAnnouncement(annId);
    await loadData();
  }
};

const startEdit = (ann) => {
  editingAnn.value = { ...ann, duration_days: 0 };
};

const saveEdit = async () => {
  if (!editingAnn.value.content.trim()) return;
  await updateAnnouncement(editingAnn.value.id, {
    content: editingAnn.value.content,
    duration_days: editingAnn.value.duration_days,
    is_active: editingAnn.value.is_active
  });
  editingAnn.value = null;
  alert('Obavještenje uspješno izmijenjeno!');
  await loadData();
};
</script>

<template>
  <div class="min-h-screen p-6 max-w-5xl mx-auto">
    <h1 class="text-3xl font-extrabold text-slate-800 mb-6 flex items-center gap-2">
      <span class="text-red-500">🛡️</span> Admin Panel
    </h1>

    <div class="flex gap-4 mb-6 border-b pb-2">
      <button @click="activeTab = 'reports'; loadData()" :class="activeTab === 'reports' ? 'text-orange-500 border-b-2 border-orange-500 font-bold' : 'text-slate-500'">Prijavljene teme</button>
      <button @click="activeTab = 'users'; loadData()" :class="activeTab === 'users' ? 'text-orange-500 border-b-2 border-orange-500 font-bold' : 'text-slate-500'">Korisnici</button>
      <button @click="activeTab = 'announcements'; loadData()" :class="activeTab === 'announcements' ? 'text-orange-500 border-b-2 border-orange-500 font-bold' : 'text-slate-500'">Upravljanje Obavještenjima</button>
    </div>

    <div v-if="activeTab === 'reports'" class="space-y-4">
      <div v-if="reports.length === 0" class="text-gray-500">Nema prijavljenih tema. Odlično!</div>
      <div v-for="report in reports" :key="report.report_id" class="bg-red-50 border border-red-200 p-4 rounded-xl">
        <div class="flex justify-between items-start mb-2">
          <span class="bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">Razlog: {{ report.reason }}</span>
          <button @click="resolveReport(report.report_id)" class="text-xs bg-white border border-gray-300 px-3 py-1 rounded hover:bg-gray-100">Odbaci prijavu</button>
        </div>
        <h3 class="font-bold text-slate-800">Tema: {{ report.topic.title }}</h3>
        <p class="text-sm text-slate-600 mt-1 truncate">{{ report.topic.content }}</p>
        <router-link :to="`/forum/tema/${report.topic.id}`" class="text-xs text-blue-500 hover:underline mt-2 inline-block">Idi na temu →</router-link>
      </div>
    </div>

    <div v-if="activeTab === 'users'" class="bg-white p-4 rounded-xl shadow-sm border">
      <table class="w-full text-left text-sm text-slate-600">
        <thead class="bg-gray-50 text-slate-800 border-b">
          <tr><th class="p-3">Ime</th><th class="p-3">Email</th><th class="p-3">Status</th><th class="p-3">Akcije</th></tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-b">
            <td class="p-3">{{ user.full_name }}</td>
            <td class="p-3">{{ user.email }}</td>
            <td class="p-3">
              <span :class="user.role === 'admin' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'" class="px-2 py-1 rounded text-xs font-bold uppercase">{{ user.role }}</span>
            </td>
            <td class="p-3 flex gap-2">
              <button v-if="user.role !== 'admin'" @click="setRole(user.id, 'admin')" class="text-xs bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Daj Admina</button>
              <button v-if="user.role === 'admin'" @click="setRole(user.id, 'member')" class="text-xs bg-slate-500 text-white px-2 py-1 rounded hover:bg-slate-600">Ukloni Admina</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="activeTab === 'announcements'" class="space-y-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="font-bold text-lg mb-3 text-slate-800">Kreiraj Novo Globalno Obavještenje</h3>
        <textarea v-model="newAnnouncement" rows="3" class="w-full border rounded p-2 mb-3 focus:ring focus:ring-orange-200" placeholder="Ukucajte obavještenje koje će se fiksirati na vrh foruma..."></textarea>
        
        <div class="flex items-center gap-4 mb-4">
          <label class="text-sm font-semibold text-slate-600">Vrijeme trajanja obavještenja:</label>
          <select v-model="durationDays" class="border rounded p-1.5 bg-gray-50 text-sm">
            <option :value="0">Beskonačno (Dok ga ne obrišem)</option>
            <option :value="3">3 Dana</option>
            <option :value="10">10 Dana</option>
          </select>
        </div>

        <button @click="postAnnouncement" class="bg-orange-500 text-white px-4 py-2 rounded font-bold hover:bg-orange-600 transition-colors">Objavi obavještenje</button>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="font-bold text-lg mb-4 text-slate-800">Prethodna obavještenja</h3>
        <div v-if="announcements.length === 0" class="text-gray-500 text-sm">Nema ranije kreiranih obavještenja.</div>
        
        <div class="space-y-3">
          <div v-for="ann in announcements" :key="ann.id" class="p-4 border rounded-xl bg-slate-50 flex flex-col justify-between md:flex-row md:items-center gap-4">
            
            <div v-if="editingAnn && editingAnn.id === ann.id" class="w-full space-y-2">
              <input v-model="editingAnn.content" type="text" class="w-full border rounded p-2 text-sm bg-white" />
              <div class="flex items-center gap-4 text-xs">
                <select v-model="editingAnn.duration_days" class="border rounded p-1">
                  <option :value="0">Beskonačno</option>
                  <option :value="3">Produži za 3 dana</option>
                  <option :value="10">Produži za 10 dana</option>
                </select>
                <label class="flex items-center gap-1">
                  <input type="checkbox" v-model="editingAnn.is_active" /> Aktivno
                </label>
                <button @click="saveEdit" class="bg-green-600 text-white px-3 py-1 rounded font-bold">Spasi</button>
                <button @click="editingAnn = null" class="bg-gray-400 text-white px-3 py-1 rounded">Odustani</button>
              </div>
            </div>

            <template v-else>
              <div class="flex-1">
                <p class="text-slate-800 font-medium text-sm">{{ ann.content }}</p>
                <div class="flex gap-3 text-xs text-slate-400 mt-1">
                  <span>Status: <b :class="ann.is_active ? 'text-green-600':'text-red-500'">{{ ann.is_active ? 'Aktivno' : 'Deaktivirano' }}</b></span>
                  <span v-if="ann.expires_at">Ističe: {{ new Date(ann.expires_at).toLocaleDateString() }}</span>
                  <span v-else>Ističe: Beskonačno</span>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="startEdit(ann)" class="text-xs border border-blue-400 text-blue-600 px-3 py-1 rounded hover:bg-blue-50">Uredi</button>
                <button v-if="ann.is_active" @click="handleDeactivate(ann.id)" class="text-xs bg-red-100 border border-red-200 text-red-600 px-3 py-1 rounded hover:bg-red-200">Deaktiviraj</button>
              </div>
              </template>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>