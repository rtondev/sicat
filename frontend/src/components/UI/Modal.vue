<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="$emit('close')"
      >
        <div class="absolute inset-0 bg-black/30 backdrop-blur-sm"></div>
        
        <div :class="[
          'relative bg-white rounded-lg shadow-xl w-full max-h-[90vh] overflow-y-auto',
          size === 'large' ? 'max-w-5xl' : 'max-w-md'
        ]">
          <div class="p-6">
            <div v-if="title || $slots.header" class="flex items-center justify-between mb-4">
              <div v-if="title" class="flex-1">
                <h2 class="text-xl font-semibold text-gray-900">{{ title }}</h2>
              </div>
              <div v-else-if="$slots.header" class="flex-1">
                <slot name="header"></slot>
              </div>
              <button
                @click="$emit('close')"
                class="text-gray-400 hover:text-gray-600 transition-colors ml-4 flex-shrink-0"
              >
                <ion-icon name="close-outline" class="text-2xl"></ion-icon>
              </button>
            </div>
            
            <div>
              <slot></slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

defineEmits(['close'])
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.95);
  opacity: 0;
}
</style>

