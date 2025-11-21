<template>
  <div class="min-h-[calc(100vh-200px)] flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div class="hidden lg:flex items-center justify-center">
        <img src="/user-books.svg" alt="Biblioteca" class="w-full max-w-lg" />
      </div>

      <div class="w-full max-w-md mx-auto">
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <div class="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center">
              <ion-icon name="library-outline" class="text-3xl text-purple-600"></ion-icon>
            </div>
          </div>
          <h1 class="text-xl font-bold text-gray-900 mb-2">Entrar</h1>
          <p class="text-gray-600">Acesse sua conta para continuar</p>
        </div>

        <Card>
        <div
          v-if="showSuccessMessage"
          class="mb-6 p-4 rounded-lg bg-green-50 border border-green-200"
        >
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <ion-icon name="checkmark-circle" class="text-xl text-green-600"></ion-icon>
            </div>
            <div class="flex-1">
              <h3 class="text-green-700 font-semibold mb-1 text-sm">Conta criada com sucesso!</h3>
              <p class="text-green-600 text-xs">
                Sua conta foi criada com sucesso. Agora você pode fazer login para acessar o sistema.
              </p>
            </div>
            <button
              @click="showSuccessMessage = false"
              class="flex-shrink-0 text-green-600 hover:text-green-700 transition-colors"
            >
              <ion-icon name="close-outline" class="text-lg"></ion-icon>
            </button>
          </div>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <Input
            id="matricula"
            label="Matrícula"
            v-model="form.matricula"
            placeholder="Digite sua matrícula"
            required
            :error="errors.matricula"
          />
          <Input
            id="senha"
            label="Senha"
            type="password"
            v-model="form.senha"
            placeholder="Digite sua senha"
            required
            :error="errors.senha"
          />
          
          <div v-if="error" class="p-3 rounded-lg bg-red-50 border border-red-200">
            <p class="text-red-600 text-sm flex items-center gap-2">
              <ion-icon name="alert-circle-outline"></ion-icon>
              {{ error }}
            </p>
          </div>

          <div class="flex gap-3">
            <router-link to="/register" class="flex-1">
              <Button variant="outline" class="w-full">
                Criar conta
              </Button>
            </router-link>
            <Button
              type="submit"
              :loading="loading"
              loading-text="Entrando..."
              class="flex-1"
            >
              Entrar
            </Button>
          </div>
        </form>
      </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authAPI } from '../services/api'
import Card from '../components/UI/Card.vue'
import Input from '../components/UI/Input.vue'
import Button from '../components/UI/Button.vue'

const router = useRouter()
const route = useRoute()

const form = ref({
  matricula: '',
  senha: ''
})

const errors = ref({})
const error = ref('')
const loading = ref(false)
const showSuccessMessage = ref(false)

const checkSuccessMessage = () => {
  const registro = route.query.registro
  if (registro === 'sucesso' || registro === 'true') {
    showSuccessMessage.value = true
    setTimeout(() => {
      router.replace({ query: {} })
    }, 200)
  }
}

onMounted(() => {
  checkSuccessMessage()
})

watch(() => route.query.registro, (newVal) => {
  if (newVal === 'sucesso' || newVal === 'true') {
    showSuccessMessage.value = true
    setTimeout(() => {
      router.replace({ query: {} })
    }, 200)
  }
}, { immediate: true })

const handleLogin = async () => {
  errors.value = {}
  error.value = ''
  
  if (!form.value.matricula) {
    errors.value.matricula = 'Matrícula é obrigatória'
    return
  }
  
  if (!form.value.senha) {
    errors.value.senha = 'Senha é obrigatória'
    return
  }
  
  loading.value = true

  try {
    const response = await authAPI.login(form.value.matricula, form.value.senha)
    
    localStorage.setItem('access_token', response.token)
    localStorage.setItem('user_role', response.tipo || '')
    
    try {
      const userData = await authAPI.getMe()
      localStorage.setItem('user_nome', userData.nome_completo || '')
      localStorage.setItem('user_role', userData.tipo || response.tipo || '')
    } catch (e) {
    }
    
    window.dispatchEvent(new Event('auth-changed'))
    
    router.push('/dashboard')
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Usuário ou senha incorretos'
    } else {
      error.value = 'Erro ao fazer login. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

