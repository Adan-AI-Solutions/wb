<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-800 mb-4">
      Todo一覧 ({{ todos.length }}件)
    </h2>
    
    <div v-if="loading && todos.length === 0" class="text-center py-8 text-gray-500">
      読み込み中...
    </div>

    <div v-else-if="todos.length === 0" class="text-center py-8 text-gray-500">
      Todoがありません
    </div>

    <div v-else class="space-y-3">
      <TodoItem
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        :loading="loading"
        @toggle="$emit('toggle', $event)"
        @delete="$emit('delete', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import TodoItem from './TodoItem.vue'
import type { Todo } from '@/api/todos'

interface Props {
  todos: Todo[]
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false
})

defineEmits<{
  toggle: [id: string]
  delete: [id: string]
}>()
</script>

