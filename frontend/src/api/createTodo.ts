import { callCloudFunction } from '@/plugins/firebase'
import type { Todo, TodoCreate } from './todoTypes'

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  return await callCloudFunction<Todo>('create_todo', todo)
}
