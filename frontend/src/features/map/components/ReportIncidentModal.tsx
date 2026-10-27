import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertCircle, MapPin } from 'lucide-react'
import { useCreateAccident } from '@/queries/accidents/useCreateAccident'
import { CATEGORY_LABELS, SEVERITY_LABELS } from '@/features/map/incident-labels'
import type { IncidentCategory, IncidentSeverity } from '@/types'
import { getErrorMessage } from '@/api/error'

const ReportIncidentError = {
  statusMessages: {
    422: 'Please check your details: title 5-200 characters, description up to 2000 characters.',
    429: 'You have reached the hourly reporting limit. Please try again later.',
  },
  defaultMessage: 'Failed to submit the report. Please try again.'
}

interface ReportIncidentModalProps {
  coordinates: [number, number] | null
  onClose: () => void
}

export default function ReportIncidentModal({ coordinates, onClose }: ReportIncidentModalProps) {
  const createMutation = useCreateAccident()

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState<IncidentCategory>('other')
  const [severity, setSeverity] = useState<IncidentSeverity>('medium')

  const resetForm = () => {
    setTitle('')
    setDescription('')
    setCategory('other')
    setSeverity('medium')
    createMutation.reset()
  }

  const handleClose = () => {
    resetForm()
    onClose()
  }

  const handleSubmit = (e: React.SubmitEvent) => {
    e.preventDefault()
    if (!coordinates) return

    createMutation.mutate(
      {
        title: title.trim(),
        description: description.trim() || null,
        category,
        severity,
        coordinates,
      },
      {
        onSuccess: handleClose
      }
    )
  }

  return (
    <Dialog open={coordinates !== null} onOpenChange={(isOpen) => !isOpen && handleClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold tracking-tight">Report an incident</DialogTitle>
          <DialogDescription>
            Your report will be visible to everyone once an administrator approves it.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {coordinates && (
            <div className="flex items-center gap-2 rounded-md border border-slate-200 bg-slate-50 p-2 text-xs text-slate-600">
              <MapPin className="h-4 w-4 shrink-0 text-slate-500" />
              <span>{coordinates[0].toFixed(5)}, {coordinates[1].toFixed(5)}</span>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="report-title">Title</Label>
            <Input
              id="report-title"
              type="text"
              placeholder="Pothole in the right lane"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={createMutation.isPending}
              minLength={5}
              maxLength={200}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="report-description">Description</Label>
            <Textarea
              id="report-description"
              placeholder="What happened and how does it affect traffic?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={createMutation.isPending}
              maxLength={2000}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Category</Label>
              <Select
                items={CATEGORY_LABELS}
                value={category}
                onValueChange={(value) => value && setCategory(value as IncidentCategory)}
                disabled={createMutation.isPending}
              >
                <SelectTrigger className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {(Object.keys(CATEGORY_LABELS) as IncidentCategory[]).map((key) => (
                    <SelectItem key={key} value={key}>
                      {CATEGORY_LABELS[key]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Severity</Label>
              <Select
                items={SEVERITY_LABELS}
                value={severity}
                onValueChange={(value) => value && setSeverity(value as IncidentSeverity)}
                disabled={createMutation.isPending}
              >
                <SelectTrigger className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {(Object.keys(SEVERITY_LABELS) as IncidentSeverity[]).map((key) => (
                    <SelectItem key={key} value={key}>
                      {SEVERITY_LABELS[key]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {createMutation.isError && (
            <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <p>{getErrorMessage(createMutation.error, ReportIncidentError)}</p>
            </div>
          )}

          <Button type="submit" className="w-full" disabled={createMutation.isPending}>
            {createMutation.isPending ? 'Submitting...' : 'Submit report'}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
