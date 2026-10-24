import type { Accident, AccidentStatus } from "@/types"
import { useQuery } from "@tanstack/react-query"
import { accidentKeys } from "@/queries/accidents/accidentKeys"
import { privateApi } from "@/api/axios"

export function useAdminAccidents(status: AccidentStatus = 'pending', limit = 100) {
  return useQuery({
    queryKey: accidentKeys.adminQueue(status, limit),
    queryFn: async () => {
      const { data } = await privateApi.get<Accident[]>('/api/admin/accidents/', {
        params: { status, limit }
      })
      return data
    }
  })
}