import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { setUnauthorizedHandler } from './api/sessions'
import { setUser } from './auth'
import router from './router'

// 401 dari API mana pun -> sesi habis -> kembali ke login
setUnauthorizedHandler(() => {
  setUser(null)
  router.push('/login')
})

createApp(App).use(router).mount('#app')
