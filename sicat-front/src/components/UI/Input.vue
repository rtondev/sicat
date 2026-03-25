<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-xs font-medium text-gray-600 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :class="[
        'w-full px-3 py-2 bg-white border border-gray-200 rounded-sm',
        'text-sm text-gray-900 placeholder:text-xs placeholder:text-gray-400',
        'focus:outline-none focus:ring-1 focus:ring-purple-500 focus:border-purple-500 hover:border-gray-400',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        error && 'border-red-500 focus:ring-red-500'
      ]"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-xs text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
defineProps({
  id: String,
  label: String,
  type: {
    type: String,
    default: 'text'
  },
  modelValue: [String, Number],
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  error: String,
  hint: String
})

defineEmits(['update:modelValue'])
</script>

