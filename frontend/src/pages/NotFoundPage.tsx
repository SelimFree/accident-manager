import { Link } from 'react-router-dom'
import { buttonVariants } from '@/components/ui/button'
import { MapPinOff } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center space-y-4 bg-slate-50 px-4 text-center">
      <div className="rounded-full bg-slate-100 p-4">
        <MapPinOff className="h-12 w-12 text-slate-400" />
      </div>
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">404 - Page Not Found</h1>
        <p className="text-slate-500 max-w-md mx-auto">
          We can't seem to find the page you're looking for. It might have been moved or the URL is incorrect.
        </p>
      </div>
      <Link to="/" className={buttonVariants({ variant: 'default' })}>
        Return to Map
      </Link>
    </div>
  )
}