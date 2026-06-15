<script setup>
import { ref, onMounted, computed } from 'vue';
import { getActiveAnnouncements } from '../services/forum'; 
import { updateAnnouncement, deleteAnnouncement } from '../services/forum_admin';

const activeAnnouncements = ref([]);
const isLoading = ref(true);

const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

//za edit prompt
const showEditModal = ref(false);
const selectedAnn = ref(null);
const editTitle = ref('');
const editContent = ref('');
const editDurationDays = ref(0);
const isSubmittingEdit = ref(false);

//za delete prompt
const showDeleteModal = ref(false);
const annToDelete = ref(null);
const isSubmittingDelete = ref(false);

const fetchAnnouncements = async () => {
  try {
    activeAnnouncements.value = await getActiveAnnouncements();
  } catch (error) {
    console.error("Greška pri učitavanju globalnih obavještenja:", error);
  }
};

onMounted(async () => {
  try {
    await fetchAnnouncements();
  } finally {
    isLoading.value = false;
  }
});

const openEditModal = (ann) => {
  selectedAnn.value = ann;
  editTitle.value = ann.title || '';
  editContent.value = ann.content || '';
  
  if (ann.expires_at && ann.created_at) {
    const start = new Date(ann.created_at);
    const end = new Date(ann.expires_at);
    const diffTime = end - start;
    editDurationDays.value = Math.max(1, Math.round(diffTime / (1000 * 60 * 60 * 24)));
  } else {
    editDurationDays.value = 0; 
  }
  
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  selectedAnn.value = null;
};

const handleUpdateAnnouncement = async () => {
  if (!editTitle.value.trim() || !editContent.value.trim()) return;
  isSubmittingEdit.value = true;
  try {
    const payload = {
      title: editTitle.value,
      content: editContent.value,
      duration_days: editDurationDays.value
    };
    const response = await updateAnnouncement(selectedAnn.value.id, payload);
    if (response) {
      await fetchAnnouncements();
      closeEditModal();
    }
  } catch (error) {
    console.error("Greška pri ažuriranju obavještenja:", error);
  } finally {
    isSubmittingEdit.value = false;
  }
};

const openDeleteModal = (ann) => {
  annToDelete.value = ann;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  annToDelete.value = null;
};

const handleDeleteAnnouncement = async () => {
  if (!annToDelete.value) return;
  isSubmittingDelete.value = true;
  try {
    await deleteAnnouncement(annToDelete.value.id);
    await fetchAnnouncements();
    closeDeleteModal();
  } catch (error) {
    console.error("Greška pri brisanju obavještenja:", error);
  } finally {
    isSubmittingDelete.value = false;
  }
};

</script>

