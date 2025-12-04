import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1'
const LIST_PATH = import.meta.env.VITE_API_TODOS_LIST_PATH || '/list_todos'
const GET_PATH = import.meta.env.VITE_API_TODOS_GET_PATH || '/get_todo'
const CREATE_PATH = import.meta.env.VITE_API_TODOS_CREATE_PATH || '/create_todo'
const UPDATE_PATH = import.meta.env.VITE_API_TODOS_UPDATE_PATH || '/update_todo'
const DELETE_PATH = import.meta.env.VITE_API_TODOS_DELETE_PATH || '/delete_todo'

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
  const response = await axios.get<Todo[]>(`${API_BASE_URL}${LIST_PATH}`)
  return response.data
}

export const getTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get<Todo>(`${API_BASE_URL}${GET_PATH}/${id}`)
  return response.data
}

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  const response = await axios.post<Todo>(`${API_BASE_URL}${CREATE_PATH}`, todo)
  return response.data
}

export const updateTodo = async (id: string, todo: TodoUpdate): Promise<Todo> => {
  const response = await axios.patch<Todo>(`${API_BASE_URL}${UPDATE_PATH}/${id}`, todo)
  return response.data
}

export const deleteTodo = async (id: string): Promise<void> => {
  await axios.delete(`${API_BASE_URL}${DELETE_PATH}/${id}`)
}
