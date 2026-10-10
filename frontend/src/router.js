import { createRouter, createWebHistory } from 'vue-router'
import { loadUser } from './auth'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView, meta: { requiresAuth: true } },
    { path: '/login', component: LoginView },
  ],
})

// Guard hanya kenyamanan UI — penjaga sebenarnya tetap di backend.
router.beforeEach(async (to) => {
  const user = await loadUser()
  if (to.meta.requiresAuth && !user) return '/login'
  if (to.path === '/login' && user) return '/'
})

export default router
