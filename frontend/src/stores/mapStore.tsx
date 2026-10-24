import type { PublicMapFilters } from '@/features/map/map-filters'
import type { IncidentCategory, IncidentSeverity } from '@/types'
import { create } from 'zustand'

interface MapState {
    filters: PublicMapFilters
    categories: IncidentCategory[]
    severities: IncidentSeverity[]

    setBoundingBox: (bounds: { west: number; south: number; east: number; north: number }) => void
    setLimit: (limit: number) => void
    toggleCategory: (category: IncidentCategory) => void
    toggleSeverity: (severity: IncidentSeverity) => void
    resetFilters: () => void
}

const ALL_CATEGORIES: IncidentCategory[] = ['accident', 'road_work', 'road_closure', 'pothole', 'traffic_light', 'other']
const ALL_SEVERITIES: IncidentSeverity[] = ['low', 'medium', 'high']

export const useMapStore = create<MapState>((set) => ({
    filters: {
        limit: 100,
        west: null,
        south: null,
        east: null,
        north: null,
    },
    categories: ALL_CATEGORIES,
    severities: ALL_SEVERITIES,

    setBoundingBox: (bounds) => set((state) => ({ 
        filters: { ...state.filters, ...bounds } 
    })),

    setLimit: (limit) => set((state) => ({ 
        filters: { ...state.filters, limit } 
    })),

    toggleCategory: (category) => set((state) => ({
        categories: state.categories.includes(category)
            ? state.categories.filter((c) => c !== category)
            : [...state.categories, category]
    })),

    toggleSeverity: (severity) => set((state) => ({
        severities: state.severities.includes(severity)
            ? state.severities.filter((s) => s !== severity)
            : [...state.severities, severity]
    })),

    resetFilters: () => set({
        categories: ALL_CATEGORIES,
        severities: ALL_SEVERITIES,
    })
}))