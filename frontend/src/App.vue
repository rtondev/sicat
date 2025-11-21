<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <Header />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

const route = useRoute()

const showFooter = computed(() => {
  const routesWithFooter = ['/login', '/register']
  return routesWithFooter.includes(route.path)
})
</script>
