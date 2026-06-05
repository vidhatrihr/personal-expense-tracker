import { ref } from 'vue'
import { apiRequest } from '@/utils/api.js'

const user = ref(null)
const fetched = ref(false)

export function useWhoAmI() {
  async function whoAmI() {
    if (fetched.value) {
      return user.value
    }
    try {
      const res = await apiRequest('/whoami')
      fetched.value = true
      if (!res.ok) {
        user.value = null
        return null
      }
      const json = await res.json()
      user.value = json.data
      return json.data
    } catch {
      user.value = null
      fetched.value = false
      return null
    }
  }

  function clearUser() {
    user.value = null
    fetched.value = false
  }

  return { whoAmI, user, clearUser }
}
