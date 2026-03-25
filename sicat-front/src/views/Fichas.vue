<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
          <ion-icon name="document-text-outline" class="text-purple-600"></ion-icon>
          Minhas Fichas
        </h1>
        <p class="text-gray-600">Gerencie suas fichas catalográficas</p>
      </div>
      <router-link to="/fichas/nova">
        <Button>
          <ion-icon name="add-outline"></ion-icon>
          Nova Ficha
        </Button>
      </router-link>
    </div>

    <div v-if="loading" class="text-center py-12">
      <ion-icon name="hourglass-outline" class="text-4xl text-purple-600 animate-spin"></ion-icon>
      <p class="text-gray-600 mt-4">Carregando...</p>
    </div>

    <div v-else-if="fichas.length === 0" class="text-center py-12">
      <ion-icon name="document-outline" class="text-6xl text-gray-700 mb-4"></ion-icon>
      <p class="text-gray-600 mb-4">Nenhuma ficha encontrada</p>
      <router-link to="/fichas/nova">
        <Button>
          <ion-icon name="add-outline"></ion-icon>
          Criar Primeira Ficha
        </Button>
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card v-for="ficha in fichas" :key="ficha.id" class="hover:border-purple-600 hover:shadow-md transition-all">
        <div class="space-y-4">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">{{ ficha.titulo }}</h3>
              <p class="text-xs text-gray-500 mb-2">ID: {{ ficha.id_curto }}</p>
            </div>
            <span :class="[
              'inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full flex-shrink-0',
              ficha.status === 'aprovado' ? 'bg-green-100 text-green-800' :
              ficha.status === 'negado' ? 'bg-red-100 text-red-800' :
              'bg-yellow-100 text-yellow-800'
            ]">
              <ion-icon :name="getStatusIcon(ficha.status)" class="text-sm"></ion-icon>
              {{ getStatusLabel(ficha.status) }}
            </span>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex items-center gap-2 text-gray-600">
              <ion-icon name="person-outline" class="text-gray-400"></ion-icon>
              <span class="truncate">{{ ficha.autor_nome_completo }}</span>
            </div>
            <div class="flex items-center gap-2 text-gray-600">
              <ion-icon name="calendar-outline" class="text-gray-400"></ion-icon>
              <span>{{ new Date(ficha.data_criacao).toLocaleDateString('pt-BR') }}</span>
            </div>
          </div>
          
          <div class="pt-3 border-t border-gray-200 flex items-center justify-between">
            <Button
              v-if="ficha.status === 'aprovado'"
              variant="outline"
              size="sm"
              @click="downloadFicha(ficha.id)"
            >
              <ion-icon name="download-outline"></ion-icon>
              Baixar
            </Button>
            <span v-else class="text-xs text-gray-500">
              {{ ficha.status === 'aguardando_autorizacao' ? 'Aguardando aprovação' : 'Ficha negada' }}
            </span>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Card from '../components/UI/Card.vue'
import Button from '../components/UI/Button.vue'
import api from '../services/api'

const router = useRouter()
const fichas = ref([])
const loading = ref(true)

const getStatusLabel = (status) => {
  const labels = {
    aguardando_autorizacao: 'Aguardando',
    aprovado: 'Aprovado',
    negado: 'Negado'
  }
  return labels[status] || status
}

const getStatusIcon = (status) => {
  const icons = {
    aguardando_autorizacao: 'time-outline',
    aprovado: 'checkmark-circle-outline',
    negado: 'close-circle-outline'
  }
  return icons[status] || 'help-outline'
}

const getStatusClass = (status) => {
  const classes = {
    aguardando_autorizacao: 'text-yellow-600 flex items-center gap-1',
    aprovado: 'text-green-600 flex items-center gap-1',
    negado: 'text-red-600 flex items-center gap-1'
  }
  return classes[status] || 'text-gray-600 flex items-center gap-1'
}

const carregarFichas = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/fichas/minhas')
    fichas.value = response.data
  } catch (error) {
    if (error.response?.status === 401) {
      router.push('/login')
    } else {
      alert('Erro ao carregar fichas. Tente novamente.')
    }
  } finally {
    loading.value = false
  }
}

const downloadFicha = async (id) => {
  try {
    const response = await api.get(`/api/fichas/${id}/download`, {
      responseType: 'blob'
    })
    const blob = new Blob([response.data], { type: 'image/png' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `ficha_${id}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    alert('Erro ao baixar ficha. Tente novamente.')
  }
}

onMounted(() => {
  carregarFichas()
})
</script>

