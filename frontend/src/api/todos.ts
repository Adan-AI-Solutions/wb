import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_V1_PREFIX = import.meta.env.VITE_API_V1_PREFIX || '/api/v1'

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
  const response = await axios.get<Todo[]>(`${API_BASE_URL}${API_V1_PREFIX}/todos/`)
  return response.data
}

export const getTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get<Todo>(`${API_BASE_URL}${API_V1_PREFIX}/todos/${id}`)
  return response.data
}

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  const response = await axios.post<Todo>(`${API_BASE_URL}${API_V1_PREFIX}/todos/`, todo)
  return response.data
}

export const updateTodo = async (id: string, todo: TodoUpdate): Promise<Todo> => {
  const response = await axios.patch<Todo>(`${API_BASE_URL}${API_V1_PREFIX}/todos/${id}`, todo)
  return response.data
}

export const deleteTodo = async (id: string): Promise<void> => {
  await axios.delete(`${API_BASE_URL}${API_V1_PREFIX}/todos/${id}`)
}

