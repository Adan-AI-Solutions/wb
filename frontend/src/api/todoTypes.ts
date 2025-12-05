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
