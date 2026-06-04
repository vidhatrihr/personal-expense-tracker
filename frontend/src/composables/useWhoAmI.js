import { useRouter } from 'vue-router'
import { apiRequest } from '@/utils/api.js'

export function useWhoAmI() {
  const router = useRouter()

  // Checks the current session. Returns user data or null if unauthenticated.
  async function whoAmI() {
    const res = await apiRequest('/whoami')
    if (!res.ok) {
      router.push('/')
      return null
    }
    const json = await res.json()
    return json.data
  }

  return { whoAmI }
}
