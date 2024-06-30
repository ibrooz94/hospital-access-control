import http from './api'

async function getCurrentUser() {
  return await http.get('users/me')
}

export default {
  getCurrentUser
}
