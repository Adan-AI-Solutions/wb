<template>
  <div class="home">
    <h1>WB Frontend</h1>
    <p>Welcome to WB Project</p>
    <div v-if="healthStatus">
      <p>Backend Status: {{ healthStatus.status }}</p>
      <p>Timestamp: {{ healthStatus.timestamp }}</p>
    </div>
    <button @click="checkHealth">Check Backend Health</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { checkBackendHealth } from '@/api/health'

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

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #35a372;
}
</style>

