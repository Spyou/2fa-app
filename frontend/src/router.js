import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Setup2FA from './views/Setup2FA.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login, meta: { requiresGuest: true } },
    { path: '/register', component: Register, meta: { requiresGuest: true } },
    { path: '/setup-2fa', component: Setup2FA },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }
  ]
})

// Route guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else if (to.meta.requiresGuest && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
