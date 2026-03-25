<template>
  <div>
    <Table
      :columns="columns"
      :items="usuarios"
      :loading="loading"
      loading-text="Carregando usuários..."
      empty-text="Nenhum usuário encontrado"
      empty-icon="people-outline"
    >
      <template #cell-tipo="{ item }">
        <span :class="[
          'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
          item.tipo === 'admin' ? 'bg-purple-100 text-purple-800' :
          item.tipo === 'bibliotecario' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        ]">
          {{ item.tipo === 'admin' ? 'Admin' : item.tipo === 'bibliotecario' ? 'Bibliotecário' : 'Usuário' }}
        </span>
      </template>

      <template #cell-biblioteca="{ item }">
        <span v-if="item.tipo === 'bibliotecario' && item.biblioteca" class="inline-flex items-center text-sm text-blue-600 font-medium">
          <ion-icon name="library-outline" class="mr-1"></ion-icon>
          {{ item.biblioteca.nome }} - {{ item.biblioteca.campus }}
        </span>
        <span v-else class="text-sm text-gray-400">-</span>
      </template>

      <template #cell-acoes="{ item }">
        <select
          :value="item.tipo"
          @change="alterarTipoUsuario(item.id, $event.target.value)"
          class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent hover:border-purple-400 transition-colors"
        >
          <option value="usuario">Usuário</option>
          <option value="bibliotecario">Bibliotecário</option>
          <option value="admin">Admin</option>
        </select>
      </template>
    </Table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Table from '../components/UI/Table.vue'
import api from '../services/api'

const usuarios = ref([])
const loading = ref(false)

const columns = [
  { key: 'nome_completo', label: 'Nome' },
  { key: 'matricula', label: 'Matrícula' },
  { key: 'cpf', label: 'CPF' },
  { key: 'tipo', label: 'Tipo' },
  { key: 'biblioteca', label: 'Biblioteca' },
  { key: 'acoes', label: 'Ações' }
]

const carregarUsuarios = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/admin/usuarios')
    usuarios.value = response.data
  } catch (error) {
  } finally {
    loading.value = false
  }
}

const alterarTipoUsuario = async (usuarioId, novoTipo) => {
  try {
    await api.patch(`/api/admin/usuarios/${usuarioId}/tipo`, {
      tipo: novoTipo
    })
    await carregarUsuarios()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao alterar tipo de usuário. Tente novamente.'
    alert(errorMsg)
    await carregarUsuarios()
  }
}

onMounted(() => {
  carregarUsuarios()
})
</script>


