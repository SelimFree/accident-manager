import { publicApi } from "@/api/axios"
import type { PublicMapFilters } from "@/features/map/map-filters"
import type { Accident } from "@/types"
import { keepPreviousData, useQuery } from "@tanstack/react-query"
import { accidentKeys } from "@/queries/accidents/accidentKeys"

export function usePublicAccidents(filters: PublicMapFilters) {
  return useQuery({
    queryKey: accidentKeys.list(filters),
    queryFn: async () => {
      const { data } = await publicApi.get<Accident[]>('/api/accidents/', {
        params: filters 
      })
      return data
    },
    placeholderData: keepPreviousData,
  })
}