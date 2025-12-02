<template>
  <div
    class="flex items-start justify-between p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
    :class="{ 'opacity-70 bg-gray-50': todo.completed }"
  >
    <div class="flex items-start gap-3 flex-1">
      <input
        type="checkbox"
        :checked="todo.completed"
        @change="$emit('toggle', todo.id)"
        class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
      />
      <div class="flex-1">
        <h3
          class="text-lg font-medium text-gray-800"
          :class="{ 'line-through text-gray-500': todo.completed }"
        >
          {{ todo.title }}
        </h3>
        <p v-if="todo.description" class="mt-1 text-sm text-gray-600">
          {{ todo.description }}
        </p>
        <small class="text-xs text-gray-400 mt-2 block">
          作成: {{ formatDate(todo.created_at) }}
          <span v-if="todo.updated_at" class="ml-2">
            | 更新: {{ formatDate(todo.updated_at) }}
          </span>
        </small>
      </div>
    </div>
    <AButton
      variant="danger"
      size="sm"
      :disabled="loading"
      @click="$emit('delete', todo.id)"
    >
      削除
    </AButton>
  </div>
</template>

<script setup lang="ts">
import AButton from '../common/AButton.vue'
import type { Todo } from '@/api/todos'

interface Props {
  todo: Todo
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false
})

defineEmits<{
  toggle: [id: string]
  delete: [id: string]
}>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('ja-JP')
}
</script>

