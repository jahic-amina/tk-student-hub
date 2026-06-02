<script setup>
import { ref, onMounted } from 'vue';
import { getUsers, changeUserRole, getReports, dismissReport, createAnnouncement, deleteAnnouncement } from '../../services/admin';

const activeTab = ref('reports');
const users = ref([]);
const reports = ref([]);
const newAnnouncement = ref('');

const loadData = async () => {
  if (activeTab.value === 'users') users.value = await getUsers();
  if (activeTab.value === 'reports') reports.value = await getReports();
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
  await createAnnouncement(newAnnouncement.value);
  newAnnouncement.value = '';
  alert('Obavještenje objavljeno!');
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
      <button @click="activeTab = 'announcements'" :class="activeTab === 'announcements' ? 'text-orange-500 border-b-2 border-orange-500 font-bold' : 'text-slate-500'">Postavi Obavještenje</button>
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

    <div v-if="activeTab === 'announcements'" class="bg-white p-6 rounded-xl shadow-sm border">
      <h3 class="font-bold mb-2">Globalno obavještenje za Forum</h3>
      <textarea v-model="newAnnouncement" rows="4" class="w-full border rounded p-2 mb-3 focus:ring focus:ring-orange-200" placeholder="Ukucajte obavještenje koje će se vidjeti na vrhu foruma..."></textarea>
      <button @click="postAnnouncement" class="bg-orange-500 text-white px-4 py-2 rounded font-bold hover:bg-orange-600">Objavi obavještenje</button>
    </div>
  </div>
</template>