import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API } from '@/services'
// import { StorageSerializers, useStorageAsync } from '@vueuse/core'
import { computed } from 'vue'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const authUser = ref(null)

    // const authUser = useStorageAsync('authUser', {}, localStorage, {
    //   serializer: StorageSerializers.object,
    //   mergeDefaults: true
    // })

    // const error = ref(null)

    // function setError(value) {
    //   error.value = value
    // }
    const isAuthenticated = computed(() => authUser.value)
    const isAdmin = computed(() => authUser.value?.is_superuser)
    const userRole = computed(() => authUser.value?.role.name)

    function setUser(payload = null) {
      authUser.value = payload
    }

    async function dispatchCurrentUser() {
      try {
        const { status, data } = await API.user.getCurrentUser()
        if (status === 200) {
          setUser(data)
          return {
            success: true,
            content: data
          }
        }
      } catch (error) {
        const _error = error
        return {
          success: false,
          status: _error.response?.status,
          content: null
        }
      }
      return {
        success: false,
        content: null,
        status: 400
      }
    }

    async function dispatchLogin(credentials) {
      try {
        const { status } = await API.auth.login(credentials)
        if (status === 204) {
          return {
            success: true
          }
        }
      } catch (error) {
        // setError(error.response?.data?.detail)
        return {
          success: false,
          status: error.response?.status,
          content: error.response?.data
        }
      }
      return {
        success: false,
        content: null,
        status: 400
      }
    }
    async function dispatchLogout() {
      try {
        const { status } = await API.auth.logout()
        if (status === 204) {
          setUser(null)
          return {
            success: true
          }
        }
      } catch (error) {
        // setError(error)
        return {
          success: false,
          status: error.response?.status,
          content: error.response?.data
        }
      }
      return {
        success: false,
        content: null,
        status: 400
      }
    }

    return {
      authUser,
      userRole,
      isAuthenticated,
      isAdmin,
      setUser,
      dispatchCurrentUser,
      dispatchLogin,
      dispatchLogout
    }
  },
  { persist: true }
)
