import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

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
    path: '/prakse-i-edukacije',
    name: 'prakse',
    component: () => import('../views/prakse/PrakseView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/materials',
    name: 'materials',
    component: () => import('../views/materials/MaterialsView.vue'),
    meta: { requiresAuth: true }
  },
  

  {
    path: '/forum',
    name: 'forum',
    component: () => import('../views/forum/ForumView.vue'),
  },
  {
    path: '/forum/nova-tema',
    name: 'create-topic',
    component: () => import('../views/forum/CreateTopicView.vue'),
  },
  {
    path: '/forum/tema/:id', // :id omogućava dinamičko prosljeđivanje ID-ja teme
    name: 'topic-detail',
    component: () => import('../views/forum/TopicDetailView.vue'),
    props: true // Dozvoljava da ID rute uđe direktno kao prop u komponentu
  },
  // =========================================================

  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
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