import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'

export default function RootLayout() {
  return (
    <div className="flex flex-col h-screen w-screen bg-slate-50 overflow-hidden">
      <Navbar />
      <main className="flex-1 relative isolate z-0">
        <Outlet />
      </main>
    </div>
  )
}