import { createBrowserRouter } from 'react-router-dom'
import MapPage from '@/pages/MapPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MapPage />,
  },
  {
    path: '/admin',
    element: <div>Admin Layout Placeholder</div>,
    children: [
      {
        index: true,
        element: <div>Admin Dashboard</div>,
      },
    ],
  },
])