<script setup>
import { ref, onMounted, computed } from 'vue';
import { 
  getGuidelines, 
  createGuideline, 
  updateGuideline, 
  deleteGuideline 
} from '../services/forum_admin.js';

const guidelines = ref([]);
const isLoading = ref(true);

// Provjera da li je korisnik admin
const isAdmin = computed(() => localStorage.getItem('role') === 'admin');

// Stanje modala
const showModal = ref(false);
const isEditing = ref(false);
const formError = ref('');
const isSubmitting = ref(false);

// Forma za smjernicu
const formData = ref({
  id: null,
  title: '',
  content: '',
  order: 0
});

const ucitajPravila = async () => {
  isLoading.value = true;
  try {
    const data = await getGuidelines();
    // Sortiranje po 'order' polju (za svaki slučaj, iako backend već sortira)
    guidelines.value = data.sort((a, b) => a.order - b.order);
  } catch (error) {
    console.error("Greška pri učitavanju pravila:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  ucitajPravila();
});

// Otvaranje modala za kreiranje
const otvoriModalZaDodavanje = () => {
  isEditing.value = false;
  formError.value = '';
  formData.value = { id: null, title: '', content: '', order: guidelines.value.length + 1 };
  showModal.value = true;
};

// Otvaranje modala za editovanje
const otvoriModalZaIzmjenu = (pravilo) => {
  isEditing.value = true;
  formError.value = '';
  formData.value = { ...pravilo };
  showModal.value = true;
};

// Zтваranje modala
const zatvoriModal = () => {
  showModal.value = false;
  formData.value = { id: null, title: '', content: '', order: 0 };
};

// Spašavanje (Kreiranje ili Izmjena)
const spasiPravilo = async () => {
  if (!formData.value.title.trim() || !formData.value.content.trim()) {
    formError.value = "Naslov i sadržaj su obavezni.";
    return;
  }

  isSubmitting.value = true;
  formError.value = '';

  try {
    if (isEditing.value) {
      await updateGuideline(formData.value.id, {
        title: formData.value.title,
        content: formData.value.content,
        order: formData.value.order
      });
    } else {
      await createGuideline(formData.value.title, formData.value.content, formData.value.order);
    }
    await ucitajPravila();
    zatvoriModal();
  } catch (error) {
    formError.value = error.message || "Došlo je do greške prilikom spašavanja.";
  } finally {
    isSubmitting.value = false;
  }
};

// Brisanje
const obrisiPravilo = async (id) => {
  if (!confirm("Da li ste sigurni da želite obrisati ovo pravilo?")) return;
  
  try {
    await deleteGuideline(id);
    await ucitajPravila();
  } catch (error) {
    alert("Greška pri brisanju: " + error.message);
  }
};
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 shadow-sm overflow-hidden mb-4">
    <div class="bg-gray-50 dark:bg-slate-800 border-b border-gray-100 dark:border-slate-700 p-3 flex justify-between items-center">
      <h3 class="text-[13px] font-extrabold text-slate-800 dark:text-slate-200 uppercase tracking-wide flex items-center gap-1.5">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-emerald-500">
          <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
        </svg>
        Pravila Foruma
      </h3>
      <button 
        v-if="isAdmin" 
        @click="otvoriModalZaDodavanje"
        class="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 dark:hover:text-emerald-300 bg-emerald-50 dark:bg-emerald-900/30 p-1 rounded-md transition-colors"
        title="Dodaj novo pravilo"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
      </button>
    </div>

    <div class="p-3">
      <div v-if="isLoading" class="flex justify-center py-4">
        <div class="w-5 h-5 border-2 border-gray-300 border-t-emerald-500 rounded-full animate-spin"></div>
      </div>
      
      <div v-else-if="guidelines.length === 0" class="text-center py-4 text-xs text-slate-500">
        Nema definisanih pravila.
      </div>
      
      <div v-else class="space-y-3">
        <div 
          v-for="(pravilo, index) in guidelines" 
          :key="pravilo.id"
          class="group relative pl-2 border-l-2 border-emerald-500/30 hover:border-emerald-500 transition-colors"
        >
          <div class="flex justify-between items-start gap-2">
            <h4 class="text-xs font-bold text-slate-800 dark:text-slate-200">
              {{ index + 1 }}. {{ pravilo.title }}
            </h4>
            <div v-if="isAdmin" class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
              <button @click="otvoriModalZaIzmjenu(pravilo)" class="text-slate-400 hover:text-amber-500">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5"><path d="M5.433 13.917l1.262-3.155A4 4 0 017.58 9.42l6.92-6.918a2.121 2.121 0 013 3l-6.92 6.918c-.383.383-.84.685-1.343.886l-3.154 1.262a.5.5 0 01-.65-.65z" /><path d="M3.5 5.75c0-.69.56-1.25 1.25-1.25H10A.75.75 0 0010 3H4.75A2.75 2.75 0 002 5.75v9.5A2.75 2.75 0 004.75 18h9.5A2.75 2.75 0 0017 15.25V10a.75.75 0 00-1.5 0v5.25c0 .69-.56 1.25-1.25 1.25h-9.5c-.69 0-1.25-.56-1.25-1.25v-9.5z" /></svg>
              </button>
              <button @click="obrisiPravilo(pravilo.id)" class="text-slate-400 hover:text-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5"><path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.52.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clip-rule="evenodd" /></svg>
              </button>
            </div>
          </div>
          <p class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5 leading-tight">
            {{ pravilo.content }}
          </p>
        </div>
      </div>
    </div>

    <div v-if="showModal && isAdmin" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-slate-800 p-5 rounded-xl w-full max-w-sm shadow-2xl border border-gray-100 dark:border-slate-700">
        <h2 class="text-sm font-bold mb-4 text-slate-800 dark:text-white uppercase tracking-wider">
          {{ isEditing ? 'Uredi pravilo' : 'Novo pravilo' }}
        </h2>
        
        <div v-if="formError" class="mb-3 p-2 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100">
          {{ formError }}
        </div>

        <div class="space-y-3">
          <div>
            <label class="block mb-1 text-[11px] font-bold text-slate-500 uppercase">Naslov</label>
            <input 
              v-model="formData.title" 
              type="text" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2 text-xs bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
              placeholder="Npr. Zabranjeno vrijeđanje" 
            />
          </div>
          
          <div>
            <label class="block mb-1 text-[11px] font-bold text-slate-500 uppercase">Sadržaj pravila</label>
            <textarea 
              v-model="formData.content" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2 text-xs bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-white h-20 focus:ring-2 focus:ring-emerald-500 focus:outline-none resize-none" 
              placeholder="Opišite detaljno šta je dozvoljeno a šta ne..."
            ></textarea>
          </div>
          
          <div>
            <label class="block mb-1 text-[11px] font-bold text-slate-500 uppercase">Redni broj (Prioritet)</label>
            <input 
              v-model.number="formData.order" 
              type="number" 
              class="w-full border border-gray-300 dark:border-slate-600 rounded-lg p-2 text-xs bg-gray-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none" 
            />
          </div>
        </div>
        
        <div class="flex justify-end gap-2 mt-5">
          <button 
            @click="zatvoriModal" 
            :disabled="isSubmitting"
            class="px-3 py-1.5 bg-gray-100 dark:bg-slate-700 hover:bg-gray-200 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-bold transition-colors"
          >
            Otkaži
          </button>
          <button 
            @click="spasiPravilo" 
            :disabled="isSubmitting"
            class="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold shadow-sm transition-colors disabled:opacity-50"
          >
            {{ isSubmitting ? 'Spašavanje...' : 'Spasi' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>