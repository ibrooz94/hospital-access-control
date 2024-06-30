<script setup>
import { computed } from 'vue'
import OverlayLayer from '@/components/OverlayLayer.vue'


const props = defineProps({

  modelValue: {
    type: [String, Number, Boolean],
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const value = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const cancel = () => {
  value.value = false
}

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && value.value) {
    cancel()
  }
})
</script>

<template>
  <OverlayLayer v-show="value" @overlay-click="cancel">
    <!-- <div class="space-y-3"> -->
    <slot />
    <!-- </div> -->
  </OverlayLayer>
</template>
