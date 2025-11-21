<template>
  <header class="border-b border-gray-200 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 gap-4 overflow-x-auto">
        <div class="flex items-center gap-3 flex-shrink-0">
          <router-link to="/" class="flex items-center gap-2 flex-shrink-0">
            <ion-icon name="library-outline" class="text-lg text-purple-600"></ion-icon>
            <span class="text-base font-bold text-gray-900">SICAT</span>
          </router-link>
          <nav v-if="isAuthenticated" class="flex items-center gap-2">
            <router-link
              to="/dashboard"
              :class="[
                'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
                $route.path.startsWith('/dashboard') 
                  ? 'bg-pink-100 text-pink-700' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              Dashboard
            </router-link>
            <router-link
              to="/fichas"
              :class="[
                'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
                $route.path.startsWith('/fichas') 
                  ? 'bg-pink-100 text-pink-700' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              Fichas
            </router-link>
            <router-link
              v-if="userRole === 'admin'"
              to="/admin"
              :class="[
                'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
                $route.path.startsWith('/admin') 
                  ? 'bg-pink-100 text-pink-700' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              Admin
            </router-link>
            <router-link
              v-if="userRole === 'bibliotecario'"
              to="/bibliotecario"
              :class="[
                'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
                $route.path.startsWith('/bibliotecario') 
                  ? 'bg-pink-100 text-pink-700' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              ]"
            >
              Solicitações
            </router-link>
          </nav>
        </div>
        <div v-if="isAuthenticated" class="flex items-center gap-2 flex-shrink-0">
          <router-link
            to="/perfil"
            :class="[
              'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium',
              $route.path === '/perfil' 
                ? 'bg-pink-100 text-pink-700' 
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            ]"
          >
            <span class="hidden sm:inline">{{ userNome || 'Perfil' }}</span>
          </router-link>
        </div>
        <div v-else class="flex items-center gap-2 flex-shrink-0">
          <router-link
            to="/register"
            :class="[
              'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
              $route.path === '/register' 
                ? 'bg-pink-100 text-pink-700' 
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            ]"
          >
            Criar conta
          </router-link>
          <router-link
            to="/login"
            :class="[
              'px-3 py-1.5 rounded-lg transition-colors flex items-center text-sm font-medium flex-shrink-0',
              $route.path === '/login' 
                ? 'bg-pink-100 text-pink-700' 
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
            ]"
          >
            Entrar
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isAuthenticated = ref(!!localStorage.getItem('access_token'))
const userRole = ref(localStorage.getItem('user_role') || '')
const userNome = ref('')

const atualizarEstado = () => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
  userRole.value = localStorage.getItem('user_role') || ''
  const nome = localStorage.getItem('user_nome') || ''
  userNome.value = nome.split(' ')[0] || nome
}

const handleStorageChange = (e) => {
  if (e.key === 'access_token' || e.key === 'user_role' || e.key === 'user_nome') {
    atualizarEstado()
  }
}

const handleAuthChange = () => {
  atualizarEstado()
}

watch(() => route.path, () => {
  atualizarEstado()
}, { immediate: true })

onMounted(() => {
  atualizarEstado()
  window.addEventListener('storage', handleStorageChange)
  window.addEventListener('auth-changed', handleAuthChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange)
  window.removeEventListener('auth-changed', handleAuthChange)
})
</script>

