import { callCloudFunction } from '@/plugins/firebase'

export const deleteTodo = async (id: string): Promise<void> => {
  await callCloudFunction<void>('delete_todo', { id })
}
