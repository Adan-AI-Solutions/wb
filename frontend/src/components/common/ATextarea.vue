<template>
  <div>
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
    </label>
    <textarea
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :rows="rows"
      :class="textareaClass"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id?: string
  label?: string
  modelValue: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  rows?: number
}

const props = withDefaults(defineProps<Props>(), {
  required: false,
  disabled: false,
  rows: 3
})

defineEmits<{
  'update:modelValue': [value: string]
}>()

const textareaClass = computed(() => {
  const base = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
  const disabled = props.disabled ? 'bg-gray-100 cursor-not-allowed' : ''
  return `${base} ${disabled}`
})
</script>

