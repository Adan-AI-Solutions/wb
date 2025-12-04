import axios from 'axios'

const LIST_ENDPOINT =
  import.meta.env.VITE_API_TODOS_LIST_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/list_todos'
const GET_ENDPOINT =
  import.meta.env.VITE_API_TODOS_GET_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/get_todo'
const CREATE_ENDPOINT =
  import.meta.env.VITE_API_TODOS_CREATE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/create_todo'
const UPDATE_ENDPOINT =
  import.meta.env.VITE_API_TODOS_UPDATE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/update_todo'
const DELETE_ENDPOINT =
  import.meta.env.VITE_API_TODOS_DELETE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/delete_todo'

export interface Todo {
  id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string | null
}

export interface TodoCreate {
  title: string
  description?: string | null
  completed?: boolean
}

export interface TodoUpdate {
  title?: string
  description?: string | null
  completed?: boolean
}

export const getTodos = async (): Promise<Todo[]> => {
  const response = await axios.get<Todo[]>(LIST_ENDPOINT)
  return response.data
}

export const getTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get<Todo>(`${GET_ENDPOINT}/${id}`)
  return response.data
}

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  const response = await axios.post<Todo>(CREATE_ENDPOINT, todo)
  return response.data
}

export const updateTodo = async (id: string, todo: TodoUpdate): Promise<Todo> => {
  const response = await axios.patch<Todo>(`${UPDATE_ENDPOINT}/${id}`, todo)
  return response.data
}

export const deleteTodo = async (id: string): Promise<void> => {
  await axios.delete(`${DELETE_ENDPOINT}/${id}`)
}
