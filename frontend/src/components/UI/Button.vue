<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'rounded-lg font-medium transition-all duration-200 cursor-pointer',
      size === 'lg' ? 'px-6 py-3 text-lg' : size === 'sm' ? 'px-3 py-1.5 text-sm' : 'px-4 py-2',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white',
      variant === 'primary' 
        ? 'bg-purple-600 hover:bg-purple-700 text-white focus:ring-purple-500 disabled:bg-purple-400 disabled:cursor-not-allowed'
        : variant === 'outline'
        ? 'border border-gray-300 hover:bg-gray-100 text-gray-700 focus:ring-gray-400 disabled:opacity-50'
        : 'bg-gray-200 hover:bg-gray-300 text-gray-800 focus:ring-gray-400 disabled:opacity-50',
      loading && 'opacity-70 cursor-wait'
    ]"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="flex items-center justify-center gap-2">
      <ion-icon name="hourglass-outline" class="animate-spin"></ion-icon>
      <span>{{ loadingText || 'Carregando...' }}</span>
    </span>
    <span v-else class="flex items-center justify-center gap-2">
      <slot></slot>
    </span>
  </button>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary'
  },
  size: {
    type: String,
    default: 'md'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: null
  }
})

defineEmits(['click'])
</script>
