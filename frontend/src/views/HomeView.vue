<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">WB Frontend</h1>
      <p class="text-lg text-gray-600">Welcome to WB Project</p>
    </div>

    <div v-if="healthStatus" class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Backend Status</h2>
      <div class="space-y-2">
        <p class="text-gray-700">
          <span class="font-medium">Status:</span>
          <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 rounded">{{ healthStatus.status }}</span>
        </p>
        <p class="text-gray-700">
          <span class="font-medium">Timestamp:</span>
          <span class="ml-2">{{ healthStatus.timestamp }}</span>
        </p>
      </div>
    </div>

    <div class="text-center">
      <AButton @click="checkHealth">Check Backend Health</AButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { checkBackendHealth } from '@/api/health'
import AButton from '@/components/common/AButton.vue'

const healthStatus = ref<{ status: string; timestamp: string } | null>(null)

const checkHealth = async () => {
  try {
    const response = await checkBackendHealth()
    healthStatus.value = response
  } catch (error) {
    console.error('Failed to check backend health:', error)
    alert('Backend接続に失敗しました')
  }
}
</script>

