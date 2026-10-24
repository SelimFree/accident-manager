import { useAuthStore } from '@/stores/authStore'
import type { UserRole } from '@/types'

export function useHasRole(allowedRoles: UserRole | UserRole[]) {
  const user = useAuthStore((state) => state.user)

  if (!user) return false

  if (Array.isArray(allowedRoles)) {
    return allowedRoles.includes(user.role)
  }

  return user.role === allowedRoles
}