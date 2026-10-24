import type { NearbyFilters } from "@/features/map/map-filters"
import { useQuery } from "@tanstack/react-query"
import { accidentKeys } from "@/queries/accidents/accidentKeys"
import { publicApi } from "@/api/axios"
import type { Accident } from "@/types"

export function useNearbyAccidents(filters: NearbyFilters, enabled = true) {
  return useQuery({
    queryKey: accidentKeys.nearby(filters),
    queryFn: async () => {
      const { data } = await publicApi.get<Accident[]>('/api/accidents/nearby', {
        params: filters
      })
      return data
    },
    enabled,
  })
}