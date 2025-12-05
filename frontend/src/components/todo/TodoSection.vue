<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Todo管理</h1>
    
    <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
      {{ error }}
    </div>

    <TodoForm
      :loading="loading"
      @submit="handleSubmit"
    />

    <TodoList
      :todos="todos"
      :loading="loading"
      @toggle="handleToggle"
      @delete="handleDelete"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TodoForm from './TodoForm.vue'
import TodoList from './TodoList.vue'
import type { Todo, TodoCreate } from '@/api/todoTypes'

interface Props {
  getTodos: () => Promise<Todo[]>
  createTodo: (todo: TodoCreate) => Promise<Todo>
  updateTodo: (id: string, todo: { completed: boolean }) => Promise<Todo>
  deleteTodo: (id: string) => Promise<void>
}

const props = defineProps<Props>()

// コンポーネント内で状態管理
const todos = ref<Todo[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const fetchTodos = async () => {
  loading.value = true
  error.value = null
  try {
    todos.value = await props.getTodos()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Todoの取得に失敗しました'
    console.error('Failed to fetch todos:', err)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async (data: TodoCreate) => {
  loading.value = true
  error.value = null
  try {
    const newTodo = await props.createTodo(data)
    todos.value.push(newTodo)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Todoの作成に失敗しました'
    console.error('Failed to create todo:', err)
  } finally {
    loading.value = false
  }
}

const handleToggle = async (id: string) => {
  loading.value = true
  error.value = null
  try {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      const updatedTodo = await props.updateTodo(id, { completed: !todo.completed })
      const index = todos.value.findIndex(t => t.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Todoの更新に失敗しました'
    console.error('Failed to update todo:', err)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id: string) => {
  if (confirm('このTodoを削除しますか？')) {
    loading.value = true
    error.value = null
    try {
      await props.deleteTodo(id)
      todos.value = todos.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Todoの削除に失敗しました'
      console.error('Failed to delete todo:', err)
    } finally {
      loading.value = false
    }
  }
}

onMounted(() => {
  fetchTodos()
})
</script>
