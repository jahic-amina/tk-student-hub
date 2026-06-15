import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdsView from '../views/ads/AdsView.vue'
import AdView from '../views/ads/AdView.vue'
import ApplicationView from '../views/application/ApplicationView.vue'
import CompanyRegisterView from '../views/company/CompanyRegisterView.vue'
import CompanyLoginView from '../views/company/CompanyLoginView.vue'
import AdminCompanyApprovalView from '../views/company/AdminCompanyApprovalView.vue'
import CompanyView from '../views/company/CompanyView.vue'
import AdminAdsView from '../views/ads/AdminAdsApprovalView.vue'

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: { guestOnly: true },
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
    path: '/ads/:id/apply',
    name: 'application',
    component: ApplicationView,
    meta: { requiresAuth: true }
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
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/ads',
    name: 'admin-ads',
    component: AdminAdsView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: "/prakse-i-edukacije",
    name: "prakse",
    component: AdsView, // POPRAVLJENO: Koristi AdsView umjesto ApplicationView
    meta: { requiresAuth: true },
  },
  {
    path: "/materials",
    name: "materials",
    component: () => import("../views/materials/MaterialsView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/materials/upload",   
    name: "material-upload",
    component: () => import("../views/materials/MaterialUploadView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/materials/pending", 
    name: "pending-materials",
    component: () => import("../views/materials/MaterialsView.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/materials/:id",
    name: "material-details",
    component: () => import("../views/materials/MaterialDetailView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: '/forum',
    name: 'forum',
    component: () => import('../views/forum/ForumView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/forum/nova-tema',
    name: 'create-topic',
    component: () => import('../views/forum/CreateTopicView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/forum/tema/:id', 
    name: 'topic-detail',
    component: () => import('../views/forum/TopicDetailView.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/profiles/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/admin/AdminKorisniciView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/forum',
    name: 'admin-forum-dashboard',
    component: () => import('../views/forum/admin/AdminDashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/prakse',
    name: 'prakse',
    component: () => import('../views/prakse/PrakseView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/workshops',
    name: 'workshops',
    component: () => import('../views/workshops/WorkshopsView.vue'),
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// POPRAVLJENO: Očišćena i ispravljena navigacijska zaštita (Guards)
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')
  const role = localStorage.getItem('role')
  const isAdmin = role === 'admin'

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router;