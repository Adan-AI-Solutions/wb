import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Todo, TodoCreate, TodoUpdate } from '@/api/todos'
import * as todoApi from '@/api/todos'

export const useTodosStore = defineStore('todos', () => {
  const todos = ref<Todo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const completedTodos = computed(() => todos.value.filter(todo => todo.completed))
  const activeTodos = computed(() => todos.value.filter(todo => !todo.completed))
  const todosCount = computed(() => todos.value.length)

  const fetchTodos = async () => {
    loading.value = true
    error.value = null
    try {
      todos.value = await todoApi.getTodos()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Todoの取得に失敗しました'
      console.error('Failed to fetch todos:', err)
    } finally {
      loading.value = false
    }
  }

  const addTodo = async (todo: TodoCreate) => {
    loading.value = true
    error.value = null
    try {
      const newTodo = await todoApi.createTodo(todo)
      todos.value.push(newTodo)
      return newTodo
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Todoの作成に失敗しました'
      console.error('Failed to create todo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTodo = async (id: string, updates: TodoUpdate) => {
    loading.value = true
    error.value = null
    try {
      const updatedTodo = await todoApi.updateTodo(id, updates)
      const index = todos.value.findIndex(t => t.id === id)
      if (index !== -1) {
        todos.value[index] = updatedTodo
      }
      return updatedTodo
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Todoの更新に失敗しました'
      console.error('Failed to update todo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeTodo = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      await todoApi.deleteTodo(id)
      todos.value = todos.value.filter(t => t.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Todoの削除に失敗しました'
      console.error('Failed to delete todo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const toggleTodo = async (id: string) => {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      await updateTodo(id, { completed: !todo.completed })
    }
  }

  return {
    todos,
    loading,
    error,
    completedTodos,
    activeTodos,
    todosCount,
    fetchTodos,
    addTodo,
    updateTodo,
    removeTodo,
    toggleTodo
  }
})

