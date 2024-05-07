import axios from 'axios'
import router from '@/router'

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
    // const authStore = useAuthStore()
    if (!error.response) {
      return console.log('Network Error')
    }
    const status = error?.response?.status || null
    const url = error?.request?.responseURL || null
    if (status === 401) {
      if (!url?.includes('/logout')) {
        instance.post('auth/jwt/logout')
      }
      localStorage.removeItem('auth')
      router.push('/login')
    } else return Promise.reject(error)
  }
)

export default instance
