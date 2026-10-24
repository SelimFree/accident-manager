import { useCallback, useEffect, useMemo, useRef } from 'react'
import { useMap, useMapEvents } from 'react-leaflet'
import { useMapStore } from '@/stores/mapStore'

export default function MapBoundsUpdater() {
  const map = useMap()
  const setBoundingBox = useMapStore((state) => state.setBoundingBox)
  const lastBoundsRef = useRef<string | null>(null)

  const updateBounds = useCallback(() => {
    const bounds = map.getBounds()
    
    const newBounds = {
      south: bounds.getSouth(),
      west: bounds.getWest(),
      north: bounds.getNorth(),
      east: bounds.getEast(),
    }

    const boundsKey = `${newBounds.south},${newBounds.west},${newBounds.north},${newBounds.east}`

    if (lastBoundsRef.current !== boundsKey) {
      lastBoundsRef.current = boundsKey
      setBoundingBox(newBounds)
    }
  }, [map, setBoundingBox])

  const handlers = useMemo(() => ({ moveend: updateBounds }), [updateBounds])
  useMapEvents(handlers)

  useEffect(() => {
    updateBounds()
  }, [updateBounds])

  return null
}