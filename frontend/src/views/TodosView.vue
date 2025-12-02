<template>
  <div class="todos-view">
    <h1>Todo管理</h1>
    
    <div v-if="todosStore.error" class="error">
      {{ todosStore.error }}
    </div>

    <!-- Todo作成フォーム -->
    <div class="todo-form">
      <h2>新しいTodoを作成</h2>
      <form @submit.prevent="handleSubmit">
        <div>
          <label for="title">タイトル:</label>
          <input
            id="title"
            v-model="newTodo.title"
            type="text"
            required
            placeholder="Todoのタイトルを入力"
          />
        </div>
        <div>
          <label for="description">説明:</label>
          <textarea
            id="description"
            v-model="newTodo.description"
            placeholder="説明を入力（任意）"
            rows="3"
          />
        </div>
        <button type="submit" :disabled="todosStore.loading">
          {{ todosStore.loading ? '作成中...' : '作成' }}
        </button>
      </form>
    </div>

    <!-- Todo一覧 -->
    <div class="todos-list">
      <h2>Todo一覧 ({{ todosStore.todosCount }}件)</h2>
      
      <div v-if="todosStore.loading && todosStore.todos.length === 0" class="loading">
        読み込み中...
      </div>

      <div v-else-if="todosStore.todos.length === 0" class="empty">
        Todoがありません
      </div>

      <div v-else class="todo-items">
        <div
          v-for="todo in todosStore.todos"
          :key="todo.id"
          class="todo-item"
          :class="{ completed: todo.completed }"
        >
          <div class="todo-content">
            <input
              type="checkbox"
              :checked="todo.completed"
              @change="todosStore.toggleTodo(todo.id)"
            />
            <div class="todo-info">
              <h3>{{ todo.title }}</h3>
              <p v-if="todo.description">{{ todo.description }}</p>
              <small>
                作成: {{ formatDate(todo.created_at) }}
                <span v-if="todo.updated_at">
                  | 更新: {{ formatDate(todo.updated_at) }}
                </span>
              </small>
            </div>
          </div>
          <button
            @click="handleDelete(todo.id)"
            class="delete-btn"
            :disabled="todosStore.loading"
          >
            削除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTodosStore } from '@/stores/todos'
import type { TodoCreate } from '@/api/todos'

const todosStore = useTodosStore()

const newTodo = ref<TodoCreate>({
  title: '',
  description: null
})

const handleSubmit = async () => {
  try {
    await todosStore.addTodo(newTodo.value)
    newTodo.value = { title: '', description: null }
  } catch (error) {
    // エラーはstoreで処理済み
  }
}

const handleDelete = async (id: string) => {
  if (confirm('このTodoを削除しますか？')) {
    try {
      await todosStore.removeTodo(id)
    } catch (error) {
      // エラーはstoreで処理済み
    }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('ja-JP')
}

onMounted(() => {
  todosStore.fetchTodos()
})
</script>

<style scoped>
.todos-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  color: #2c3e50;
}

h2 {
  margin-top: 2rem;
  color: #42b983;
}

.error {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.todo-form {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.todo-form form > div {
  margin-bottom: 1rem;
}

.todo-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.todo-form input,
.todo-form textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.todo-form button {
  background-color: #42b983;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.todo-form button:hover:not(:disabled) {
  background-color: #35a372;
}

.todo-form button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.todos-list {
  margin-top: 2rem;
}

.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.todo-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: all 0.2s;
}

.todo-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.todo-item.completed {
  opacity: 0.7;
  background: #f0f0f0;
}

.todo-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.todo-content input[type="checkbox"] {
  margin-top: 0.25rem;
  cursor: pointer;
}

.todo-info {
  flex: 1;
}

.todo-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.todo-item.completed .todo-info h3 {
  text-decoration: line-through;
  color: #999;
}

.todo-info p {
  margin: 0.5rem 0;
  color: #666;
}

.todo-info small {
  color: #999;
  font-size: 0.875rem;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.delete-btn:hover:not(:disabled) {
  background-color: #c82333;
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

