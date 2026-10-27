import { useMutation, useQueryClient } from "@tanstack/react-query"
import { accidentKeys } from "@/queries/accidents/accidentKeys"
import { privateApi } from "@/api/axios"
import type { Accident, IncidentCategory, IncidentSeverity } from "@/types"

export interface AccidentCreatePayload {
  title: string
  description: string | null
  category: IncidentCategory
  severity: IncidentSeverity
  coordinates: [number, number] // [lat, lng] WGS84
}

export function useCreateAccident() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (payload: AccidentCreatePayload) => {
      const { data } = await privateApi.post<Accident>('/api/accidents/', payload)
      return data
    },
    onSuccess: () => {
      // New reports are pending, so they only show up through the reporter's own list
      queryClient.invalidateQueries({ queryKey: [...accidentKeys.all, 'mine'] })
    },
  })
}
