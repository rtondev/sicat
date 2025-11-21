<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
          <ion-icon name="person-outline" class="text-purple-600"></ion-icon>
          Meu Perfil
        </h1>
        <p class="text-gray-600">Informações da sua conta</p>
      </div>
      <Button variant="outline" @click="showConfirmLogout = true">
        <ion-icon name="log-out-outline"></ion-icon>
        Sair
      </Button>
    </div>

    <Modal :show="showConfirmLogout" @close="showConfirmLogout = false" title="Confirmar Saída">
      <div class="space-y-4">
        <p class="text-gray-700">Tem certeza que deseja sair da sua conta?</p>
        <div class="flex gap-3 justify-end pt-4">
          <Button variant="outline" @click="showConfirmLogout = false">
            Cancelar
          </Button>
          <Button @click="confirmLogout">
            <ion-icon name="log-out-outline"></ion-icon>
            Sim, Sair
          </Button>
        </div>
      </div>
    </Modal>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <Card class="lg:col-span-2">
        <div v-if="loading" class="text-center py-12">
          <ion-icon name="hourglass-outline" class="text-4xl text-purple-600 animate-spin"></ion-icon>
          <p class="text-gray-600 mt-4">Carregando...</p>
        </div>

        <div v-else-if="user" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Nome Completo</label>
              <p class="text-gray-900 font-medium">{{ user.nome_completo || 'N/A' }}</p>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">CPF</label>
              <p class="text-gray-900 font-medium">{{ user.cpf || 'N/A' }}</p>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Matrícula</label>
              <p class="text-gray-900 font-medium">{{ user.matricula || 'N/A' }}</p>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de Usuário</label>
              <span :class="[
                'inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full',
                user.tipo === 'admin' ? 'bg-purple-100 text-purple-800' :
                user.tipo === 'bibliotecario' ? 'bg-blue-100 text-blue-800' :
                'bg-gray-100 text-gray-800'
              ]">
                <ion-icon :name="
                  user.tipo === 'admin' ? 'shield-checkmark-outline' :
                  user.tipo === 'bibliotecario' ? 'book-outline' :
                  'person-outline'
                "></ion-icon>
                {{ user.tipo === 'admin' ? 'Administrador' : 
                   user.tipo === 'bibliotecario' ? 'Bibliotecário' : 
                   'Usuário' }}
              </span>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Data de Registro</label>
              <p class="text-gray-900 font-medium">
                {{ new Date(user.data_registro).toLocaleString('pt-BR', { 
                  day: '2-digit', 
                  month: '2-digit', 
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                }) }}
              </p>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-500 mb-1">Última Edição</label>
              <p class="text-gray-900 font-medium">
                {{ new Date(user.data_edicao).toLocaleString('pt-BR', { 
                  day: '2-digit', 
                  month: '2-digit', 
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                }) }}
              </p>
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <div class="space-y-4">
          <div class="flex items-center gap-3 pb-4 border-b border-gray-200">
            <div class="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center">
              <ion-icon name="person-outline" class="text-3xl text-purple-600"></ion-icon>
            </div>
            <div>
              <p class="font-semibold text-gray-900">{{ user?.nome_completo || 'Usuário' }}</p>
              <p class="text-sm text-gray-600">{{ user?.matricula || '' }}</p>
            </div>
          </div>
          <div v-if="user?.biblioteca" class="pt-4">
            <label class="block text-xs font-medium text-gray-500 mb-2">Biblioteca Vinculada</label>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="font-medium text-gray-900">{{ user.biblioteca.nome }}</p>
              <p class="text-sm text-gray-600">{{ user.biblioteca.campus }}</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'
import Card from '../components/UI/Card.vue'
import Button from '../components/UI/Button.vue'
import Modal from '../components/UI/Modal.vue'

const router = useRouter()
const user = ref(null)
const loading = ref(true)
const showConfirmLogout = ref(false)

const confirmLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  localStorage.removeItem('user_nome')
  window.dispatchEvent(new Event('auth-changed'))
  router.push('/login')
}

onMounted(async () => {
  try {
    const data = await authAPI.getMe()
    user.value = data
  } catch (error) {
  } finally {
    loading.value = false
  }
})
</script>

