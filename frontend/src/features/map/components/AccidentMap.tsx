import '@/features/map/leaflet-config'
import { MapContainer, TileLayer } from 'react-leaflet'
import { AlertCircle, Plus } from 'lucide-react'
import PageFullScreenLoader from '@/components/layout/PageFullScreenLoader'
import { usePublicAccidents } from '@/queries/accidents/usePublicAccidents'
import MapFilters from '@/features/map/components//MapFilter'
import MapBoundsUpdater from '@/features/map/components/MapBoundsUpdater'
import { useMapStore } from '@/stores/mapStore'
import { useMyAccidents } from '@/queries/accidents/useMyAccidents'
import { useAuthStore } from '@/stores/authStore'
import { useMemo } from 'react'
import type { Accident } from '@/types'
import AccidentMarker from '@/features/map/components/AccidentMarker'
import {Button} from "@/components/ui/button"

const INITIAL_CENTER: [number, number] = [47.4979, 19.0402]
const INITIAL_ZOOM = 13

export default function AccidentMap() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  const filters = useMapStore((state) => state.filters)
  const activeCategories = useMapStore((state) => state.categories)
  const activeSeverities = useMapStore((state) => state.severities)

  // const [isReportModalOpen, setIsReportModalOpen] = useState(false)

  const {
    data: publicAccidents = [],
    isFetching: isPublicFetching,
    isError: isPublicError
  } = usePublicAccidents(filters)

  const {
    data: myAccidents = []
  } = useMyAccidents(isAuthenticated)

  const allAccidents = useMemo(() => {
    const uniqueAccidents = new Map<string, Accident>()
    publicAccidents.forEach(acc => uniqueAccidents.set(acc.id, acc))
    myAccidents.forEach(acc => uniqueAccidents.set(acc.id, acc))

    return Array.from(uniqueAccidents.values())
  }, [publicAccidents, myAccidents])

  const filteredAccidents = allAccidents.filter((incident) => {
    return (
      activeCategories.includes(incident.category) &&
      activeSeverities.includes(incident.severity)
    )
  })

  if (isPublicError) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-slate-50 text-slate-600 gap-2">
        <AlertCircle className="h-5 w-5 text-red-500" />
        <span>Failed to load incident data. Please refresh the page.</span>
      </div>
    )
  }

  const isInitialLoad = isPublicFetching && publicAccidents.length === 0

  return (
    <div className="h-full w-full relative">
      {isInitialLoad && <PageFullScreenLoader />}

      <MapFilters />

      {isAuthenticated && (
        <Button
          // onClick={() => setIsReportModalOpen(true)}
          size="icon"
          className="absolute bottom-6 right-6 z-1000 h-14 w-14 rounded-full shadow-xl hover:scale-105 transition-transform"
          title="Report New Incident"
        >
          <Plus className="h-6 w-6" />
        </Button>
      )}

      {/* {isReportModalOpen && (
        <ReportIncidentModal onClose={() => setIsReportModalOpen(false)} />
      )} */}

      <MapContainer
        center={INITIAL_CENTER}
        zoom={INITIAL_ZOOM}
        scrollWheelZoom={true}
        className="h-full w-full isolate z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapBoundsUpdater />

        {filteredAccidents.map((incident) => (
          <AccidentMarker key={incident.id} incident={incident} />
        ))}
      </MapContainer>
    </div>
  )
}