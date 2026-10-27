import { useEffect } from 'react'
import { useMap, useMapEvents } from 'react-leaflet'

interface LocationPickerProps {
  enabled: boolean
  onPick: (coordinates: [number, number]) => void
}

export default function LocationPicker({ enabled, onPick }: LocationPickerProps) {
  const map = useMap()

  useMapEvents({
    click: (e) => {
      if (!enabled) return
      // Wrap so longitudes stay within the -180..180 range the backend accepts
      const { lat, lng } = e.latlng.wrap()
      onPick([lat, lng])
    },
  })

  useEffect(() => {
    const container = map.getContainer()
    container.style.cursor = enabled ? 'crosshair' : ''
    return () => {
      container.style.cursor = ''
    }
  }, [map, enabled])

  return null
}
