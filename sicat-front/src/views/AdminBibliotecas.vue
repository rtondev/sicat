<template>
  <div>
    <div class="mb-4 flex justify-end">
      <Button @click="showNovaBiblioteca = true">
        <ion-icon name="add-outline"></ion-icon>
        Nova Biblioteca
      </Button>
    </div>

    <Table
      :columns="columns"
      :items="bibliotecas"
      :loading="loading"
      loading-text="Carregando bibliotecas..."
      empty-text="Nenhuma biblioteca cadastrada"
      empty-icon="library-outline"
    >
      <template #empty-action>
        <Button @click="showNovaBiblioteca = true">
          <ion-icon name="add-outline"></ion-icon>
          Criar Primeira Biblioteca
        </Button>
      </template>

      <template #cell-data_criacao="{ value }">
        {{ new Date(value).toLocaleDateString('pt-BR') }}
      </template>

      <template #cell-acoes="{ item }">
        <div class="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            @click="verDetalhes(item)"
            title="Ver detalhes"
          >
            <ion-icon name="eye-outline"></ion-icon>
          </Button>
          <Button
            size="sm"
            variant="outline"
            @click="editarBiblioteca(item)"
            title="Editar biblioteca"
          >
            <ion-icon name="create-outline"></ion-icon>
          </Button>
          <Button
            size="sm"
            variant="outline"
            @click="verBibliotecarios(item)"
            title="Ver bibliotecários"
          >
            <ion-icon name="people-outline"></ion-icon>
          </Button>
          <Button
            size="sm"
            variant="outline"
            @click="confirmarDeletar(item)"
            title="Remover biblioteca"
            class="text-red-600 hover:text-red-700 hover:border-red-400"
          >
            <ion-icon name="trash-outline"></ion-icon>
          </Button>
        </div>
      </template>
    </Table>

    <Modal :show="showNovaBiblioteca" title="Nova Biblioteca" @close="showNovaBiblioteca = false">
      <form @submit.prevent="criarBiblioteca" class="space-y-4">
        <Input
          label="Nome"
          v-model="novaBiblioteca.nome"
          placeholder="Nome da biblioteca"
          required
        />
        <Input
          label="Campus"
          v-model="novaBiblioteca.campus"
          placeholder="Nome do campus"
          required
        />
        <div class="flex gap-2 justify-end">
          <Button type="button" variant="outline" @click="showNovaBiblioteca = false">
            Cancelar
          </Button>
          <Button type="submit" :loading="criandoBiblioteca">
            Criar
          </Button>
        </div>
      </form>
    </Modal>

    <Modal :show="showAdicionarBibliotecario" @close="showAdicionarBibliotecario = false">
      <template #header>
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Adicionar Bibliotecário</h2>
          <p class="text-sm text-gray-600 mt-1">{{ bibliotecaSelecionada?.nome }}</p>
        </div>
      </template>
      
      <div v-if="loadingUsuariosParaAdicionar" class="text-center py-8">
        <ion-icon name="hourglass-outline" class="text-3xl text-purple-600 animate-spin"></ion-icon>
        <p class="text-gray-600 mt-2 text-sm">Carregando usuários...</p>
      </div>
      <div v-else-if="usuariosDisponiveis.length === 0" class="text-center py-8">
        <p class="text-gray-600">Nenhum usuário disponível</p>
      </div>
      <div v-else class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Selecione o usuário</label>
          <select
            v-model="usuarioSelecionado"
            class="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
          >
            <option value="">Selecione um usuário</option>
            <option
              v-for="usuario in usuariosDisponiveis"
              :key="usuario.id"
              :value="usuario.id"
            >
              {{ usuario.nome_completo }} ({{ usuario.matricula }}) - {{ usuario.tipo === 'admin' ? 'Admin' : usuario.tipo === 'bibliotecario' ? 'Bibliotecário' : 'Usuário' }}
            </option>
          </select>
        </div>
        <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
          <p class="text-xs text-purple-800 flex items-start gap-2">
            <ion-icon name="information-circle-outline" class="text-base flex-shrink-0 mt-0.5"></ion-icon>
            <span>O usuário selecionado terá seu tipo alterado para "Bibliotecário" automaticamente.</span>
          </p>
        </div>
        <div class="flex gap-2 justify-end">
          <Button type="button" variant="outline" @click="showAdicionarBibliotecario = false">
            Cancelar
          </Button>
          <Button
            @click="adicionarBibliotecario"
            :loading="adicionandoBibliotecario"
            :disabled="!usuarioSelecionado"
          >
            Adicionar
          </Button>
        </div>
      </div>
    </Modal>

    <Modal :show="showDetalhes" title="Detalhes da Biblioteca" @close="showDetalhes = false">
      <div v-if="bibliotecaParaDetalhes" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nome</label>
          <p class="text-gray-900 font-medium">{{ bibliotecaParaDetalhes.nome }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Campus</label>
          <p class="text-gray-900">{{ bibliotecaParaDetalhes.campus }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data de Criação</label>
          <p class="text-gray-900">{{ new Date(bibliotecaParaDetalhes.data_criacao).toLocaleDateString('pt-BR') }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Última Edição</label>
          <p class="text-gray-900">{{ new Date(bibliotecaParaDetalhes.data_edicao).toLocaleDateString('pt-BR') }}</p>
        </div>
      </div>
    </Modal>

    <Modal :show="showEditar" title="Editar Biblioteca" @close="showEditar = false">
      <form v-if="bibliotecaParaEditar" @submit.prevent="salvarEdicao" class="space-y-4">
        <Input
          label="Nome"
          v-model="bibliotecaParaEditar.nome"
          placeholder="Nome da biblioteca"
          required
        />
        <Input
          label="Campus"
          v-model="bibliotecaParaEditar.campus"
          placeholder="Nome do campus"
          required
        />
        <div class="flex gap-2 justify-end">
          <Button type="button" variant="outline" @click="showEditar = false">
            Cancelar
          </Button>
          <Button type="submit" :loading="editandoBiblioteca">
            Salvar
          </Button>
        </div>
      </form>
    </Modal>

    <Modal :show="showBibliotecarios" @close="showBibliotecarios = false">
      <template #header>
        <div class="flex items-center justify-between w-full">
          <div>
            <h2 class="text-xl font-semibold text-gray-900">Bibliotecários</h2>
            <p class="text-sm text-gray-600 mt-1">{{ bibliotecaParaBibliotecarios?.nome }}</p>
          </div>
          <Button
            size="sm"
            @click="abrirModalAdicionarBibliotecario(bibliotecaParaBibliotecarios)"
          >
            <ion-icon name="add-outline"></ion-icon>
            Adicionar
          </Button>
        </div>
      </template>
      
      <div v-if="loadingBibliotecarios" class="text-center py-8">
        <ion-icon name="hourglass-outline" class="text-3xl text-purple-600 animate-spin"></ion-icon>
        <p class="text-gray-600 mt-2 text-sm">Carregando bibliotecários...</p>
      </div>
      <div v-else-if="bibliotecariosDaBiblioteca.length === 0" class="text-center py-8">
        <ion-icon name="people-outline" class="text-4xl text-gray-400 mb-4"></ion-icon>
        <p class="text-gray-600 mb-4">Nenhum bibliotecário vinculado a esta biblioteca</p>
        <Button
          @click="abrirModalAdicionarBibliotecario(bibliotecaParaBibliotecarios)"
        >
          <ion-icon name="add-outline"></ion-icon>
          Adicionar Bibliotecário
        </Button>
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="bibliotecario in bibliotecariosDaBiblioteca"
          :key="bibliotecario.id"
          class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <div>
            <p class="font-medium text-gray-900">{{ bibliotecario.nome_completo }}</p>
            <p class="text-sm text-gray-600">{{ bibliotecario.matricula }}</p>
          </div>
          <Button
            size="sm"
            variant="outline"
            @click="removerBibliotecario(bibliotecario.id)"
            class="text-red-600 hover:text-red-700 hover:border-red-400"
          >
            <ion-icon name="trash-outline"></ion-icon>
            Remover
          </Button>
        </div>
      </div>
    </Modal>

    <Modal :show="showConfirmarDeletar" title="Confirmar Exclusão" @close="showConfirmarDeletar = false">
      <div v-if="bibliotecaParaDeletar" class="space-y-4">
        <div class="bg-red-50 border border-red-200 rounded-lg p-3">
          <p class="text-sm text-red-800">
            <ion-icon name="warning-outline" class="inline mr-1"></ion-icon>
            Tem certeza que deseja deletar a biblioteca <strong>{{ bibliotecaParaDeletar.nome }}</strong>?
          </p>
        </div>
        <p class="text-sm text-gray-600">
          Esta ação não pode ser desfeita. A biblioteca só pode ser deletada se não houver fichas associadas a ela.
        </p>
        <div class="flex gap-2 justify-end">
          <Button type="button" variant="outline" @click="showConfirmarDeletar = false">
            Cancelar
          </Button>
          <Button
            @click="deletarBiblioteca"
            :loading="deletandoBiblioteca"
            class="bg-red-600 hover:bg-red-700 text-white"
          >
            <ion-icon name="trash-outline"></ion-icon>
            Deletar
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Table from '../components/UI/Table.vue'
import Button from '../components/UI/Button.vue'
import Input from '../components/UI/Input.vue'
import Modal from '../components/UI/Modal.vue'
import api from '../services/api'

const bibliotecas = ref([])
const loading = ref(false)
const showNovaBiblioteca = ref(false)
const criandoBiblioteca = ref(false)
const novaBiblioteca = ref({
  nome: '',
  campus: ''
})
const showAdicionarBibliotecario = ref(false)
const bibliotecaSelecionada = ref(null)
const usuarioSelecionado = ref('')
const usuariosDisponiveis = ref([])
const loadingUsuariosParaAdicionar = ref(false)
const adicionandoBibliotecario = ref(false)
const showDetalhes = ref(false)
const showEditar = ref(false)
const showBibliotecarios = ref(false)
const bibliotecaParaEditar = ref(null)
const bibliotecaParaDetalhes = ref(null)
const bibliotecaParaBibliotecarios = ref(null)
const bibliotecariosDaBiblioteca = ref([])
const loadingBibliotecarios = ref(false)
const editandoBiblioteca = ref(false)
const deletandoBiblioteca = ref(false)
const bibliotecaParaDeletar = ref(null)
const showConfirmarDeletar = ref(false)

const columns = [
  { key: 'nome', label: 'Nome' },
  { key: 'campus', label: 'Campus' },
  { key: 'data_criacao', label: 'Data de Criação' },
  { key: 'acoes', label: 'Ações' }
]

const carregarBibliotecas = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/admin/bibliotecas')
    bibliotecas.value = response.data
  } catch (error) {
  } finally {
    loading.value = false
  }
}

const criarBiblioteca = async () => {
  criandoBiblioteca.value = true
  try {
    await api.post('/api/admin/bibliotecas', novaBiblioteca.value)
    showNovaBiblioteca.value = false
    novaBiblioteca.value = { nome: '', campus: '' }
    await carregarBibliotecas()
  } catch (error) {
    alert('Erro ao criar biblioteca. Tente novamente.')
  } finally {
    criandoBiblioteca.value = false
  }
}

const abrirModalAdicionarBibliotecario = async (biblioteca) => {
  bibliotecaSelecionada.value = biblioteca
  usuarioSelecionado.value = ''
  showBibliotecarios.value = false
  showAdicionarBibliotecario.value = true
  loadingUsuariosParaAdicionar.value = true
  
  try {
    const response = await api.get('/api/admin/usuarios')
    usuariosDisponiveis.value = response.data
  } catch (error) {
    alert('Erro ao carregar usuários. Tente novamente.')
  } finally {
    loadingUsuariosParaAdicionar.value = false
  }
}

const adicionarBibliotecario = async () => {
  if (!usuarioSelecionado.value || !bibliotecaSelecionada.value) {
    return
  }
  
  adicionandoBibliotecario.value = true
  try {
    await api.post('/api/admin/bibliotecas/adicionar-bibliotecario', {
      usuario_id: usuarioSelecionado.value,
      biblioteca_id: bibliotecaSelecionada.value.id
    })
    
    showAdicionarBibliotecario.value = false
    const bibliotecaId = bibliotecaSelecionada.value.id
    bibliotecaSelecionada.value = null
    usuarioSelecionado.value = ''
    
    alert('Bibliotecário adicionado com sucesso! O tipo do usuário foi alterado para "Bibliotecário".')
    
    if (bibliotecaParaBibliotecarios.value && bibliotecaParaBibliotecarios.value.id === bibliotecaId) {
      await verBibliotecarios(bibliotecaParaBibliotecarios.value)
    }
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao adicionar bibliotecário. Tente novamente.'
    alert(errorMsg)
  } finally {
    adicionandoBibliotecario.value = false
  }
}

const verDetalhes = (biblioteca) => {
  bibliotecaParaDetalhes.value = biblioteca
  showDetalhes.value = true
}

const editarBiblioteca = (biblioteca) => {
  bibliotecaParaEditar.value = { ...biblioteca }
  showEditar.value = true
}

const salvarEdicao = async () => {
  if (!bibliotecaParaEditar.value) return
  
  editandoBiblioteca.value = true
  try {
    await api.patch(`/api/admin/bibliotecas/${bibliotecaParaEditar.value.id}`, {
      nome: bibliotecaParaEditar.value.nome,
      campus: bibliotecaParaEditar.value.campus
    })
    
    showEditar.value = false
    bibliotecaParaEditar.value = null
    await carregarBibliotecas()
    alert('Biblioteca atualizada com sucesso!')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao editar biblioteca. Tente novamente.'
    alert(errorMsg)
  } finally {
    editandoBiblioteca.value = false
  }
}

const verBibliotecarios = async (biblioteca) => {
  bibliotecaParaBibliotecarios.value = biblioteca
  showBibliotecarios.value = true
  loadingBibliotecarios.value = true
  
  try {
    const response = await api.get(`/api/admin/bibliotecas/${biblioteca.id}/bibliotecarios`)
    bibliotecariosDaBiblioteca.value = response.data
  } catch (error) {
    alert('Erro ao carregar bibliotecários. Tente novamente.')
  } finally {
    loadingBibliotecarios.value = false
  }
}

const removerBibliotecario = async (usuarioId) => {
  if (!confirm('Tem certeza que deseja remover este bibliotecário da biblioteca?')) {
    return
  }
  
  try {
    await api.delete(`/api/admin/bibliotecas/${bibliotecaParaBibliotecarios.value.id}/bibliotecarios/${usuarioId}`)
    await verBibliotecarios(bibliotecaParaBibliotecarios.value)
    alert('Bibliotecário removido com sucesso!')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao remover bibliotecário. Tente novamente.'
    alert(errorMsg)
  }
}

const confirmarDeletar = (biblioteca) => {
  bibliotecaParaDeletar.value = biblioteca
  showConfirmarDeletar.value = true
}

const deletarBiblioteca = async () => {
  if (!bibliotecaParaDeletar.value) return
  
  deletandoBiblioteca.value = true
  try {
    await api.delete(`/api/admin/bibliotecas/${bibliotecaParaDeletar.value.id}`)
    showConfirmarDeletar.value = false
    bibliotecaParaDeletar.value = null
    await carregarBibliotecas()
    alert('Biblioteca deletada com sucesso!')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao deletar biblioteca. Tente novamente.'
    alert(errorMsg)
  } finally {
    deletandoBiblioteca.value = false
  }
}

onMounted(() => {
  carregarBibliotecas()
})
</script>

