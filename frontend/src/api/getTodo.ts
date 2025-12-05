import { callCloudFunction } from '@/plugins/firebase'
import type { Todo } from './todoTypes'

export const getTodo = async (id: string): Promise<Todo> => {
  return await callCloudFunction<Todo>('get_todo', { id })
}
