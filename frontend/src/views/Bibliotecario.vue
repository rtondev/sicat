<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-6">
      <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
        <ion-icon name="book-outline" class="text-purple-600"></ion-icon>
        Fichas da Biblioteca
      </h1>
      <p class="text-gray-600">Visualize e gerencie todas as fichas da sua biblioteca</p>
    </div>

    <div v-if="!loading" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
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

    <div v-if="loading" class="text-center py-12">
      <ion-icon name="hourglass-outline" class="text-4xl text-purple-600 animate-spin"></ion-icon>
      <p class="text-gray-600 mt-4">Carregando solicitações...</p>
    </div>

    <div v-else-if="solicitacoes.length === 0" class="text-center py-12 bg-white rounded-lg border border-gray-200">
      <ion-icon name="document-outline" class="text-6xl text-gray-400 mb-4"></ion-icon>
      <p class="text-gray-600 text-lg mb-2">Nenhuma ficha encontrada</p>
      <p class="text-gray-500 text-sm">Ainda não há fichas cadastradas nesta biblioteca</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div class="p-4 border-b border-gray-200 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Todas as Fichas</h2>
          <select
            v-model="filtroStatus"
            class="px-3 py-1.5 text-sm bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
          >
            <option value="todas">Todas</option>
            <option value="aguardando_autorizacao">Pendentes</option>
            <option value="aprovado">Aprovadas</option>
            <option value="negado">Negadas</option>
          </select>
        </div>
        <div class="divide-y divide-gray-200 max-h-[calc(100vh-300px)] overflow-y-auto">
          <div
            v-for="solicitacao in fichasFiltradas"
            :key="solicitacao.id"
            :class="[
              'p-4 transition-colors',
              solicitacaoSelecionada?.id === solicitacao.id ? 'bg-purple-50 border-l-4 border-purple-600' : 'hover:bg-gray-50'
            ]"
          >
            <div @click="selecionarSolicitacao(solicitacao)" class="cursor-pointer">
              <h3 class="font-semibold text-gray-900 mb-1">{{ solicitacao.titulo }}</h3>
              <p class="text-sm text-gray-600 mb-2">ID: {{ solicitacao.id_curto }}</p>
              <p class="text-sm text-gray-600 mb-2">Autor: {{ solicitacao.autor_nome_completo }}</p>
            <div class="flex items-center gap-2 mt-2">
              <span :class="[
                'inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full',
                solicitacao.status === 'aprovado' ? 'bg-green-100 text-green-800' :
                solicitacao.status === 'negado' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              ]">
                <ion-icon :name="
                  solicitacao.status === 'aprovado' ? 'checkmark-circle-outline' :
                  solicitacao.status === 'negado' ? 'close-circle-outline' :
                  'time-outline'
                "></ion-icon>
                {{ 
                  solicitacao.status === 'aprovado' ? 'Aprovado' :
                  solicitacao.status === 'negado' ? 'Negado' :
                  'Aguardando'
                }}
              </span>
              <span class="text-xs text-gray-500">
                {{ new Date(solicitacao.data_criacao).toLocaleDateString('pt-BR') }}
              </span>
            </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
        <div v-if="!solicitacaoSelecionada" class="p-12 text-center">
          <ion-icon name="document-outline" class="text-6xl text-gray-400 mb-4"></ion-icon>
          <p class="text-gray-600">Selecione uma solicitação para ver os detalhes</p>
        </div>

        <div v-else class="flex flex-col">
          <div class="p-4 border-b border-gray-200 flex-shrink-0">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h2 class="text-lg font-semibold text-gray-900 mb-1">{{ solicitacaoSelecionada.titulo }}</h2>
                <p class="text-sm text-gray-600">ID: {{ solicitacaoSelecionada.id_curto }}</p>
              </div>
              <button
                @click="solicitacaoSelecionada = null"
                class="text-gray-400 hover:text-gray-600"
              >
                <ion-icon name="close-outline" class="text-xl"></ion-icon>
              </button>
            </div>
          </div>

          <div class="p-4 flex-shrink-0">
            <div class="space-y-3 text-sm mb-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Autor</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.autor_nome_completo }}</p>
              </div>
              <div v-if="solicitacaoSelecionada.subtitulo">
                <label class="block text-xs font-medium text-gray-500 mb-1">Subtítulo</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.subtitulo }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Data</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.data_dia }}/{{ solicitacaoSelecionada.data_mes }}/{{ solicitacaoSelecionada.data_ano }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Cidade / Campus</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.cidade }} - {{ solicitacaoSelecionada.campus }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Programa / Curso</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.programa }} - {{ solicitacaoSelecionada.curso }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Palavras-chave</label>
                <p class="text-gray-900">{{ solicitacaoSelecionada.palavras_chave }}</p>
              </div>
            </div>
            <div class="pt-4 border-t border-gray-200 flex justify-end">
              <Button @click="verDetalhesCompletos">
                <ion-icon name="eye-outline"></ion-icon>
                Ver Detalhes Completos
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Modal :show="modalVer.show" @close="fecharModalVer" title="Detalhes da Solicitação" size="large">
      <div v-if="modalVer.solicitacao" class="space-y-6">
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Título</label>
            <p class="text-gray-900 font-semibold">{{ modalVer.solicitacao.titulo }}</p>
          </div>
          <div v-if="modalVer.solicitacao.subtitulo">
            <label class="block text-xs font-medium text-gray-500 mb-1">Subtítulo</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.subtitulo }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">ID</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.id_curto }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Autor</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.autor_nome_completo }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Data</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.data_dia }}/{{ modalVer.solicitacao.data_mes }}/{{ modalVer.solicitacao.data_ano }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Cidade / Campus</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.cidade }} - {{ modalVer.solicitacao.campus }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Programa / Curso</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.programa }} - {{ modalVer.solicitacao.curso }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Palavras-chave</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.palavras_chave }}</p>
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de Trabalho</label>
            <p class="text-gray-900">{{ modalVer.solicitacao.tipo_trabalho }}</p>
          </div>
        </div>

        <div class="border-t border-gray-200 pt-4">
          <div class="flex items-center justify-between mb-2">
            <label class="block text-xs font-medium text-gray-500">PDF do TCC</label>
            <button
              v-if="modalVer.pdfUrl"
              @click="abrirPdfNovaAbaModal"
              class="text-xs text-purple-600 hover:text-purple-700 flex items-center gap-1"
            >
              <ion-icon name="open-outline"></ion-icon>
              Abrir em nova aba
            </button>
          </div>
          <div class="border border-gray-200 rounded-lg overflow-hidden" style="height: 500px;">
            <iframe
              v-if="modalVer.pdfUrl"
              :src="modalVer.pdfUrl"
              class="w-full h-full border-0"
              type="application/pdf"
            ></iframe>
            <div v-else class="flex items-center justify-center h-full text-gray-500">
              <div class="text-center">
                <ion-icon name="document-outline" class="text-4xl mb-2"></ion-icon>
                <p class="text-sm">Carregando PDF...</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="modalVer.solicitacao?.status === 'aguardando_autorizacao'" class="flex gap-3 pt-4 border-t border-gray-200">
          <Button
            variant="outline"
            @click="aprovarNegarModal(false)"
            :loading="processando"
            class="flex-1"
          >
            <ion-icon name="close-circle-outline"></ion-icon>
            Negar
          </Button>
          <Button
            @click="aprovarNegarModal(true)"
            :loading="processando"
            class="flex-1"
          >
            <ion-icon name="checkmark-circle-outline"></ion-icon>
            Aprovar
          </Button>
        </div>
        <div v-else class="pt-4 border-t border-gray-200">
          <p class="text-sm text-gray-600 text-center">
            Esta ficha já foi 
            <span :class="
              modalVer.solicitacao?.status === 'aprovado' ? 'text-green-600 font-semibold' :
              'text-red-600 font-semibold'
            ">
              {{ modalVer.solicitacao?.status === 'aprovado' ? 'aprovada' : 'negada' }}
            </span>
          </p>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from '../components/UI/Button.vue'
