import { useEffect, useState } from 'react'
import { useMap, useMapEvents, Marker } from 'react-leaflet'
import type L from 'leaflet'
import { ghostIcon } from '@/features/map/leaflet-config'

interface LocationPickerProps {
  enabled: boolean
  onPick: (coordinates: [number, number]) => void
}

export default function LocationPicker({ enabled, onPick }: LocationPickerProps) {
  const map = useMap()
  const [hoverPosition, setHoverPosition] = useState<L.LatLng | null>(null)

  useMapEvents({
    mousemove: (e) => {
      if (enabled) {
        setHoverPosition(e.latlng)
      }
    },
    mouseout: () => {
      setHoverPosition(null)
    },
    click: (e) => {
      if (!enabled) return
      
      const { lat, lng } = e.latlng.wrap()
      onPick([lat, lng])
      
      setHoverPosition(null)
    },
  })

  useEffect(() => {
    const container = map.getContainer()
    container.style.cursor = enabled ? 'crosshair' : ''
    
    return () => {
      container.style.cursor = ''
    }
  }, [map, enabled])

  if (!enabled || !hoverPosition) return null

  return (
    <Marker 
      position={hoverPosition} 
      icon={ghostIcon} 
      interactive={false} 
    />
  )
}