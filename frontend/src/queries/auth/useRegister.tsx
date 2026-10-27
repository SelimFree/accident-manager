import { useMutation } from '@tanstack/react-query'
import { publicApi } from '@/api/axios'
import type { User } from '@/types'

export interface RegisterPayload {
  name: string
  email: string
  password: string
}

export function useRegister() {
  return useMutation({
    mutationFn: async (payload: RegisterPayload) => {
      const { data } = await publicApi.post<User>('/api/auth/register', payload)
      return data
    },
  })
}
