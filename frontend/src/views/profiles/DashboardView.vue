<template>
  <main class="min-h-screen bg-gradient-to-br from-blue-50 via-gray-50 to-white px-6 py-8">
    <section class="mx-auto max-w-6xl">
      <div class="mb-8">
        <p class="text-sm font-medium text-blue-600">TK Student Hub</p>
        <h1 class="mt-2 text-3xl font-bold text-gray-900">
          Moj studentski dashboard
        </h1>
        <p class="mt-2 text-gray-600">
          Personalizovani pregled nakon prijave — bez ponavljanja glavne navigacije.
        </p>
      </div>

      <div v-if="loading" class="rounded-2xl bg-white p-6 shadow">
        Učitavanje dashboarda...
      </div>

      <div v-else-if="error" class="rounded-2xl bg-red-50 p-6 text-red-700 shadow">
        {{ error }}
      </div>

      <div v-else class="space-y-6">
        <section class="rounded-2xl bg-white p-6 shadow">
          <div class="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
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
                  Dobrodošao/la, {{ dashboard.student.full_name }}
                </h2>
                <p class="text-gray-600">{{ dashboard.student.email }}</p>
                <p class="mt-1 text-sm text-gray-500">
                  Uloga: {{ dashboard.student.role }}
                </p>
              </div>
            </div>

            <router-link
              to="/profiles"
              class="inline-flex justify-center rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
            >
              Uredi profil
            </router-link>
          </div>

          <p class="mt-5 text-gray-700">
            {{ dashboard.student.biografija || "Još nisi dodao/la biografiju. Kratak opis može pomoći da profil izgleda potpunije." }}
          </p>
        </section>

        <section class="grid gap-4 md:grid-cols-3">
          <div
            v-for="item in dashboard.student_overview.items"
            :key="item.title"
            class="rounded-2xl bg-white p-5 shadow"
          >
            <p class="text-sm text-gray-500">{{ item.title }}</p>
            <p class="mt-2 text-3xl font-bold text-gray-900">
              {{ item.value }}
            </p>
            <p class="mt-1 text-sm text-gray-500">
              {{ item.description }}
            </p>
          </div>
        </section>

        <section class="rounded-2xl bg-white p-6 shadow">
          <div class="mb-4 flex items-center justify-between">
            <div>
              <h3 class="text-xl font-bold text-gray-900">
                Popunjenost profila
              </h3>
              <p class="text-sm text-gray-500">
                Kompletiran profil olakšava korištenje platforme.
              </p>
            </div>

            <span class="text-2xl font-bold text-blue-600">
              {{ dashboard.profile_status.completion_percent }}%
            </span>
          </div>

          <div class="h-3 overflow-hidden rounded-full bg-gray-100">
            <div
              class="h-full rounded-full bg-blue-600"
              :style="{ width: dashboard.profile_status.completion_percent + '%' }"
            ></div>
          </div>

          <div class="mt-4 grid gap-3 md:grid-cols-3">
            <div
              v-for="item in dashboard.profile_status.items"
              :key="item.label"
              class="rounded-xl border border-gray-200 p-4"
            >
              <p class="font-medium text-gray-900">{{ item.label }}</p>
              <p
                class="mt-1 text-sm"
                :class="item.completed ? 'text-green-600' : 'text-orange-600'"
              >
                {{ item.completed ? "Popunjeno" : "Nije popunjeno" }}
              </p>
            </div>
          </div>
        </section>

        <section class="grid gap-6 lg:grid-cols-2">
          <div class="rounded-2xl bg-white p-6 shadow">
            <h3 class="text-xl font-bold text-gray-900">
              Preporučeni sljedeći koraci
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              Ovo nisu kopije glavnog menija, nego prijedlozi šta bi student mogao uraditi sljedeće.
            </p>

            <div class="mt-5 space-y-4">
              <router-link
                v-for="step in dashboard.next_steps"
                :key="step.title"
                :to="step.path"
                class="block rounded-xl border border-gray-200 p-4 transition hover:border-blue-400 hover:bg-blue-50"
              >
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <h4 class="font-semibold text-gray-900">
                      {{ step.title }}
                    </h4>
                    <p class="mt-1 text-sm text-gray-600">
                      {{ step.description }}
                    </p>
                  </div>

                  <span class="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                    {{ step.priority }}
                  </span>
                </div>
              </router-link>
            </div>
          </div>

          <div class="rounded-2xl bg-white p-6 shadow">
            <h3 class="text-xl font-bold text-gray-900">
              Studentski podsjetnik
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              Kratke stvari koje student može provjeriti nakon prijave.
            </p>

            <ul class="mt-5 space-y-3">
              <li
                v-for="reminder in dashboard.reminders"
                :key="reminder"
                class="rounded-xl bg-gray-50 p-4 text-sm text-gray-700"
              >
                {{ reminder }}
              </li>
            </ul>
          </div>
        </section>

        <section class="rounded-2xl bg-white p-6 shadow">
          <h3 class="text-xl font-bold text-gray-900">
            {{ dashboard.activity.title }}
          </h3>

          <p
            v-if="dashboard.activity.items.length === 0"
            class="mt-3 rounded-xl bg-gray-50 p-4 text-sm text-gray-600"
          >
            {{ dashboard.activity.empty_message }}
          </p>

          <ul v-else class="mt-4 space-y-3">
            <li
              v-for="activity in dashboard.activity.items"
              :key="activity.id"
              class="rounded-xl border border-gray-200 p-4"
            >
              {{ activity.title }}
            </li>
          </ul>
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