<template>
  <div v-if="activeAnnouncements.length > 0" class="w-full space-y-3 mb-6">
    <div 
      v-for="ann in activeAnnouncements" 
      :key="ann.id"
      class="bg-orange-50/90 dark:bg-slate-800/95 border border-orange-200 dark:border-orange-900/40 rounded-2xl p-5 shadow-sm flex items-start gap-4 transition-all duration-300 backdrop-blur-sm"
    >
      <div class="p-2.5 bg-orange-100 dark:bg-orange-950/40 text-orange-600 dark:text-orange-400 rounded-xl flex items-center justify-center text-xl shadow-inner select-none">
        📢
      </div>
      
      <div class="flex-1">
        <h3 class="text-base font-bold text-slate-800 dark:text-slate-100 tracking-tight leading-snug">
          {{ ann.title || 'Zvanično obavještenje administratora' }}
        </h3>
        <p class="text-sm text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed font-medium whitespace-pre-line">
          {{ ann.content }}
        </p>
      </div>

      <div v-if="isAdmin" class="flex flex-col gap-2 self-center shrink-0 ml-2">
        <button 
          @click="openEditModal(ann)" 
          class="px-3 py-1.5 text-xs font-bold text-orange-700 bg-orange-100/80 hover:bg-orange-200 dark:text-orange-300 dark:bg-slate-700 dark:hover:bg-slate-600/80 rounded-xl transition-colors flex items-center justify-center gap-1 shadow-sm"
          title="Uredi obavještenje"
        >
          ✏️ <span>Uredi</span>
        </button>
        <button 
          @click="openDeleteModal(ann)" 
          class="px-3 py-1.5 text-xs font-bold text-red-700 bg-red-100/70 hover:bg-red-200 dark:text-red-400 dark:bg-slate-700/50 dark:hover:bg-slate-600 rounded-xl transition-colors flex items-center justify-center gap-1 shadow-sm"
          title="Obriši obavještenje"
        >
          🗑️ <span>Obriši</span>
        </button>
      </div>
    </div>
  </div>

  <div v-if="showEditModal" class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 backdrop-blur-sm">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl w-full max-w-md shadow-2xl text-slate-800 dark:text-slate-100 mx-4">
      <h2 class="text-xl font-bold mb-4 flex items-center gap-2 text-orange-600 dark:text-orange-400">
        ✏️ Uredi obavještenje
      </h2>
      
      <div class="space-y-4">
        <div>
          <label class="block mb-1 text-sm font-bold text-slate-700 dark:text-slate-300">Naslov</label>
          <input 
            v-model="editTitle" 
            type="text"
            class="w-full border dark:border-slate-700 dark:bg-slate-800 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-orange-400 outline-none transition-all"
            placeholder="Unesite naslov..."
          />
        </div>
        
        <div>
          <label class="block mb-1 text-sm font-bold text-slate-700 dark:text-slate-300">Sadržaj</label>
          <textarea 
            v-model="editContent" 
            class="w-full border dark:border-slate-700 dark:bg-slate-800 rounded-xl p-2.5 text-sm h-32 focus:ring-2 focus:ring-orange-400 outline-none transition-all resize-none"
            placeholder="Unesite sadržaj obavještenja..."
          ></textarea>
        </div>
        
        <div>
          <label class="block mb-1 text-sm font-bold text-slate-700 dark:text-slate-300">Trajanje (u danima - 0 za beskonačno)</label>
          <input 
            v-model.number="editDurationDays" 
            type="number"
            min="0"
            class="w-full border dark:border-slate-700 dark:bg-slate-800 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-orange-400 outline-none transition-all"
          />
        </div>
      </div>
      
      <div class="flex justify-end gap-3 mt-6">
        <button 
          @click="closeEditModal" 
          class="px-4 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-sm font-medium transition-colors"
          :disabled="isSubmittingEdit"
        >
          Otkaži
        </button>
        <button 
          @click="handleUpdateAnnouncement" 
          class="px-5 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-xl text-sm font-bold transition-colors shadow-sm"
          :disabled="isSubmittingEdit"
        >
          {{ isSubmittingEdit ? 'Spremanje...' : 'Spremi izmjene' }}
        </button>
      </div>
    </div>
  </div>

  <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex justify-center items-center z-50 backdrop-blur-sm">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl w-full max-w-sm shadow-2xl text-slate-800 dark:text-slate-100 mx-4 text-center">
      <div class="w-12 h-12 bg-red-100 dark:bg-red-950/40 text-red-600 dark:text-red-400 rounded-full flex items-center justify-center text-2xl mx-auto mb-3">
        🗑️
      </div>
      <h2 class="text-lg font-bold mb-2">Potvrda brisanja</h2>
      <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">
        Jeste li sigurni da želite obrisati ovo obavještenje?
      </p>
      
      <div class="flex justify-center gap-4">
        <button 
          @click="closeDeleteModal" 
          class="px-5 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-sm font-medium transition-colors w-24"
          :disabled="isSubmittingDelete"
        >
          Otkazuj
        </button>
        <button 
          @click="handleDeleteAnnouncement" 
          class="px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm font-bold transition-colors shadow-sm w-24"
          :disabled="isSubmittingDelete"
        >
          {{ isSubmittingDelete ? '...' : 'Obriši' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/*Vizuelni efekat pulsiranja za nova obavjestenja*/
.animate-pulse-once {
  animation: pulseOnce 1.5s ease-in-out 1;
}
@keyframes pulseOnce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.01); }
}
</style>