import Modal from '../components/UI/Modal.vue'
import Card from '../components/UI/Card.vue'
import api from '../services/api'

const router = useRouter()

const solicitacoes = ref([])
const solicitacaoSelecionada = ref(null)
const loading = ref(false)
const processando = ref(false)
const pdfUrl = ref(null)
const filtroStatus = ref('todas')
const modalVer = ref({
  show: false,
  solicitacao: null,
  pdfUrl: null
})

const stats = computed(() => {
  return {
    totalFichas: solicitacoes.value.length,
    pendentes: solicitacoes.value.filter(s => s.status === 'aguardando_autorizacao').length,
    aprovadas: solicitacoes.value.filter(s => s.status === 'aprovado').length
  }
})

const fichasFiltradas = computed(() => {
  if (filtroStatus.value === 'todas') {
    return solicitacoes.value
  }
  return solicitacoes.value.filter(s => s.status === filtroStatus.value)
})

const carregarSolicitacoes = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/bibliotecarios/solicitacoes')
    solicitacoes.value = response.data
  } catch (error) {
    alert('Erro ao carregar solicitações. Tente novamente.')
  } finally {
    loading.value = false
  }
}

const selecionarSolicitacao = async (solicitacao) => {
  solicitacaoSelecionada.value = solicitacao
  pdfUrl.value = null
}

