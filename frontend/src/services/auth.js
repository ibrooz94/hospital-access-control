import http from './api'

async function login(credentials) {
  let config = {
    headers: { 'Content-Type': 'multipart/form-data' }
  }
  return await http.post('auth/jwt/login', credentials, config)
}

async function register(input) {
  return await http.post('auth/jwt/register', input)
}
async function logout() {
  return await http.post('auth/jwt/logout')
}

export default {
  login,
  logout,
  register
}
