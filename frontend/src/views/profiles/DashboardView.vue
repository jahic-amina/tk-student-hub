<template>
  <main class="min-h-screen bg-gray-50 px-6 py-8">
    <section class="mx-auto max-w-6xl">
      <div class="mb-8">
        <p class="text-sm font-medium text-blue-600">TK Student Hub</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">
          Personalizovani dashboard
        </h1>
        <p class="mt-2 text-gray-600">
          Brzi pregled profila, materijala, praksi i forum aktivnosti.
        </p>
      </div>

      <div v-if="loading" class="rounded-xl bg-white p-6 shadow">
        Učitavanje dashboarda...
      </div>

      <div v-else-if="error" class="rounded-xl bg-red-50 p-6 text-red-700 shadow">
        {{ error }}
      </div>

      <div v-else>
        <section class="mb-6 rounded-2xl bg-white p-6 shadow">
          <div class="flex items-center gap-5">
            <img
              v-if="dashboard.student.profilna_slika_url"
              :src="apiBaseUrl + dashboard.student.profilna_slika_url"
              alt="Profilna slika"
              class="h-20 w-20 rounded-full object-cover"
            />

            <div
              v-else
              class="flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-2xl font-bold text-blue-700"
            >
              {{ initials }}
            </div>

            <div>
              <h2 class="text-2xl font-bold text-gray-900">
                Dobro došao/la, {{ dashboard.student.full_name }}
              </h2>
              <p class="text-gray-600">{{ dashboard.student.email }}</p>
              <p class="mt-1 text-sm text-gray-500">
                Uloga: {{ dashboard.student.role }}
              </p>
            </div>
          </div>

          <p class="mt-5 text-gray-700">
            {{ dashboard.student.biografija || "Biografija još nije dodana." }}
          </p>
        </section>

        <section class="mb-6 grid gap-4 md:grid-cols-3">
          <div class="rounded-2xl bg-white p-5 shadow">
            <p class="text-sm text-gray-500">Materijali</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">
              {{ dashboard.summary.materials_count }}
            </p>
          </div>

          <div class="rounded-2xl bg-white p-5 shadow">
            <p class="text-sm text-gray-500">Prakse i edukacije</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">
              {{ dashboard.summary.opportunities_count }}
            </p>
          </div>

          <div class="rounded-2xl bg-white p-5 shadow">
            <p class="text-sm text-gray-500">Forum aktivnosti</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">
              {{ dashboard.summary.forum_activity_count }}
            </p>
          </div>
        </section>

        <section class="rounded-2xl bg-white p-6 shadow">
          <h3 class="mb-4 text-xl font-bold text-gray-900">
            Relevantni sadržaji
          </h3>

          <div class="grid gap-4 md:grid-cols-3">
            <router-link
              v-for="item in dashboard.relevant_content"
              :key="item.title"
              :to="item.path"
              class="rounded-xl border border-gray-200 p-4 transition hover:border-blue-400 hover:bg-blue-50"
            >
              <h4 class="font-semibold text-gray-900">{{ item.title }}</h4>
              <p class="mt-2 text-sm text-gray-600">{{ item.description }}</p>
            </router-link>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"

const apiBaseUrl = "http://127.0.0.1:8000"
const dashboard = ref(null)
const loading = ref(true)
const error = ref("")

const initials = computed(() => {
  const name = dashboard.value?.student?.full_name || "S"
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()
})

onMounted(async () => {
  try {
    const token = localStorage.getItem("token")

    const response = await fetch(`${apiBaseUrl}/dashboard/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error("Dashboard se nije mogao učitati.")
    }

    dashboard.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>