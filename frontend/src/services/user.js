import http from './api'

async function getCurrentUser() {
  return await http.get('user/me')
}

export default {
  getCurrentUser
}
