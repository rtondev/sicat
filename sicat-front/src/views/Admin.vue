<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-6">
      <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
        <ion-icon name="settings-outline" class="text-purple-600"></ion-icon>
        Administração
      </h1>
      <p class="text-gray-600">Painel de administração do sistema</p>
    </div>

    <div class="border-b border-gray-200 mb-6">
      <nav class="flex space-x-8">
        <button
          @click="handleTabChange('usuarios')"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center',
            activeTab === 'usuarios'
              ? 'border-purple-600 text-purple-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          <ion-icon name="people-outline" class="text-base mr-2"></ion-icon>
          Usuários
        </button>
        <button
          @click="handleTabChange('fichas')"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center',
            activeTab === 'fichas'
              ? 'border-purple-600 text-purple-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          <ion-icon name="document-text-outline" class="text-base mr-2"></ion-icon>
          Fichas
        </button>
        <button
          @click="handleTabChange('bibliotecas')"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center',
            activeTab === 'bibliotecas'
              ? 'border-purple-600 text-purple-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          <ion-icon name="library-outline" class="text-base mr-2"></ion-icon>
          Bibliotecas
        </button>
      </nav>
    </div>

    <AdminUsuarios v-if="activeTab === 'usuarios'" />

    <AdminFichas v-else-if="activeTab === 'fichas'" />

    <AdminBibliotecas v-else-if="activeTab === 'bibliotecas'" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminUsuarios from './AdminUsuarios.vue'
import AdminFichas from './AdminFichas.vue'
import AdminBibliotecas from './AdminBibliotecas.vue'

const router = useRouter()
const activeTab = ref('usuarios')

const handleTabChange = (tab) => {
  activeTab.value = tab
}
</script>
