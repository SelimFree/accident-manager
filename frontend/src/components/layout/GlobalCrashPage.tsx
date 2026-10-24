import { useState } from 'react'
import { useRouteError, isRouteErrorResponse } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { AlertTriangle, Copy, CheckCircle2 } from 'lucide-react'

export default function GlobalCrashPage() {
  const error = useRouteError()
  const [showDetails, setShowDetails] = useState(false)
  const [copied, setCopied] = useState(false)

  let errorMessage = 'An unexpected error occurred.'
  let errorStack = ''

  if (isRouteErrorResponse(error)) {
    errorMessage = `${error.status} ${error.statusText}`
    errorStack = error.data
  } else if (error instanceof Error) {
    errorMessage = error.message
    errorStack = error.stack || ''
  }

  const handleCopy = () => {
    const debugInfo = `Error: ${errorMessage}\n\nStack:\n${errorStack}`
    navigator.clipboard.writeText(debugInfo)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleReload = () => {
    window.location.assign('/')
  }

  return (
    <div className="flex min-h-screen w-screen flex-col items-center justify-center bg-slate-50 px-4 py-12">
      <div className="w-full max-w-2xl space-y-6">
        <div className="flex flex-col items-center text-center space-y-4">
          <div className="rounded-full bg-red-100 p-4">
            <AlertTriangle className="h-12 w-12 text-red-600" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Something went wrong
          </h1>
          <p className="text-slate-500">
            The application crashed unexpectedly. We apologize for the inconvenience.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Button onClick={handleReload} size="lg">
            Reload Application
          </Button>
        </div>

        <div className="pt-8">
          <Button 
            variant="ghost" 
            onClick={() => setShowDetails(!showDetails)}
            className="w-full text-slate-500"
          >
            {showDetails ? 'Hide technical details' : 'Show technical details'}
          </Button>

          {showDetails && (
            <div className="mt-4 overflow-hidden rounded-md border border-slate-200 bg-slate-900">
              <div className="flex items-center justify-between border-b border-slate-800 bg-slate-950 px-4 py-2">
                <span className="text-xs font-mono text-slate-400">Error Stack Trace</span>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="h-8 px-2 text-slate-400 hover:text-white"
                  onClick={handleCopy}
                >
                  {copied ? (
                    <CheckCircle2 className="mr-1 h-4 w-4 text-green-400" />
                  ) : (
                    <Copy className="mr-1 h-4 w-4" />
                  )}
                  {copied ? 'Copied' : 'Copy'}
                </Button>
              </div>
              <div className="p-4 overflow-x-auto">
                <pre className="text-xs font-mono text-red-400">
                  {errorMessage}
                  {'\n\n'}
                  {errorStack}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}