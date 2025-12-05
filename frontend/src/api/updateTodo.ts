import axios from 'axios'
import type { Todo, TodoUpdate } from './todoTypes'

const UPDATE_TODO_ENDPOINT =
  import.meta.env.VITE_API_TODOS_UPDATE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/update_todo'

export const updateTodo = async (id: string, todo: TodoUpdate): Promise<Todo> => {
  const response = await axios.patch<Todo>(`${UPDATE_TODO_ENDPOINT}/${id}`, todo)
  return response.data
}
