import type { IncidentCategory, IncidentSeverity } from '@/types'

export const CATEGORY_LABELS: Record<IncidentCategory, string> = {
  accident: 'Traffic Accident',
  road_work: 'Road Work',
  road_closure: 'Road Closure',
  pothole: 'Pothole',
  traffic_light: 'Broken Traffic Light',
  other: 'Other Incident'
}

export const SEVERITY_LABELS: Record<IncidentSeverity, string> = {
  high: 'High Severity',
  medium: 'Medium Severity',
  low: 'Low Severity'
}
