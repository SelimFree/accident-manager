import { Link } from 'react-router-dom'
import { Button, buttonVariants } from '@/components/ui/button'
import { ServerCrash } from 'lucide-react'

export default function ServerErrorPage() {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center space-y-4 bg-slate-50 px-4 text-center">
      <div className="rounded-full bg-red-100 p-4">
        <ServerCrash className="h-12 w-12 text-red-600" />
      </div>
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">System Offline</h1>
        <p className="text-slate-500 max-w-md mx-auto">
          Our servers are currently experiencing issues. We are working to restore the service as quickly as possible.
        </p>
      </div>
      <div className="flex gap-4">
        <Button onClick={() => window.location.reload()} variant="outline">
          Try Again
        </Button>
        <Link to="/" className={buttonVariants({ variant: 'default' })}>
          Return Home
        </Link>
      </div>
    </div>
  )
}