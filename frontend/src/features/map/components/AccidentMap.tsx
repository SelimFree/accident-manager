import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import '@/features/map/leaflet-config'

const MOCK_INCIDENTS = [
  {
    id: '33333333-3333-3333-3333-333333333333',
    title: 'Major Pothole on Main Bridge',
    description: 'Deep pothole causing traffic slowdowns in the right lane.',
    status: 'pending',
    position: [47.4979, 19.0402] as [number, number],
  },
  {
    id: '44444444-4444-4444-4444-444444444444',
    title: 'Broken Traffic Light',
    description: 'Traffic light at the intersection is completely off.',
    status: 'in_progress',
    position: [47.5000, 19.0600] as [number, number],
  },
]

export default function AccidentMap() {
  return (
    <div className="h-full w-full">
      <MapContainer
        center={[47.4979, 19.0402]}
        zoom={13}
        scrollWheelZoom={true}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {MOCK_INCIDENTS.map((incident) => (
          <Marker key={incident.id} position={incident.position}>
            <Popup>
              <div className="space-y-1">
                <h4 className="font-semibold text-sm">{incident.title}</h4>
                <p className="text-xs text-slate-600">{incident.description}</p>
                <span className="inline-block px-1.5 py-0.5 text-[10px] font-medium rounded bg-amber-100 text-amber-800 uppercase">
                  {incident.status}
                </span>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}