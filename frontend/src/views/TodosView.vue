<template>
  <TodoSection
    :get-todos="getTodos"
    :create-todo="createTodo"
    :update-todo="updateTodo"
    :delete-todo="deleteTodo"
  />
</template>

<script setup lang="ts">
import { getTodos } from '@/api/getTodos'
import { createTodo } from '@/api/createTodo'
import { updateTodo } from '@/api/updateTodo'
import { deleteTodo } from '@/api/deleteTodo'
import TodoSection from '@/components/todo/TodoSection.vue'
</script>
