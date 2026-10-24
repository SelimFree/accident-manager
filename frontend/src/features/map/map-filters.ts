export interface PublicMapFilters {
  limit?: number
  offset?: number
  west?: number | null
  south?: number | null
  east?: number | null
  north?: number | null
}

export interface NearbyFilters {
  lat: number
  lng: number
  radius_m?: number
}