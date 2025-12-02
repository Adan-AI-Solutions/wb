<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="container mx-auto px-4">
        <div class="flex space-x-6 py-4">
          <router-link
            to="/"
            class="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            Home
          </router-link>
          <router-link
            to="/todos"
            class="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            Todos
          </router-link>
          <router-link
            to="/about"
            class="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            About
          </router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts">
// App component
</script>

