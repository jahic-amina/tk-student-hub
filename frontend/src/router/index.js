import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdsView from '../views/ads/AdsView.vue'
import AdView from '../views/ads/AdView.vue'
import CompanyRegisterView from '../views/company/CompanyRegisterView.vue'
import CompanyLoginView from '../views/company/CompanyLoginView.vue'
import AdminCompanyApprovalView from '../views/company/AdminCompanyApprovalView.vue'
import CompanyView from '../views/company/CompanyView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  {
    path: '/ads',
    name: 'ads',
    component: AdsView
  },
  {
    path: '/ads/:id',
    name: 'ad-detail',
    component: AdView
  },
  {
    path: '/companies/:id',
    name: 'company',
    component: CompanyView
  },
  {
    path: '/company/register',
    name: 'company-register',
    component: CompanyRegisterView
  },
  {
    path: '/company/login',
    name: 'company-login',
    component: CompanyLoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/admin/companies',
    name: 'admin-companies',
    component: AdminCompanyApprovalView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router