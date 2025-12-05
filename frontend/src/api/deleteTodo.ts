import axios from 'axios'

const DELETE_TODO_ENDPOINT =
  import.meta.env.VITE_API_TODOS_DELETE_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/delete_todo'

export const deleteTodo = async (id: string): Promise<void> => {
  await axios.delete(`${DELETE_TODO_ENDPOINT}/${id}`)
}
