<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <textarea
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :rows="rows"
      :class="[
        'w-full px-4 py-2 bg-white border border-gray-300 rounded-lg',
        'text-gray-900 placeholder-gray-400 resize-none',
        'focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        error && 'border-red-500 focus:ring-red-500'
      ]"
      @input="$emit('update:modelValue', $event.target.value)"
    ></textarea>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-xs text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
defineProps({
  id: String,
  label: String,
  modelValue: String,
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  rows: {
    type: Number,
    default: 4
  },
  error: String,
  hint: String
})

defineEmits(['update:modelValue'])
</script>

