import { useMemo } from 'react'
import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { useAuthStore } from '@/stores/authStore'
import { Clock, AlertTriangle } from 'lucide-react'
import type { Accident } from '@/types'

interface AccidentMarkerProps {
  incident: Accident
}

const formatTime = (dateString: string) => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(dateString))
}

export default function AccidentMarker({ incident }: AccidentMarkerProps) {
  const user = useAuthStore((state) => state.user)
  const isMine = user?.id === incident.reporter_id

  const customIcon = useMemo(() => {
    const bgColor = isMine ? 'bg-indigo-600' : 'bg-slate-600'
    const ringColor = isMine ? 'ring-indigo-200' : 'ring-slate-200'
    
    return L.divIcon({
      className: 'bg-transparent',
      html: `
        <div class="relative flex items-center justify-center w-8 h-8">
          <div class="w-4 h-4 rounded-full ${bgColor} border-2 border-white shadow-sm ring-4 ${ringColor}"></div>
          ${isMine ? '<div class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-amber-400 rounded-full border-2 border-white shadow-sm"></div>' : ''}
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16],
    })
  }, [isMine])

  const severityColors = {
    low: 'text-green-700 bg-green-100',
    medium: 'text-amber-700 bg-amber-100',
    high: 'text-red-700 bg-red-100',
  }

  return (
    <Marker 
      position={[incident.coordinates[0], incident.coordinates[1]]} 
      icon={customIcon}
      zIndexOffset={isMine ? 1000 : 0} 
    >
      <Popup className="custom-popup">
        <div className="space-y-3 min-w-50 max-w-70">
          <div className="flex items-start justify-between gap-3">
            <h4 className="font-semibold text-sm leading-tight text-slate-900">{incident.title}</h4>
            {isMine && (
              <span className="shrink-0 rounded bg-indigo-50 px-1.5 py-0.5 text-[9px] font-bold tracking-wider text-indigo-600 uppercase">
                Yours
              </span>
            )}
          </div>
          
          {incident.description && (
            <p className="text-xs text-slate-600">{incident.description}</p>
          )}

          <div className="grid grid-cols-1 gap-1.5 pt-2 border-t border-slate-100">
            <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
              <Clock className="h-3 w-3" />
              <span>Reported: {formatTime(incident.created_at)}</span>
            </div>
            
            {incident.starts_at && (
              <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
                <AlertTriangle className="h-3 w-3" />
                <span>Impact: {formatTime(incident.starts_at)} {incident.ends_at ? `- ${formatTime(incident.ends_at)}` : '(Ongoing)'}</span>
              </div>
            )}
          </div>
          
          <div className="flex flex-wrap gap-1.5 pt-1">
            <span className={`inline-block px-1.5 py-0.5 text-[10px] font-medium rounded uppercase ${severityColors[incident.severity]}`}>
              {incident.severity} Severity
            </span>
            <span className="inline-block px-1.5 py-0.5 text-[10px] font-medium rounded bg-slate-100 text-slate-800 uppercase">
              {incident.status}
            </span>
            <span className="inline-block px-1.5 py-0.5 text-[10px] font-medium rounded bg-slate-100 text-slate-800 uppercase">
              {incident.category.replace('_', ' ')}
            </span>
          </div>
        </div>
      </Popup>
    </Marker>
  )
}