import axios from 'axios'
import router from '@/router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/stores/auth'

const toast = useToast()

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT,
  withCredentials: true
})

// instance.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem('auth_token')
//     // If token exists, add it to the Authorization header
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`
//     }
//     return config
//   },
//   (error) => {
//     // Handle request errors
//     return Promise.reject(error)
//   }
// )

instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const authStore = useAuthStore()
    if (!error.response) {
      router.push('/login')
      toast.error('Network Error')
    }
    const status = error?.response?.status || null
    if (error.response.data && error.response.data.detail) {
      error.response.data.detail.forEach((element) => {
        toast.error(`${element.msg} ${element.loc[1]}`)
      })
      console.log(error.response.data)
      toast.error(`Missing ${error.response.data.detail.loc[1]}`)
    }
    if (status === 401) {
      authStore.setUser(null)
      router.push('/login')
    } else return Promise.reject(error)
  }
)

export default instance
