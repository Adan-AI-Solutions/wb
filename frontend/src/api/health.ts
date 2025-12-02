import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface HealthResponse {
  status: string
  timestamp: string
  service: string
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
  const response = await axios.get<HealthResponse>(`${API_BASE_URL}/healthz`)
  return response.data
}

