import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

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
    path: "/prakse-i-edukacije",
    name: "prakse",
    component: () => import("../views/prakse/PrakseView.vue"),
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
    meta: { requiresAuth: true },
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
  // =========================================================

  {
    path: '/profiles',
    name: 'profiles',
    component: () => import('../views/profiles/ProfilesView.vue'),
    meta: { requiresAuth: true }
  },

  // =========================================================

  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('../views/forum/admin/AdminDashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
    
  {
    path: "/profiles",
    name: "profiles",
    component: () => import("../views/profiles/ProfilesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/materials/:id",
    name: "material-details",
    component: () => import("../views/materials/MaterialDetailView.vue"),
    meta: { requiresAuth: false },
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('token')
  const userRole = localStorage.getItem('role')

  if (to.meta.requiresAuth && !isLoggedIn) {
    next("/login");
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    next('/') // Ako nije admin, baci ga na pocetnu
  } else {
    next();
  }
});

export default router;
