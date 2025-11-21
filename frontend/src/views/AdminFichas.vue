<template>
  <div>
    <Table
      :columns="columns"
      :items="fichas"
      :loading="loading"
      loading-text="Carregando fichas..."
      empty-text="Nenhuma ficha encontrada"
      empty-icon="document-text-outline"
    >
      <template #cell-status="{ item }">
        <span :class="[
          'inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full',
          item.status === 'aprovado' ? 'bg-green-100 text-green-800' :
          item.status === 'negado' ? 'bg-red-100 text-red-800' :
          'bg-yellow-100 text-yellow-800'
        ]">
          <ion-icon :name="item.status === 'aprovado' ? 'checkmark-circle' : item.status === 'negado' ? 'close-circle' : 'time'" class="text-sm"></ion-icon>
          {{ item.status === 'aprovado' ? 'Aprovado' : item.status === 'negado' ? 'Negado' : 'Aguardando' }}
        </span>
      </template>
    </Table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Table from '../components/UI/Table.vue'
import api from '../services/api'

const fichas = ref([])
const loading = ref(false)

const columns = [
  { key: 'titulo', label: 'Título' },
  { key: 'id_curto', label: 'ID' },
  { key: 'autor_nome_completo', label: 'Autor' },
  { key: 'status', label: 'Status' }
]

const carregarFichas = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/admin/fichas')
    fichas.value = response.data
  } catch (error) {
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  carregarFichas()
})
</script>


