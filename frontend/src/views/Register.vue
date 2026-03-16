<template>
  <div class="min-h-[calc(100vh-200px)] flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div class="hidden lg:flex items-center justify-center">
        <img src="/user-book.svg" alt="Biblioteca" class="w-full max-w-md" />
      </div>

      <div class="w-full max-w-md mx-auto">
        <Card>

      <div class="mb-4">
        <div class="mb-3 text-center">
          <h2 class="text-lg font-semibold text-gray-900 mb-1">
            {{ stepTitle }}
          </h2>
          <p class="text-xs text-gray-600">
            {{ stepSubtitle }}
          </p>
        </div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-medium text-gray-600">Etapa {{ currentStep }} de 3</span>
          <span class="text-xs font-medium text-gray-600">{{ progressPercentage }}%</span>
        </div>
        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            class="h-full bg-purple-600 transition-all duration-300 rounded-full"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
        <div class="flex items-center justify-between mt-2">
          <span :class="['text-[10px] font-medium', currentStep >= 1 ? 'text-purple-600' : 'text-gray-400']">Validação</span>
          <span :class="['text-[10px] font-medium', currentStep >= 2 ? 'text-purple-600' : 'text-gray-400']">Confirmação</span>
          <span :class="['text-[10px] font-medium', currentStep >= 3 ? 'text-purple-600' : 'text-gray-400']">Senha</span>
        </div>
      </div>

      <div v-if="currentStep === 1" class="space-y-4">
        <Input
          id="matricula"
          label="Matrícula"
          v-model="form.matricula"
          placeholder="Digite sua matrícula"
          required
          :error="errors.matricula"
        />
        <Input
          id="senha_suap"
          label="Senha do SUAP"
          type="password"
          v-model="form.senha_suap"
          placeholder="Digite sua senha do SUAP"
          required
          :error="errors.senha_suap"
        />
         <div v-if="error" class="p-3 rounded-lg bg-red-50 border border-red-200">
          <p class="text-red-600 text-sm flex items-center gap-2">
            <ion-icon name="alert-circle-outline"></ion-icon>
            {{ error }}
          </p>
        </div>
      </div>

      <div v-else-if="currentStep === 2" class="space-y-4">
        <Card class="bg-purple-50 border-purple-200 p-4">
          <div class="space-y-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
              <p class="text-gray-900 font-medium">{{ suapDados?.nome || suapDados?.nome_registro || 'N/A' }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">CPF</label>
              <p class="text-gray-900">{{ suapDados?.cpf || 'N/A' }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Matrícula</label>
              <p class="text-gray-900">{{ form.matricula }}</p>
            </div>
            <div v-if="suapDados?.email || suapDados?.email_preferencial">
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <p class="text-gray-900">{{ suapDados?.email || suapDados?.email_preferencial || 'N/A' }}</p>
            </div>
            <div v-if="suapDados?.campus">
              <label class="block text-sm font-medium text-gray-700 mb-1">Campus</label>
              <p class="text-gray-900">{{ suapDados.campus }}</p>
            </div>
            <div v-if="suapDados?.tipo_usuario">
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Usuário</label>
              <p class="text-gray-900">{{ suapDados.tipo_usuario }}</p>
            </div>
          </div>
        </Card>
      </div>

      <div v-else class="space-y-4">
        <Input
          id="nova_senha"
          label="Nova Senha"
          type="password"
          v-model="form.nova_senha"
          placeholder="Digite sua nova senha"
          required
          :error="errors.nova_senha"
        />
        <div class="mt-1 p-3 rounded-lg bg-gray-50 border border-gray-200">
          <template v-if="!passwordChecks.allValid">
            <p class="text-xs font-medium text-gray-700 mb-2">Sua senha deve conter:</p>
            <ul class="space-y-1 text-xs list-none pl-0">
              <li class="flex items-center gap-2">
                <ion-icon
                  :name="passwordChecks.minLength ? 'checkmark-circle' : 'close-circle-outline'"
                  :class="passwordChecks.minLength ? 'text-green-500' : 'text-red-400'"
                ></ion-icon>
                <span :class="passwordChecks.minLength ? 'text-green-700' : 'text-red-600'">
                  Pelo menos 8 caracteres
                </span>
              </li>
              <li class="flex items-center gap-2">
                <ion-icon
                  :name="passwordChecks.hasUpper ? 'checkmark-circle' : 'close-circle-outline'"
                  :class="passwordChecks.hasUpper ? 'text-green-500' : 'text-red-400'"
                ></ion-icon>
                <span :class="passwordChecks.hasUpper ? 'text-green-700' : 'text-red-600'">
                  Uma letra maiúscula (A-Z)
                </span>
              </li>
              <li class="flex items-center gap-2">
                <ion-icon
                  :name="passwordChecks.hasLower ? 'checkmark-circle' : 'close-circle-outline'"
                  :class="passwordChecks.hasLower ? 'text-green-500' : 'text-red-400'"
                ></ion-icon>
                <span :class="passwordChecks.hasLower ? 'text-green-700' : 'text-red-600'">
                  Uma letra minúscula (a-z)
                </span>
              </li>
              <li class="flex items-center gap-2">
                <ion-icon
                  :name="passwordChecks.hasNumber ? 'checkmark-circle' : 'close-circle-outline'"
                  :class="passwordChecks.hasNumber ? 'text-green-500' : 'text-red-400'"
                ></ion-icon>
                <span :class="passwordChecks.hasNumber ? 'text-green-700' : 'text-red-600'">
                  Um número (0-9)
                </span>
              </li>
            </ul>
          </template>
          <template v-else>
            <div class="flex items-center gap-2 text-xs text-green-700">
              <ion-icon name="shield-checkmark-outline" class="text-green-500"></ion-icon>
              <span>Sua senha atende aos requisitos mínimos de segurança.</span>
            </div>
          </template>
        </div>
        <Input
          id="confirmar_senha"
          label="Confirmar Senha"
          type="password"
          v-model="form.confirmar_senha"
          placeholder="Confirme sua nova senha"
          required
          :error="errors.confirmar_senha"
        />
         <div v-if="error" class="p-3 rounded-lg bg-red-50 border border-red-200">
          <p class="text-red-600 text-sm flex items-center gap-2">
            <ion-icon name="alert-circle-outline"></ion-icon>
            {{ error }}
          </p>
        </div>
      </div>

          <div class="flex gap-3 mt-6">
            <template v-if="currentStep === 1">
              <Button
                type="button"
                @click="handleNextStep"
                :loading="validating"
                loading-text="Validando..."
                class="w-full"
              >
                Continuar
              </Button>
            </template>
            <template v-else-if="currentStep === 2">
              <Button
                type="button"
                variant="outline"
                @click="handleBackStep"
                class="flex-1"
              >
                Voltar
              </Button>
              <Button
                type="button"
                @click="currentStep = 3"
                class="flex-1"
              >
                Continuar
              </Button>
            </template>
            <template v-else>
              <Button
                type="button"
                variant="outline"
                @click="handleBackStep"
                class="flex-1"
              >
                Voltar
              </Button>
              <Button
                type="button"
                @click="handleRegister"
                :loading="loading"
                loading-text="Criando..."
                class="flex-1"
              >
                Criar Conta
              </Button>
            </template>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'
import Card from '../components/UI/Card.vue'
import Input from '../components/UI/Input.vue'
import Button from '../components/UI/Button.vue'

const router = useRouter()

const currentStep = ref(1)
const form = ref({
  matricula: '',
  senha_suap: '',
  nova_senha: '',
  confirmar_senha: ''
})

const errors = ref({})
const error = ref('')
const loading = ref(false)
const validating = ref(false)
const suapDados = ref(null)

const progressPercentage = computed(() => {
  return Math.round((currentStep.value / 3) * 100)
})

const stepTitle = computed(() => {
  if (currentStep.value === 1) return 'Validação de Identidade'
  if (currentStep.value === 2) return 'Confirmação de Dados'
  return 'Definir Senha'
})

const stepSubtitle = computed(() => {
  if (currentStep.value === 1) return 'Informe suas credenciais do SUAP'
  if (currentStep.value === 2) return 'Verifique os dados coletados do SUAP'
  return 'Crie uma nova senha para sua conta'
})

const passwordChecks = computed(() => {
  const value = form.value.nova_senha || ''
  return {
    minLength: value.length >= 8,
    hasUpper: /[A-Z]/.test(value),
    hasLower: /[a-z]/.test(value),
    hasNumber: /[0-9]/.test(value),
    get allValid() {
      return this.minLength && this.hasUpper && this.hasLower && this.hasNumber
    }
  }
})

const validateStep1 = () => {
  errors.value = {}
  
  if (!form.value.matricula) {
    errors.value.matricula = 'Matrícula é obrigatória'
    return false
  }
  
  if (!form.value.senha_suap) {
    errors.value.senha_suap = 'Senha do SUAP é obrigatória'
    return false
  }
  
  return true
}

const validateStep2 = () => {
  errors.value = {}
  
  if (!form.value.nova_senha) {
    errors.value.nova_senha = 'Nova senha é obrigatória'
  } else if (!passwordChecks.value.minLength || !passwordChecks.value.hasUpper || !passwordChecks.value.hasLower || !passwordChecks.value.hasNumber) {
    errors.value.nova_senha = 'A senha não atende aos requisitos mínimos'
  }
  
  if (!form.value.confirmar_senha) {
    errors.value.confirmar_senha = 'Confirmação de senha é obrigatória'
  } else if (form.value.nova_senha !== form.value.confirmar_senha) {
    errors.value.confirmar_senha = 'As senhas não coincidem'
  }
  
  return Object.keys(errors.value).length === 0
}

const handleBackStep = () => {
  error.value = ''
  errors.value = {}
  
  if (currentStep.value === 2) {
    localStorage.removeItem('suap_data')
    suapDados.value = null
    currentStep.value = 1
  } else if (currentStep.value === 3) {
    currentStep.value = 2
  }
}

const handleNextStep = async () => {
  error.value = ''
  errors.value = {}
  
  if (!validateStep1()) {
    return
  }
  
  validating.value = true
  
  try {
    const suapData = await authAPI.validateSuap(form.value.matricula, form.value.senha_suap)
    
    if (suapData && suapData.valido) {
      localStorage.setItem('suap_data', JSON.stringify({
        token: suapData.token,
        dados: suapData.dados
      }))
      suapDados.value = suapData.dados
      currentStep.value = 2
      error.value = ''
    } else {
      error.value = 'Credenciais do SUAP inválidas. Verifique sua matrícula e senha.'
    }
  } catch (err) {
    if (err.message === 'Credenciais do SUAP inválidas') {
      error.value = 'Credenciais do SUAP inválidas. Verifique sua matrícula e senha.'
    } else if (err.response?.status === 401) {
      error.value = 'Credenciais do SUAP inválidas. Verifique sua matrícula e senha.'
    } else if (err.response?.status === 400) {
      error.value = err.response?.data?.detail || 'Dados inválidos. Verifique as informações.'
    } else {
      error.value = 'Erro ao validar credenciais. Verifique sua conexão e tente novamente.'
    }
  } finally {
    validating.value = false
  }
}

const handleRegister = async () => {
  errors.value = {}
  error.value = ''
  
  if (!validateStep2()) {
    return
  }
  
  const suapDataStr = localStorage.getItem('suap_data')
  if (!suapDataStr) {
    error.value = 'Sessão expirada. Por favor, valide suas credenciais novamente.'
    currentStep.value = 1
    suapDados.value = null
    return
  }
  
  if (!suapDados.value) {
    try {
      const suapData = JSON.parse(suapDataStr)
      suapDados.value = suapData.dados
    } catch (e) {
      error.value = 'Erro ao carregar dados. Por favor, valide suas credenciais novamente.'
      currentStep.value = 1
      return
    }
  }
  
  loading.value = true

  try {
    const response = await authAPI.register(
      form.value.matricula,
      form.value.senha_suap,
      form.value.nova_senha,
      form.value.confirmar_senha
    )
    
    localStorage.removeItem('suap_data')
    
    setTimeout(() => {
      router.replace({
        path: '/login',
        query: { registro: 'sucesso' }
      })
    }, 500)
  } catch (err) {
    if (err.response?.status === 400) {
      error.value = err.response?.data?.detail || 'Dados inválidos. Verifique as informações.'
    } else if (err.response?.status === 401) {
      error.value = 'Credenciais do SUAP inválidas. Verifique sua matrícula e senha do SUAP.'
      currentStep.value = 1
      localStorage.removeItem('suap_data')
      suapDados.value = null
    } else if (err.response?.status === 409 || err.response?.status === 400) {
      const detail = err.response?.data?.detail || ''
      if (detail.includes('já cadastrado') || detail.includes('já cadastrada')) {
        error.value = 'Matrícula ou CPF já cadastrado. Faça login ou recupere sua senha.'
      } else {
        error.value = detail || 'Dados inválidos. Verifique as informações.'
      }
      currentStep.value = 1
      localStorage.removeItem('suap_data')
      suapDados.value = null
    } else {
      error.value = 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

