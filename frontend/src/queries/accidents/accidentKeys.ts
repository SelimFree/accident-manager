import type { NearbyFilters, PublicMapFilters } from "@/features/map/map-filters"
import type { AccidentStatus } from "@/types"

export const accidentKeys = {
  all: ['accidents'] as const,
  
  lists: () => [...accidentKeys.all, 'list'] as const,
  list: (filters: PublicMapFilters) => [...accidentKeys.lists(), { filters }] as const,
  
  nearbys: () => [...accidentKeys.all, 'nearby'] as const,
  nearby: (filters: NearbyFilters) => [...accidentKeys.nearbys(), { filters }] as const,
  
  mine: (limit?: number, offset?: number) => [...accidentKeys.all, 'mine', { limit, offset }] as const,
  
  adminQueue: (status?: AccidentStatus, limit?: number) => 
    [...accidentKeys.all, 'adminQueue', { status, limit }] as const,
    
  detail: (id: string) => [...accidentKeys.all, 'detail', id] as const,
}