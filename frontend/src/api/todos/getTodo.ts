import axios from 'axios'
import type { Todo } from './types'

const GET_TODO_ENDPOINT =
  import.meta.env.VITE_API_TODOS_GET_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/get_todo'

export const getTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get<Todo>(`${GET_TODO_ENDPOINT}/${id}`)
  return response.data
}
