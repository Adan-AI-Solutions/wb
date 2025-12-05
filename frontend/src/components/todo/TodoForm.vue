<template>
  <div class="bg-gray-50 p-6 rounded-lg mb-6">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">新しいTodoを作成</h2>
    <form @submit.prevent="handleSubmit">
      <div class="space-y-4">
        <AInput
          id="todo-title"
          v-model="title"
          label="タイトル"
          placeholder="Todoのタイトルを入力"
          required
        />
        <ATextarea
          id="todo-description"
          v-model="description"
          label="説明"
          placeholder="説明を入力（任意）"
        />
        <AButton type="submit" :disabled="loading">
          {{ loading ? '作成中...' : '作成' }}
        </AButton>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import AInput from '../common/AInput.vue'
import ATextarea from '../common/ATextarea.vue'
import AButton from '../common/AButton.vue'
import type { TodoCreate } from '@/api/todoTypes'

interface Props {
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const title = ref('')
const description = ref('')

const formData = computed<TodoCreate>(() => ({
  title: title.value,
  description: description.value || null
}))

const emit = defineEmits<{
  submit: [data: TodoCreate]
}>()

const handleSubmit = () => {
  emit('submit', formData.value)
  title.value = ''
  description.value = ''
}

watch(() => props.loading, (newVal) => {
  if (!newVal) {
    // 送信成功後にフォームをリセット
    title.value = ''
    description.value = ''
  }
})
</script>
