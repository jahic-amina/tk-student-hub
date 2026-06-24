<template>
  <div class="min-h-screen bg-gray-50 dark:bg-slate-900 font-sans text-gray-800 dark:text-slate-200 transition-colors duration-200">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8 md:py-12">

      <div class="flex justify-between items-center mb-6">
        <router-link to="/ads" class="text-sm font-bold text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 transition">
          ← Nazad na listu oglasa
        </router-link>
        
        <div v-if="isOwner && !isEditing && company" class="flex gap-2">
          <button @click="startEdit" class="px-4 py-2 text-sm font-bold bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 rounded-xl hover:bg-gray-50 dark:hover:bg-slate-700 transition shadow-sm border-none cursor-pointer">
            ⚙️ Uredi profil
          </button>
          <button @click="isCreatingAd = true" class="px-4 py-2 text-sm font-bold bg-orange-600 dark:bg-orange-500 text-white rounded-xl hover:bg-orange-700 dark:hover:bg-orange-600 transition shadow-sm border-none cursor-pointer">
            ➕ Novi oglas
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-center py-12 text-gray-500 dark:text-slate-400 text-sm font-medium">
        Učitavanje podataka o kompaniji...
      </div>

      <div v-else-if="errorMessage" class="p-6 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 rounded-2xl text-red-700 dark:text-red-400 text-sm mb-4">
        {{ errorMessage }}
      </div>

      <template v-else-if="company">

        <!-- View Company Profile -->
        <div v-if="!isEditing" class="bg-white dark:bg-slate-800 rounded-3xl border border-gray-100 dark:border-slate-700/50 shadow-sm p-6 sm:p-8 mb-8">
          <div class="flex flex-col sm:flex-row gap-6 items-start">
            <div class="flex-shrink-0">
              <img
                v-if="company.logo_path"
                :src="logoUrl"
                :alt="company.company_name"
                class="w-20 h-20 object-contain rounded-2xl border border-gray-100 dark:border-slate-700 bg-white dark:bg-slate-900"
              />
              <div
                v-else
                class="w-20 h-20 rounded-2xl border border-gray-100 dark:border-slate-700 bg-gray-50 dark:bg-slate-900 flex items-center justify-center text-2xl font-black text-gray-300 dark:text-slate-700"
              >
                {{ company.company_name?.charAt(0) }}
              </div>
            </div>

            <div class="flex-1">
              <div class="flex flex-wrap items-center gap-2 mb-1">
                <h1 class="text-2xl font-black text-gray-900 dark:text-slate-100">{{ company.company_name }}</h1>
                <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-400">
                  Odobrena
                </span>
              </div>
              <p class="text-gray-500 dark:text-slate-400 text-sm leading-relaxed mt-2">{{ company.description || 'Nema unesenog opisa.' }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-6 pt-6 border-t border-gray-100 dark:border-slate-700/60 text-sm">
            <div>
              <p class="text-xs text-gray-400 dark:text-slate-500 font-semibold uppercase tracking-wide mb-1">Email</p>
              <a :href="`mailto:${company.email}`" class="text-orange-500 dark:text-orange-400 hover:underline font-medium block truncate">
                {{ company.email }}
              </a>
            </div>
            <div>
              <p class="text-xs text-gray-400 dark:text-slate-500 font-semibold uppercase tracking-wide mb-1">Web</p>
              <a :href="company.website_url" target="_blank" class="text-orange-500 dark:text-orange-400 hover:underline font-medium block truncate">
                {{ company.website_url || 'Nije uneseno' }}
              </a>
            </div>
            <div>
              <p class="text-xs text-gray-400 dark:text-slate-500 font-semibold uppercase tracking-wide mb-1">Adresa</p>
              <p class="text-gray-700 dark:text-slate-300 font-medium truncate">{{ company.address || 'Nije uneseno' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-400 dark:text-slate-500 font-semibold uppercase tracking-wide mb-1">Telefon</p>
              <p class="text-gray-700 dark:text-slate-300 font-medium">{{ company.phone_number || 'Nije uneseno' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-400 dark:text-slate-500 font-semibold uppercase tracking-wide mb-1">JIB / TIN</p>
              <p class="text-gray-700 dark:text-slate-300 font-mono font-medium">{{ company.tin || 'Nije uneseno' }}</p>
            </div>
          </div>
        </div>

        <!-- Edit Profile Form -->
        <div v-else class="bg-white dark:bg-slate-800 rounded-3xl border border-orange-200 dark:border-orange-500/30 shadow-md p-6 sm:p-8 mb-8">
          <h2 class="text-xl font-black text-gray-950 dark:text-slate-100 mb-4">Uredi profil kompanije</h2>
          
          <div v-if="profileError" class="p-4 mb-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 text-red-700 dark:text-red-400 rounded-xl text-xs font-medium">
            {{ profileError }}
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Naziv kompanije</label>
              <input v-model="editForm.company_name" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Opis kompanije</label>
              <textarea v-model="editForm.description" rows="3" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500"></textarea>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Broj telefona</label>
                <input v-model="editForm.phone_number" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Web stranica (URL)</label>
                <input v-model="editForm.website_url" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Adresa</label>
                <input v-model="editForm.address" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">JIB / TIN</label>
                <input v-model="editForm.tin" type="text" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
            </div>
            <div class="flex justify-end gap-2 pt-4 border-t border-gray-100 dark:border-slate-700/60">
              <button @click="isEditing = false" class="px-4 py-2 text-sm font-semibold text-gray-500 dark:text-slate-400 hover:text-gray-700 dark:hover:text-slate-300 bg-transparent border-none cursor-pointer">Odustani</button>
              <button @click="saveProfile" :disabled="saving" class="px-5 py-2 text-sm font-bold bg-orange-600 dark:bg-orange-500 text-white rounded-xl hover:bg-orange-700 dark:hover:bg-orange-600 disabled:opacity-50 border-none cursor-pointer">
                {{ saving ? 'Spašavanje...' : 'Spasi izmjene' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Ads Section -->
        <div>
          <h2 class="text-lg font-bold text-gray-900 dark:text-slate-100 mb-4 flex items-center gap-2">
            💼 Aktivni oglasi 
            <span class="text-gray-400 dark:text-slate-500 font-medium text-base">({{ ads.length }})</span>
          </h2>

          <div v-if="ads.length === 0" class="text-center py-10 px-4 bg-white dark:bg-slate-800 rounded-2xl border border-dashed border-gray-200 dark:border-slate-700">
            <p class="text-gray-400 dark:text-slate-500 text-sm">Ova kompanija trenutno nema aktivnih oglasa.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <AdCard
              v-for="ad in ads"
              :key="ad.id"
              :ad="ad"
            />
          </div>
        </div>

      </template>

      <!-- Modal: Create New Ad -->
      <div v-if="isCreatingAd" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-slate-800 rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-xl border border-transparent dark:border-slate-700">
          <h3 class="text-xl font-black text-gray-900 dark:text-slate-100 mb-4">Kreiraj novi oglas za praksu</h3>
          
          <div v-if="adError" class="p-4 mb-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 text-red-700 dark:text-red-400 rounded-xl text-xs font-medium">
            {{ adError }}
          </div>

          <div class="space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Naslov pozicije</label>
                <input v-model="adForm.title" type="text" placeholder="npr. Junior Backend Developer" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Tip oglasa</label>
                <select v-model="adForm.type" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500">
                  <option value="internship">Praksa</option>
                  <option value="education">Edukacija</option>
                  <option value="scholarship">Stipendija</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <div class="col-span-1">
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Oblast</label>
                <input v-model="adForm.field" type="text" placeholder="npr. IT" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Lokacija</label>
                <input v-model="adForm.location" type="text" placeholder="Sarajevo" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div class="col-span-1">
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Rok prijave</label>
                <input v-model="adForm.deadline" type="date" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Opis posla i zadataka</label>
              <textarea v-model="adForm.description" rows="3" placeholder="Unesite detaljan opis prakse..." class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500"></textarea>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Trajanje (mj.)</label>
                <input v-model.number="adForm.duration_months" type="number" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Broj mjesta</label>
                <input v-model.number="adForm.spots" type="number" class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 dark:text-slate-400 uppercase mb-1">Kompenzacija</label>
                <input
                  v-if="!kompenzacijaPoDogovoru"
                  v-model.number="adForm.compensation"
                  type="number"
                  class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 rounded-xl text-sm text-gray-900 dark:text-slate-100 focus:outline-none focus:border-orange-500"
                />
                <div
                  v-else
                  class="w-full px-4 py-2 border border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-800 rounded-xl text-sm text-gray-400 dark:text-slate-500"
                >
                  Po dogovoru
                </div>
                <label class="flex items-center gap-2 mt-1 cursor-pointer">
                  <input
                    type="checkbox"
                    v-model="kompenzacijaPoDogovoru"
                    @change="kompenzacijaPoDogovoru ? adForm.compensation = null : null"
                    class="accent-orange-500"
                  />
                  <span class="text-xs text-gray-500 dark:text-slate-400">Po dogovoru</span>
                </label>
              </div>
            </div>

            <div class="flex justify-end gap-2 pt-4 border-t border-gray-100 dark:border-slate-700/60 mt-6">
              <button @click="isCreatingAd = false" class="px-4 py-2 text-sm font-semibold text-gray-500 dark:text-slate-400 hover:text-gray-700 dark:hover:text-slate-300 bg-transparent border-none cursor-pointer">Zatvori</button>
              <button @click="createAd" :disabled="saving" class="px-5 py-2 text-sm font-bold bg-orange-600 dark:bg-orange-500 text-white rounded-xl hover:bg-orange-700 dark:hover:bg-orange-600 disabled:opacity-50 border-none cursor-pointer">
                {{ saving ? 'Objavljivanje...' : 'Objavi oglas' }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import AdCard from '../../components/ads/AdCard.vue'
import { getCompanyById, getAdsByCompany } from '../../services/api.js'
import { mapAd } from '../../services/utils.js'

const BASE_URL = 'http://127.0.0.1:8000'

export default {
  name: 'CompanyView',
  components: { AdCard },
  data() {
    return {
      loading: false,
      saving: false,
      errorMessage: '',
      profileError: '', 
      adError: '',      
      company: null,
      kompenzacijaPoDogovoru: false,
      ads: [],
      
      loggedInCompanyId: null,
      hasCompanyToken: false,
      
      isEditing: false,
      isCreatingAd: false,
      
      editForm: {
        company_name: '',
        description: '',
        website_url: '',
        address: '',
        phone_number: '',
        tin: ''
      },
      
      adForm: {
        title: '',
        type: 'internship',
        field: '',
        location: '',
        description: '',
        duration_months: 3,
        compensation: 300,
        spots: 1,
        deadline: ''
      }
    }
  },
  computed: {
    logoUrl() {
      return `${BASE_URL}/${this.company?.logo_path}`
    },
    isOwner() {
      return this.hasCompanyToken && Number(this.loggedInCompanyId) === Number(this.$route.params.id)
    }
  },
  methods: {
    async fetchCompany() {
      this.loading = true
      this.errorMessage = ''
      const companyId = Number(this.$route.params.id)
      let company, ads

      try {
        [company, ads] = await Promise.all([
          getCompanyById(companyId),
          getAdsByCompany(companyId)
        ])
      } catch (err) {
        this.errorMessage = 'Ne mogu učitati podatke o kompaniji.'
        this.loading = false
        return
      }

      this.company = company
      this.ads = (ads || []).map(ad => mapAd(ad, company.company_name))
      this.loading = false
    },

    startEdit() {
      this.editForm.company_name = this.company.company_name
      this.editForm.description = this.company.description
      this.editForm.website_url = this.company.website_url
      this.editForm.address = this.company.address
      this.editForm.phone_number = this.company.phone_number || ''
      this.editForm.tin = this.company.tin || ''
      this.profileError = ''
      this.isEditing = true
    },

    async saveProfile() {
      this.saving = true;
      this.profileError = '';
      const token = localStorage.getItem('company_token');
      try {
        const response = await fetch(`${BASE_URL}/companies/${this.company.id}`, {
          method: 'PATCH', 
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            company_name: this.editForm.company_name,
            description: this.editForm.description,
            website_url: this.editForm.website_url || null,
            address: this.editForm.address || null,
            phone_number: this.editForm.phone_number || null,
            tin: this.editForm.tin || null
          })
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          let backendMsg = "Server je odbio zahtjev.";
          if (errorData.detail) {
            backendMsg = Array.isArray(errorData.detail) 
              ? errorData.detail.map(e => `${e.loc[e.loc.length-1]}: ${e.msg}`).join(' | ') 
              : JSON.stringify(errorData.detail);
          }
          throw new Error(`Kod ${response.status}: ${backendMsg}`);
        }

        this.company = { ...this.company, ...this.editForm };
        this.isEditing = false;
        
      } catch (err) {
        console.error(err);
        this.profileError = err.message;
      } finally {
        this.saving = false;
      }
    },

    async createAd() {
      this.saving = true;
      this.adError = '';
      const token = localStorage.getItem('company_token');
      
      const defaultDeadline = new Date(new Date().getTime() + 30*24*60*60*1000).toISOString().split('T')[0];

      try {
        const response = await fetch(`${BASE_URL}/ads`, { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            title: this.adForm.title,
            type: this.adForm.type, 
            field: this.adForm.field,
            location: this.adForm.location,
            description: this.adForm.description,
            duration_months: Number(this.adForm.duration_months) || 3,
            compensation: this.kompenzacijaPoDogovoru ? null : (Number(this.adForm.compensation) || 0),
            compensation_negotiable: this.kompenzacijaPoDogovoru,
            spots: Number(this.adForm.spots) || 1,
            company_id: this.company.id, 
            deadline: this.adForm.deadline || defaultDeadline 
          })
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          let backendMsg = "Server je odbio kreiranje.";
          if (errorData.detail) {
            backendMsg = Array.isArray(errorData.detail) 
              ? errorData.detail.map(e => `${e.loc[e.loc.length-1]}: ${e.msg}`).join(' | ') 
              : JSON.stringify(errorData.detail);
          }
          throw new Error(`Kod ${response.status}: ${backendMsg}`);
        }

        const createdAd = await response.json();
        this.isCreatingAd = false;
        
        const newMappedAd = mapAd(createdAd, this.company.company_name);
        this.ads.unshift(newMappedAd);

        await this.fetchCompany(); 
        
        this.adForm = { 
          title: '', 
          type: 'internship',
          field: '', 
          location: '', 
          description: '', 
          duration_months: 3, 
          compensation: 300, 
          spots: 1,
          deadline: ''
        };
        this.kompenzacijaPoDogovoru = false;
        
      } catch (err) {
        console.error(err);
        this.adError = err.message;
      } finally {
        this.saving = false;
      }
    }
  },
  mounted() {
    this.fetchCompany()
    this.hasCompanyToken = !!localStorage.getItem('company_token')
    this.loggedInCompanyId = localStorage.getItem('company_id')
  }
}
</script>