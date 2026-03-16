<template>
  <div :class="['p-6 rounded-3xl border border-gray-100 bg-gray-100', padding && `p-${padding}`]">
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  padding: String
})
</script>

