import { lazy, Suspense } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import RootLayout from '@/components/layout/RootLayout'
import PageLoader from '@/components/layout/PageLoader'
import GlobalCrashPage from '@/components/layout/GlobalCrashPage'

const NotFoundPage = lazy(() => import('@/pages/NotFoundPage'))
const ServerErrorPage = lazy(() => import('@/pages/ServerErrorPage'))
const MapPage = lazy(() => import('@/pages/MapPage'))
const LoginPage = lazy(() => import('@/pages/LoginPage'))


const router = createBrowserRouter([
  {
    element: <RootLayout />,
    errorElement: <GlobalCrashPage />,
    children: [
      {
        path: '/',
        element: (
          <Suspense fallback={<PageLoader />}>
            <MapPage />
          </Suspense>
        ),
      },
      {
        path: '/login',
        element: (
          <Suspense fallback={<PageLoader />}>
            <LoginPage />
          </Suspense>
        ),
      },
      {
        path: '/500',
        element: (
          <Suspense fallback={<PageLoader />}>
            <ServerErrorPage />
          </Suspense>
        ),
      },
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: '/report',
            element: <div>Report Incident Form Placeholder</div>,
          },
        ]
      },
      {
        element: <ProtectedRoute requireAdmin={true} />,
        children: [
          {
            path: '/admin',
            element: (
              <Suspense fallback={<PageLoader />}>
                <div>Admin Layout Placeholder</div>
              </Suspense>
            ),
            children: [
              {
                index: true,
                element: <div>Admin Dashboard</div>,
              },
            ],
          },
        ]
      },
      {
        path: '*',
        element: (
          <Suspense fallback={<PageLoader />}>
            <NotFoundPage />
          </Suspense>
        ),
      },
    ],
  }
])

export default function AppRouter() {
  return <RouterProvider router={router} />
}