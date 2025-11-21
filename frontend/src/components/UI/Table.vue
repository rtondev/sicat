<template>
  <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
    <div v-if="loading" class="text-center py-12">
      <ion-icon name="hourglass-outline" class="text-4xl text-purple-600 animate-spin"></ion-icon>
      <p class="text-gray-600 mt-4">{{ loadingText || 'Carregando...' }}</p>
    </div>

    <div v-else-if="items.length === 0" class="text-center py-12">
      <ion-icon :name="emptyIcon || 'document-outline'" class="text-6xl text-gray-400 mb-4"></ion-icon>
      <p class="text-gray-600 mb-4">{{ emptyText || 'Nenhum item encontrado' }}</p>
      <slot name="empty-action"></slot>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-100">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider',
                column.class
              ]"
            >
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(item, index) in items"
            :key="getItemKey(item, index)"
            class="hover:bg-gray-50 transition-colors"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              :class="['px-6 py-4 whitespace-nowrap', column.cellClass]"
            >
              <slot
                :name="`cell-${column.key}`"
                :item="item"
                :value="getNestedValue(item, column.key)"
                :column="column"
              >
                {{ getNestedValue(item, column.key) }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: 'Carregando...'
  },
  emptyText: {
    type: String,
    default: 'Nenhum item encontrado'
  },
  emptyIcon: {
    type: String,
    default: 'document-outline'
  },
  itemKey: {
    type: [String, Function],
    default: 'id'
  }
})

const getNestedValue = (obj, path) => {
  return path.split('.').reduce((current, prop) => current?.[prop], obj) ?? ''
}

const getItemKey = (item, index) => {
  if (typeof props.itemKey === 'function') {
    return props.itemKey(item, index)
  }
  return item[props.itemKey] ?? index
}
</script>


