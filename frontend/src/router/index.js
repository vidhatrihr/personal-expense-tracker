import { createRouter, createWebHistory } from 'vue-router'
import { useWhoAmI } from '@/composables/useWhoAmI.js'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView, meta: { guestOnly: true } },
    { path: '/register', component: RegisterView, meta: { guestOnly: true } },
    { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to, from) => {
  const { whoAmI, clearUser } = useWhoAmI()

  if (from.meta.guestOnly && to.meta.requiresAuth) {
    clearUser()
  }

  const me = await whoAmI()

  if (to.meta.requiresAuth && !me) {
    return '/'
  }
  if (to.meta.guestOnly && me) {
    return '/dashboard'
  }
})

export default router
