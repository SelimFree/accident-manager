import { useQuery } from "@tanstack/react-query"
import { accidentKeys } from "@/queries/accidents/accidentKeys"
import { privateApi } from "@/api/axios"
import type { Accident } from "@/types"

export function useMyAccidents(enabled: boolean, limit = 100, offset = 0) {
  return useQuery({
    queryKey: accidentKeys.mine(limit, offset),
    queryFn: async () => {
      const { data } = await privateApi.get<Accident[]>('/api/accidents/mine', {
        params: { limit, offset }
      })
      return data
    },
    enabled,
  })
}