<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="text-center">
      <div class="flex justify-center mb-8">
        <ion-icon name="library-outline" class="text-6xl text-purple-600"></ion-icon>
      </div>
      <h1 class="text-5xl font-bold text-gray-900 mb-4">
        Sistema de Catalogação
      </h1>
      <p class="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
        Gerencie suas fichas catalográficas de forma simples e eficiente
      </p>
      <div class="flex gap-4 justify-center">
        <router-link to="/login" v-if="!isAuthenticated">
          <Button size="lg">
            <ion-icon name="log-in-outline"></ion-icon>
            Entrar
          </Button>
        </router-link>
        <router-link to="/register" v-if="!isAuthenticated">
          <Button variant="outline" size="lg">
            <ion-icon name="person-add-outline"></ion-icon>
            Criar Conta
          </Button>
        </router-link>
        <router-link to="/dashboard" v-if="isAuthenticated">
          <Button variant="outline" size="lg">
            <ion-icon name="grid-outline"></ion-icon>
            Dashboard
          </Button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from '../components/UI/Button.vue'

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('access_token')
})
</script>

