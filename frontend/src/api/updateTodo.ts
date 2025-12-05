import { callCloudFunction } from '@/plugins/firebase'
import type { Todo, TodoUpdate } from './todoTypes'

export const updateTodo = async (id: string, todo: TodoUpdate): Promise<Todo> => {
  return await callCloudFunction<Todo>('update_todo', { id, ...todo })
}
