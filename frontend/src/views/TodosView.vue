<template>
  <TodoSection
    :get-todos="getTodos"
    :create-todo="createTodo"
    :update-todo="updateTodo"
    :delete-todo="deleteTodo"
  />
</template>

<script setup lang="ts">
import { getTodos, createTodo, updateTodo, deleteTodo } from '@/api/todos'
import TodoSection from '@/components/todo/TodoSection.vue'
</script>
