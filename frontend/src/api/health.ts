import axios from 'axios'

const HEALTH_ENDPOINT =
  import.meta.env.VITE_API_HEALTH_ENDPOINT ||
  'http://localhost:5001/wb-dev-480009/asia-northeast1/healthz_endpoint'

export interface HealthResponse {
  status: string
  timestamp: string
  service: string
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
  const response = await axios.get<HealthResponse>(HEALTH_ENDPOINT)
  return response.data
}
