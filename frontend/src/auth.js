import { ref } from 'vue'
import { me } from './api/sessions'

export const currentUser = ref(null)
let loaded = false

export async function loadUser() {
  if (loaded) return currentUser.value
  loaded = true
  currentUser.value = await me().catch(() => null)
  return currentUser.value
}

export function setUser(user) {
  loaded = true
  currentUser.value = user
}
