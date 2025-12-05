import axios from 'axios'
import type { Todo } from './types'

const GET_TODOS_ENDPOINT =
  import.meta.env.VITE_API_TODOS_LIST_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/list_todos'

export const getTodos = async (): Promise<Todo[]> => {
  const response = await axios.get<Todo[]>(GET_TODOS_ENDPOINT)
  return response.data
}
