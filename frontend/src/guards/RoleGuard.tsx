import type { ReactNode } from 'react'
import type { UserRole } from '@/types'
import { useHasRole } from '@/hooks/usesHasRole'

interface RoleGuardProps {
  allowedRoles: UserRole | UserRole[]
  children: ReactNode
  fallback?: ReactNode
}

export default function RoleGuard({ allowedRoles, children, fallback = null }: RoleGuardProps) {
  const hasRole = useHasRole(allowedRoles)

  if (!hasRole) {
    return <>{fallback}</>
  }

  return <>{children}</>
}