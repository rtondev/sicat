import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import { routes } from './router'
import { routerGuard } from './router/guards'

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(routerGuard)

const app = createApp(App)
app.use(router)
app.mount('#app')
