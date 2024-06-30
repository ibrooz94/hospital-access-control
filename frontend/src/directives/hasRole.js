import { ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  mounted(el, binding) {
    const { value } = binding
    const authStore = useAuthStore()
    const userRole = ref(authStore.userRole)
    watch(
      userRole,
      (newValRole) => {
        if (value && Array.isArray(value) && value.length > 0) {
          const hasRequiredRole = value.includes(newValRole) || authStore.isAdmin // Check for role or admin status
          if (!hasRequiredRole) {
            el.parentNode && el.parentNode.removeChild(el)
          }
        }
      },
      { immediate: true } // Run the check initially
    )
  }
}