const verDetalhesCompletos = () => {
  if (solicitacaoSelecionada.value) {
    router.push(`/bibliotecario/solicitacao/${solicitacaoSelecionada.value.id}`)
  }
}

const abrirPdfNovaAba = () => {
  if (pdfUrl.value) {
    window.open(pdfUrl.value, '_blank')
  }
}

const abrirPdfNovaAbaModal = () => {
  if (modalVer.value.pdfUrl) {
    window.open(modalVer.value.pdfUrl, '_blank')
  }
}

const abrirModalVer = async (solicitacao) => {
  modalVer.value.show = true
  modalVer.value.solicitacao = solicitacao
  modalVer.value.pdfUrl = null
  
  try {
    const response = await api.get(`/api/bibliotecarios/solicitacoes/${solicitacao.id}/pdf`, {
      responseType: 'blob'
    })
    const blob = new Blob([response.data], { type: 'application/pdf' })
    modalVer.value.pdfUrl = URL.createObjectURL(blob)
  } catch (error) {
    modalVer.value.pdfUrl = null
  }
}

const fecharModalVer = () => {
  if (modalVer.value.pdfUrl) {
    URL.revokeObjectURL(modalVer.value.pdfUrl)
  }
  modalVer.value.show = false
  modalVer.value.solicitacao = null
  modalVer.value.pdfUrl = null
}

const aprovarNegarModal = async (aprovado) => {
  if (!modalVer.value.solicitacao) return
  
  const confirmacao = aprovado 
    ? confirm('Tem certeza que deseja aprovar esta ficha?')
    : confirm('Tem certeza que deseja negar esta ficha?')
  
  if (!confirmacao) return
  
  processando.value = true
  try {
    const response = await api.post(`/api/bibliotecarios/solicitacoes/${modalVer.value.solicitacao.id}/aprovacao`, {
      aprovado
    })
    
    const index = solicitacoes.value.findIndex(s => s.id === modalVer.value.solicitacao.id)
    if (index !== -1) {
      solicitacoes.value[index] = response.data.ficha
    }
    
    modalVer.value.solicitacao = response.data.ficha
    if (solicitacaoSelecionada.value?.id === modalVer.value.solicitacao.id) {
      solicitacaoSelecionada.value = response.data.ficha
    }
    
    alert(aprovado ? 'Ficha aprovada com sucesso!' : 'Ficha negada com sucesso!')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao processar solicitação. Tente novamente.'
    alert(errorMsg)
  } finally {
    processando.value = false
  }
}

watch(() => solicitacaoSelecionada.value, (newVal, oldVal) => {
  if (oldVal && pdfUrl.value) {
    URL.revokeObjectURL(pdfUrl.value)
  }
})

onMounted(() => {
  carregarSolicitacoes()
})
</script>
