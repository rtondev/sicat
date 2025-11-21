<template>
  <div :class="['rounded-lg border border-gray-200 bg-white p-6', padding && `p-${padding}`]">
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  padding: String
})
</script>

