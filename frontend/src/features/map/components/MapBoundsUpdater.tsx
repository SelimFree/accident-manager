import { useCallback, useEffect, useMemo } from 'react'
import { useMap, useMapEvents } from 'react-leaflet'
import { useMapStore } from '@/stores/mapStore'

export default function MapBoundsUpdater() {
  const map = useMap()
  const setBoundingBox = useMapStore((state) => state.setBoundingBox)

  const updateBounds = useCallback(() => {
    const bounds = map.getBounds()
    setBoundingBox({
      south: bounds.getSouth(),
      west: bounds.getWest(),
      north: bounds.getNorth(),
      east: bounds.getEast(),
    })
  }, [map, setBoundingBox])

  const handlers = useMemo(() => ({ moveend: updateBounds }), [updateBounds])
  useMapEvents(handlers)

  useEffect(() => {
    updateBounds()
  }, [updateBounds])

  return null
}