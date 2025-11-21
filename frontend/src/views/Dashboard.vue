<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
        <ion-icon name="grid-outline" class="text-purple-600"></ion-icon>
        Dashboard
      </h1>
      <p class="text-gray-600">
        <span v-if="user">Bem-vindo, {{ user.nome_completo?.split(' ')[0] || 'Usuário' }}!</span>
        <span v-else>Bem-vindo ao SICAT</span>
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm mb-1">Total de Fichas</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalFichas }}</p>
          </div>
          <ion-icon name="document-text-outline" class="text-4xl text-purple-600"></ion-icon>
        </div>
      </Card>
      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm mb-1">Pendentes</p>
            <p class="text-3xl font-bold text-yellow-600">{{ stats.pendentes }}</p>
          </div>
          <ion-icon name="time-outline" class="text-4xl text-yellow-600"></ion-icon>
        </div>
      </Card>
      <Card>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm mb-1">Aprovadas</p>
            <p class="text-3xl font-bold text-green-600">{{ stats.aprovadas }}</p>
          </div>
          <ion-icon name="checkmark-circle-outline" class="text-4xl text-green-600"></ion-icon>
        </div>
      </Card>
    </div>

    <div class="flex gap-4">
      <router-link to="/fichas/nova">
        <Button>
          <ion-icon name="add-outline"></ion-icon>
          Nova Ficha
        </Button>
      </router-link>
      <router-link to="/fichas">
        <Button variant="outline">
          <ion-icon name="list-outline"></ion-icon>
          Ver Todas
        </Button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Card from '../components/UI/Card.vue'
import Button from '../components/UI/Button.vue'
import { authAPI } from '../services/api'
import api from '../services/api'

const user = ref(null)
const stats = ref({
  totalFichas: 0,
  pendentes: 0,
  aprovadas: 0
})
const loading = ref(true)

const carregarDados = async () => {
  loading.value = true
  try {
    try {
      const userData = await authAPI.getMe()
      user.value = userData
    } catch (error) {
    }

    try {
      const response = await api.get('/api/fichas/minhas')
      const fichas = response.data
      
      stats.value = {
        totalFichas: fichas.length,
        pendentes: fichas.filter(f => f.status === 'aguardando_autorizacao').length,
        aprovadas: fichas.filter(f => f.status === 'aprovado').length
      }
    } catch (error) {
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  carregarDados()
})
</script>

