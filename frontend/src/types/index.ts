export type UserRole = 'admin' | 'user'
export type AccidentStatus = 'pending' | 'approved' | 'rejected' | 'resolved'
export type IncidentCategory = 'accident' | 'road_work' | 'road_closure' | 'pothole' | 'traffic_light' | 'other'
export type IncidentSeverity = 'low' | 'medium' | 'high'

export interface User {
  id: string
  name: string
  email: string
  role: UserRole
}

export interface Accident {
  id: string
  reporter_id: string
  title: string
  description: string | null
  category: IncidentCategory
  severity: IncidentSeverity
  status: AccidentStatus
  is_deleted: boolean
  coordinates: [number, number] // [lat, lng] WGS84
  starts_at: string | null
  ends_at: string | null
  created_at: string
  updated_at: string
}
export interface Comment {
  id: string
  accident_id: string
  author_id: string
  author_name: string
  content: string
  created_at: string
  updated_at: string
}