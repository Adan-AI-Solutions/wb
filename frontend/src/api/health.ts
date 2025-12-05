import { callCloudFunction } from '@/plugins/firebase'

export interface HealthResponse {
  status: string
  timestamp: string
  service: string
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
  return await callCloudFunction<HealthResponse>('healthz_endpoint')
}
