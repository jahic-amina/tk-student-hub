<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-slate-900 transition-colors duration-300">
        <div class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-md w-full max-w-md border border-gray-100 dark:border-slate-700">

            <h1 class="text-2xl font-bold text-primary dark:text-orange-500 mb-2">
                Registracija
            </h1>

            <p class="text-gray-500 dark:text-slate-400 mb-6">
                Kreiraj račun na TK Student Hub
            </p>

            <div
                v-if="error"
                class="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg mb-4 text-sm"
            >
                {{ error }}
            </div>

            <div class="flex flex-col gap-4">

                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                        Ime i prezime
                    </label>
                    <input
                        v-model="fullName"
                        type="text"
                        placeholder="Ime Prezime"
                        class="w-full border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:border-primary dark:focus:border-orange-500"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                        Email
                    </label>
                    <input
                        v-model="email"
                        type="email"
                        placeholder="tvoj@email.com"
                        class="w-full border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:border-primary dark:focus:border-orange-500"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">
                        Lozinka
                    </label>
                    <input
                        v-model="password"
                        type="password"
                        placeholder="••••••••"
                        class="w-full border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:border-primary dark:focus:border-orange-500"
                    />
                </div>

                <button
                    @click="handleRegister"
                    :disabled="loading"
                    class="bg-primary dark:bg-orange-500 text-white py-2 rounded-lg hover:bg-primary/90 dark:hover:bg-orange-600 transition font-medium disabled:opacity-50"
                >
                    {{ loading ? 'Registracija...' : 'Registruj se' }}
                </button>

            </div>

            <p class="text-center text-sm text-gray-500 dark:text-slate-400 mt-6">
                Već imaš račun?
                <router-link
                    to="/login"
                    class="text-primary dark:text-orange-500 font-medium hover:underline"
                >
                    Prijavi se
                </router-link>
            </p>

        </div>
    </div>
</template>

<script>
import { registerUser, getMe } from '../services/api'

export default {
    name: 'RegisterView',
    data() {
        return {
            fullName: '',
            email: '',
            password: '',
            loading: false,
            error: null
        }
    },
    methods: {
        async handleRegister() {
            this.loading = true
            this.error = null

            const response = await registerUser(this.email, this.fullName, this.password)

            if (response.access_token) {
                localStorage.setItem('token', response.access_token)
                const user = await getMe(response.access_token)
                localStorage.setItem('username', user.full_name)
                localStorage.setItem('role', user.role)
                window.location.href = '/'
            } else {
                this.error = response.detail || 'Greška pri registraciji.'
            }

            this.loading = false
        }
    }
}
</script>