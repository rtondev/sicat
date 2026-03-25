<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
            <ion-icon name="add-circle-outline" class="text-purple-600"></ion-icon>
            Nova Ficha Catalográfica
          </h1>
          <p class="text-gray-600">Preencha os dados da ficha catalográfica</p>
        </div>
        <Button
          type="button"
          variant="outline"
          @click="preencherDadosAleatorios"
          class="flex items-center gap-2"
        >
          <ion-icon name="shuffle-outline"></ion-icon>
          Preencher com Dados Aleatórios
        </Button>
      </div>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Dados do Autor</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="Nome Completo" v-model="form.autor_nome_completo" required />
            <Input label="Sobrenome" v-model="form.autor_sobrenome" required />
            <Input label="Nome sem Último Sobrenome" v-model="form.autor_nome_sem_ultimo_sobrenome" required />
            <Input label="Último Sobrenome" v-model="form.autor_ultimo_sobrenome" required />
          </div>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Dados do Trabalho</h2>
          <div class="space-y-4">
            <Input label="Título" v-model="form.titulo" required />
            <Input label="Subtítulo" v-model="form.subtitulo" />
            <div class="grid grid-cols-3 gap-4">
              <Input label="Dia" v-model="form.data_dia" placeholder="DD" required />
              <Input label="Mês" v-model="form.data_mes" placeholder="MM" required />
              <Input label="Ano" v-model="form.data_ano" placeholder="AAAA" required />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <Input label="Cidade" v-model="form.cidade" required />
              <Input label="Campus" v-model="form.campus" required />
            </div>
            <Input label="Programa" v-model="form.programa" required />
            <Input label="Nível de Ensino" v-model="form.nivel_ensino" required />
            <Input label="Curso" v-model="form.curso" required />
            <Textarea label="Palavras-chave" v-model="form.palavras_chave" required />
            <Input label="Tipo de Trabalho" v-model="form.tipo_trabalho" placeholder="Ex: TCC" required />
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Biblioteca <span class="text-red-500">*</span>
              </label>
              <select
                v-model="form.biblioteca_id"
                required
                class="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                :disabled="loadingBibliotecas"
              >
                <option value="">Selecione uma biblioteca</option>
                <option
                  v-for="biblioteca in bibliotecas"
                  :key="biblioteca.id"
                  :value="biblioteca.id"
                >
                  {{ biblioteca.nome }} - {{ biblioteca.campus }}
                </option>
              </select>
              <p v-if="loadingBibliotecas" class="mt-1 text-xs text-gray-500">Carregando bibliotecas...</p>
              <p v-else-if="bibliotecas.length === 0" class="mt-1 text-xs text-red-600">
                Nenhuma biblioteca disponível. Entre em contato com o administrador.
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">PDF do TCC</label>
              <div class="flex items-center gap-4">
                <label
                  for="pdf_tcc"
                  class="flex cursor-pointer items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 hover:bg-gray-50 transition-colors"
                >
                  <ion-icon name="document-attach-outline"></ion-icon>
                  {{ pdfFile ? pdfFile.name : 'Selecionar PDF' }}
                </label>
                <input
                  id="pdf_tcc"
                  type="file"
                  accept="application/pdf"
                  @change="handleFileChange"
                  class="hidden"
                />
                <button
                  v-if="pdfFile"
                  type="button"
                  @click="pdfFile = null"
                  class="text-sm text-red-500 hover:text-red-400"
                >
                  Remover
                </button>
              </div>
              <div class="mt-2 space-y-1">
                <p v-if="pdfFile" class="text-sm text-gray-900">
                  Tamanho: <span class="font-medium">{{ formatFileSize(pdfFile.size) }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-4 pt-4">
          <Button type="button" variant="outline" @click="$router.back()">
            <ion-icon name="close-outline"></ion-icon>
            Cancelar
          </Button>
          <Button type="submit" :loading="loading" loading-text="Criando...">
            <ion-icon name="checkmark-outline"></ion-icon>
            Criar Ficha
          </Button>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Card from '../components/UI/Card.vue'
import Input from '../components/UI/Input.vue'
import Textarea from '../components/UI/Textarea.vue'
import Button from '../components/UI/Button.vue'
import api from '../services/api'

const router = useRouter()

const form = ref({
  autor_nome_completo: '',
  autor_sobrenome: '',
  autor_nome_sem_ultimo_sobrenome: '',
  autor_ultimo_sobrenome: '',
  titulo: '',
  subtitulo: '',
  data_dia: '',
  data_mes: '',
  data_ano: '',
  cidade: '',
  campus: '',
  programa: '',
  nivel_ensino: '',
  curso: '',
  palavras_chave: '',
  tipo_trabalho: '',
  biblioteca_id: ''
})

const pdfFile = ref(null)
const loading = ref(false)
const bibliotecas = ref([])
const loadingBibliotecas = ref(false)

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const handleFileChange = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    if (file.type !== 'application/pdf') {
      alert('Apenas arquivos PDF são permitidos')
      e.target.value = ''
      return
    }
    pdfFile.value = file
  }
}

