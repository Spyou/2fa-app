import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Setup2FA from './views/Setup2FA.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    { path: '/setup-2fa', component: Setup2FA }
  ]
})
