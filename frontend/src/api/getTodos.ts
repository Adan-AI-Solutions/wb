import { callCloudFunction } from '@/plugins/firebase'
import type { Todo } from './todoTypes'

export const getTodos = async (): Promise<Todo[]> => {
  return await callCloudFunction<Todo[]>('list_todos')
}
