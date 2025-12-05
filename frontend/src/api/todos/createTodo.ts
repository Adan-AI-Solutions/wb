import axios from 'axios'
import type { Todo, TodoCreate } from './types'

const CREATE_TODO_ENDPOINT =
  import.meta.env.VITE_API_TODOS_CREATE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/create_todo'

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  const response = await axios.post<Todo>(CREATE_TODO_ENDPOINT, todo)
  return response.data
}
