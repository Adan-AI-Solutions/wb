import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1'
const HEALTH_PATH = import.meta.env.VITE_API_HEALTH_PATH || '/healthz_endpoint'

export interface HealthResponse {
  status: string
  timestamp: string
  service: string
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
  const response = await axios.get<HealthResponse>(`${API_BASE_URL}${HEALTH_PATH}`)
  return response.data
}
