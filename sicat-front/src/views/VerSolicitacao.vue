<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <button
          @click="$router.back()"
          class="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-2"
        >
          <ion-icon name="arrow-back-outline"></ion-icon>
          <span class="text-sm">Voltar</span>
        </button>
        <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
          <ion-icon name="document-text-outline" class="text-purple-600"></ion-icon>
          Detalhes da Solicitação
        </h1>
        <p v-if="solicitacao" class="text-gray-600">ID: {{ solicitacao.id_curto }}</p>
      </div>
      <div v-if="solicitacao && solicitacao.status === 'aguardando_autorizacao'" class="flex gap-3">
        <Button
          variant="outline"
          @click="aprovarNegar(false)"
          :loading="processando"
        >
          <ion-icon name="close-circle-outline"></ion-icon>
          Negar
        </Button>
        <Button
          @click="aprovarNegar(true)"
          :loading="processando"
        >
          <ion-icon name="checkmark-circle-outline"></ion-icon>
          Aprovar
        </Button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-12">
      <ion-icon name="hourglass-outline" class="text-4xl text-purple-600 animate-spin"></ion-icon>
      <p class="text-gray-600 mt-4">Carregando...</p>
    </div>

    <div v-else-if="solicitacao" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <Card class="lg:col-span-2 flex flex-col h-[calc(100vh-200px)]">
        <div class="flex items-center justify-between mb-4 flex-shrink-0">
          <h2 class="text-lg font-semibold text-gray-900">PDF do TCC</h2>
          <Button
            v-if="pdfUrl"
            variant="outline"
            size="sm"
            @click="abrirPdfNovaAba"
          >
            <ion-icon name="open-outline"></ion-icon>
            Abrir em Nova Aba
          </Button>
        </div>
        <div class="flex-1 border border-gray-200 rounded-lg overflow-hidden min-h-0">
          <iframe
            v-if="pdfUrl"
            :src="`${pdfUrl}#toolbar=0&navpanes=0&scrollbar=0`"
            class="w-full h-full border-0"
            type="application/pdf"
          ></iframe>
          <div v-else class="flex items-center justify-center h-full text-gray-500">
            <div class="text-center">
              <ion-icon name="document-outline" class="text-4xl mb-2"></ion-icon>
              <p class="text-sm">PDF não disponível</p>
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <div class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Informações da Ficha</h2>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Título</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.titulo }}</p>
              </div>
              <div v-if="solicitacao.subtitulo">
                <label class="block text-xs font-medium text-gray-500 mb-1">Subtítulo</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.subtitulo }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">ID</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.id_curto }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Status</label>
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
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Autor</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.autor_nome_completo }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Data</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.data_dia }}/{{ solicitacao.data_mes }}/{{ solicitacao.data_ano }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Cidade</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.cidade }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Campus</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.campus }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Programa</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.programa }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Nível de Ensino</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.nivel_ensino }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Curso</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.curso }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de Trabalho</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.tipo_trabalho }}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Palavras-chave</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.palavras_chave }}</p>
              </div>
              <div v-if="solicitacao.orientador_nome_completo">
                <label class="block text-xs font-medium text-gray-500 mb-1">Orientador</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.orientador_nome_completo }}</p>
              </div>
              <div v-if="solicitacao.coorientador_nome_completo">
                <label class="block text-xs font-medium text-gray-500 mb-1">Coorientador</label>
                <p class="text-gray-900 font-medium">{{ solicitacao.coorientador_nome_completo }}</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <Modal :show="showConfirmModal" @close="showConfirmModal = false" title="Confirmar Ação">
      <div class="space-y-4">
        <p class="text-gray-700">
          {{ acaoConfirmar === 'aprovar' 
            ? 'Tem certeza que deseja aprovar esta ficha?' 
            : 'Tem certeza que deseja negar esta ficha?' }}
        </p>
        <div class="flex gap-3 justify-end pt-4">
          <Button variant="outline" @click="showConfirmModal = false">
            Cancelar
          </Button>
          <Button 
            :variant="acaoConfirmar === 'aprovar' ? 'primary' : 'outline'"
            @click="confirmarAcao"
            :loading="processando"
          >
            <ion-icon :name="acaoConfirmar === 'aprovar' ? 'checkmark-circle-outline' : 'close-circle-outline'"></ion-icon>
            {{ acaoConfirmar === 'aprovar' ? 'Sim, Aprovar' : 'Sim, Negar' }}
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Card from '../components/UI/Card.vue'
import Button from '../components/UI/Button.vue'
import Modal from '../components/UI/Modal.vue'
import api from '../services/api'

const router = useRouter()
const route = useRoute()

const solicitacao = ref(null)
const pdfUrl = ref(null)
const loading = ref(true)
const processando = ref(false)
const showConfirmModal = ref(false)
const acaoConfirmar = ref(null)

const carregarSolicitacao = async () => {
  loading.value = true
  const solicitacaoId = route.params.id
  
  try {
    const response = await api.get('/api/bibliotecarios/solicitacoes')
    const solicitacoes = response.data
    solicitacao.value = solicitacoes.find(s => s.id === solicitacaoId)
    
    if (!solicitacao.value) {
      alert('Solicitação não encontrada')
      router.push('/bibliotecario')
      return
    }
    
    if (solicitacao.value.pdf_tcc) {
      try {
        const pdfResponse = await api.get(`/api/bibliotecarios/solicitacoes/${solicitacaoId}/pdf`, {
          responseType: 'blob'
        })
        const blob = new Blob([pdfResponse.data], { type: 'application/pdf' })
        pdfUrl.value = URL.createObjectURL(blob)
      } catch (error) {
        pdfUrl.value = null
      }
    } else {
      pdfUrl.value = null
    }
  } catch (error) {
    alert('Erro ao carregar solicitação. Tente novamente.')
    router.push('/bibliotecario')
  } finally {
    loading.value = false
  }
}

const aprovarNegar = (aprovado) => {
  acaoConfirmar.value = aprovado ? 'aprovar' : 'negar'
  showConfirmModal.value = true
}

const confirmarAcao = async () => {
  if (!solicitacao.value) return
  
  const aprovado = acaoConfirmar.value === 'aprovar'
  
  processando.value = true
  try {
    const response = await api.post(`/api/bibliotecarios/solicitacoes/${solicitacao.value.id}/aprovacao`, {
      aprovado
    })
    
    solicitacao.value = response.data.ficha
    showConfirmModal.value = false
    
    alert(aprovado ? 'Ficha aprovada com sucesso!' : 'Ficha negada com sucesso!')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao processar solicitação. Tente novamente.'
    alert(errorMsg)
  } finally {
    processando.value = false
  }
}

const abrirPdfNovaAba = () => {
  if (pdfUrl.value) {
    window.open(pdfUrl.value, '_blank')
  }
}

watch(() => route.params.id, () => {
  carregarSolicitacao()
})

onMounted(() => {
  carregarSolicitacao()
})
</script>