const preencherDadosAleatorios = () => {
  const nomes = ['Maria', 'João', 'Ana', 'Pedro', 'Carla', 'Lucas', 'Juliana', 'Rafael']
  const sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Costa', 'Ferreira', 'Almeida', 'Pereira']
  const nomesCompletos = [
    'Maria Silva Santos',
    'João Pedro Oliveira',
    'Ana Carolina Souza',
    'Pedro Henrique Costa',
    'Carla Beatriz Ferreira',
    'Lucas Gabriel Almeida',
    'Juliana Maria Pereira',
    'Rafael Augusto Lima'
  ]
  
  const orientadores = [
    'Prof. Dr. Carlos Eduardo Mendes',
    'Prof. Dra. Fernanda Rodrigues',
    'Prof. Dr. Roberto Alves',
    'Prof. Dra. Patricia Santos'
  ]
  
  const coorientadores = [
    'Prof. Me. André Luiz',
    'Prof. Dra. Luciana Martins',
    null
  ]
  
  const titulos = [
    'Análise de Sistemas de Informação',
    'Desenvolvimento de Aplicações Web',
    'Inteligência Artificial e Machine Learning',
    'Banco de Dados e Big Data',
    'Segurança da Informação',
    'Engenharia de Software',
    'Redes de Computadores',
    'Sistemas Embarcados'
  ]
  
  const subtitulos = [
    'Uma Abordagem Prática',
    'Estudo de Caso',
    'Aplicações em Ambiente Real',
    'Análise Comparativa',
    null
  ]
  
  const cidades = ['Natal', 'Mossoró', 'Caicó', 'Currais Novos', 'Pau dos Ferros']
  const campus = ['Natal - Central', 'Mossoró', 'Caicó', 'Currais Novos', 'Pau dos Ferros']
  const programas = ['Técnico em Informática', 'Técnico em Redes', 'Superior em Tecnologia']
  const niveis = ['Técnico', 'Superior', 'Pós-graduação']
  const cursos = [
    'Técnico em Informática',
    'Técnico em Redes de Computadores',
    'Tecnologia em Análise e Desenvolvimento de Sistemas',
    'Tecnologia em Redes de Computadores'
  ]
  
  const palavrasChave = [
    'Sistemas de Informação, Desenvolvimento Web, Tecnologia',
    'Inteligência Artificial, Machine Learning, Python',
    'Banco de Dados, MySQL, PostgreSQL',
    'Segurança, Criptografia, Redes',
    'Software, Engenharia, Metodologias Ágeis'
  ]
  
  const tiposTrabalho = ['TCC', 'Monografia', 'Dissertação', 'Tese']
  
  const nomeCompleto = nomesCompletos[Math.floor(Math.random() * nomesCompletos.length)]
  const partesNome = nomeCompleto.split(' ')
  const ultimoSobrenome = partesNome[partesNome.length - 1]
  const nomeSemUltimo = partesNome.slice(0, -1).join(' ')
  const sobrenome = partesNome.slice(1).join(' ')
  
  const orientador = orientadores[Math.floor(Math.random() * orientadores.length)]
  const partesOrientador = orientador.split(' ')
  const orientadorSobrenome = partesOrientador.slice(-2).join(' ')
  const orientadorNomeSemUltimo = partesOrientador.slice(1, -2).join(' ')
  const orientadorUltimoSobrenome = partesOrientador[partesOrientador.length - 1]
  
  const coorientador = coorientadores[Math.floor(Math.random() * coorientadores.length)]
  let coorientadorNomeCompleto = null
  let coorientadorSobrenome = null
  let coorientadorNomeSemUltimo = null
  let coorientadorUltimoSobrenome = null
  
  if (coorientador) {
    coorientadorNomeCompleto = coorientador
    const partesCoorientador = coorientador.split(' ')
    coorientadorSobrenome = partesCoorientador.slice(-2).join(' ')
    coorientadorNomeSemUltimo = partesCoorientador.slice(1, -2).join(' ')
    coorientadorUltimoSobrenome = partesCoorientador[partesCoorientador.length - 1]
  }
  
  const hoje = new Date()
  const dia = String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')
  const mes = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')
  const ano = String(hoje.getFullYear() - Math.floor(Math.random() * 5))
  
  form.value = {
    autor_nome_completo: nomeCompleto,
    autor_sobrenome: sobrenome,
    autor_nome_sem_ultimo_sobrenome: nomeSemUltimo,
    autor_ultimo_sobrenome: ultimoSobrenome,
    orientador_nome_completo: orientador,
    orientador_sobrenome: orientadorSobrenome,
    orientador_nome_sem_ultimo_sobrenome: orientadorNomeSemUltimo,
    orientador_ultimo_sobrenome: orientadorUltimoSobrenome,
    coorientador_nome_completo: coorientadorNomeCompleto,
    coorientador_sobrenome: coorientadorSobrenome,
    coorientador_nome_sem_ultimo_sobrenome: coorientadorNomeSemUltimo,
    coorientador_ultimo_sobrenome: coorientadorUltimoSobrenome,
    titulo: titulos[Math.floor(Math.random() * titulos.length)],
    subtitulo: subtitulos[Math.floor(Math.random() * subtitulos.length)],
    data_dia: dia,
    data_mes: mes,
    data_ano: ano,
    cidade: cidades[Math.floor(Math.random() * cidades.length)],
    campus: campus[Math.floor(Math.random() * campus.length)],
    programa: programas[Math.floor(Math.random() * programas.length)],
    nivel_ensino: niveis[Math.floor(Math.random() * niveis.length)],
    curso: cursos[Math.floor(Math.random() * cursos.length)],
    palavras_chave: palavrasChave[Math.floor(Math.random() * palavrasChave.length)],
    tipo_trabalho: tiposTrabalho[Math.floor(Math.random() * tiposTrabalho.length)],
    biblioteca_id: bibliotecas.value.length > 0 ? bibliotecas.value[Math.floor(Math.random() * bibliotecas.value.length)].id : ''
  }
}

const carregarBibliotecas = async () => {
  loadingBibliotecas.value = true
  try {
    const response = await api.get('/api/public/bibliotecas')
    bibliotecas.value = response.data
  } catch (error) {
    alert('Erro ao carregar bibliotecas. Tente novamente.')
  } finally {
    loadingBibliotecas.value = false
  }
}

const handleSubmit = async () => {
  if (!form.value.biblioteca_id) {
    alert('Por favor, selecione uma biblioteca')
    return
  }
  
  loading.value = true
  
  try {
    const formData = new FormData()
    
    formData.append('ficha_json', JSON.stringify(form.value))
    
    if (pdfFile.value) {
      formData.append('pdf_tcc', pdfFile.value)
    }
    
    await api.post('/api/fichas/', formData)
    
    router.push('/fichas')
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 'Erro ao criar ficha. Tente novamente.'
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  carregarBibliotecas()
})
</script>

