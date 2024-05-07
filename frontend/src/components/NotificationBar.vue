<script setup>
import { ref, computed, useSlots, onMounted } from 'vue'
import { mdiClose } from '@mdi/js'
import { colorsBgLight, colorsOutline } from '@/colors.js'
import BaseLevel from '@/components/BaseLevel.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import BaseButton from '@/components/BaseButton.vue'

const props = defineProps({
  icon: {
    type: String,
    default: null
  },
  outline: Boolean,
  color: {
    type: String,
    required: true
  },
  autoDismiss: {
    type: Boolean,
    default: false
  }
})

const componentClass = computed(() =>
  props.outline ? colorsOutline[props.color] : colorsBgLight[props.color]
)

const isDismissed = ref(false)

onMounted(() => {
  if (props.autoDismiss) {
    setTimeout(() => {
      isDismissed.value = true
    }, 5500);
  }
})

const dismiss = () => {
  isDismissed.value = true
}

const slots = useSlots()

const hasRightSlot = computed(() => slots.right)
</script>

<template>
  <div v-if="!isDismissed" :class="componentClass"
    class="px-3 py-6 md:py-3 mb-6 last:mb-0 border rounded-lg transition-colors duration-150">
    <BaseLevel>
      <div class="flex flex-col md:flex-row items-center">
        <BaseIcon v-if="icon" :path="icon" w="w-10 md:w-5" h="h-10 md:h-5" size="24" class="md:mr-2" />
        <span class="text-center md:text-left md:py-2">
          <slot />
        </span>
      </div>
      <slot v-if="hasRightSlot" name="right" />
      <div v-else class="pl-6">
        <BaseButton :icon="mdiClose" small rounded-full color="white" @click="dismiss" />
      </div>
    </BaseLevel>
  </div>
</template>
