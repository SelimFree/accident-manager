import { useMutation } from '@tanstack/react-query'
import { publicApi } from '@/api/axios'
import { useAuthStore } from '@/stores/authStore'
import type { User } from '@/types'

export function useLogin() {
  const setAuth = useAuthStore((state) => state.setAuth)

  return useMutation({
    mutationFn: async (credentials: Record<string, string>) => {
      const tokenResponse = await publicApi.post<{ access_token: string }>('/api/auth/login', credentials)
      const token = tokenResponse.data.access_token


      const userResponse = await publicApi.get<User>('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      return { token, user: userResponse.data }
    },
    onSuccess: (data) => {
      setAuth(data.token, data.user)
    },
  })
}