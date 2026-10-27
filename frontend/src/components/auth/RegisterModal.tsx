import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { isAxiosError } from 'axios'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertCircle } from 'lucide-react'
import { useRegister } from '@/queries/auth/useRegister'

interface RegisterModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const getErrorMessage = (error: unknown) => {
  if (isAxiosError(error)) {
    if (error.response?.status === 409) {
      return 'This email is already registered.'
    }
    if (error.response?.status === 422) {
      return 'Please check your details: name 2-80 characters, a valid email, password 10-128 characters.'
    }
  }
  return 'Registration failed. Please try again.'
}

export default function RegisterModal({ open, onOpenChange }: RegisterModalProps) {
  const navigate = useNavigate()
  const registerMutation = useRegister()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const resetForm = () => {
    setName('')
    setEmail('')
    setPassword('')
    registerMutation.reset()
  }

  const handleOpenChange = (isOpen: boolean) => {
    if (!isOpen) resetForm()
    onOpenChange(isOpen)
  }

  const handleRegister = (e: React.SubmitEvent) => {
    e.preventDefault()

    registerMutation.mutate(
      { name, email, password },
      {
        onSuccess: () => {
          handleOpenChange(false)
          navigate('/login')
        }
      }
    )
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader className="text-center">
          <DialogTitle className="text-2xl font-bold tracking-tight">Create an account</DialogTitle>
          <DialogDescription>
            Sign up to report and track incidents
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="register-name">Name</Label>
            <Input
              id="register-name"
              type="text"
              placeholder="Selim"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={registerMutation.isPending}
              minLength={2}
              maxLength={80}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="register-email">Email</Label>
            <Input
              id="register-email"
              type="email"
              placeholder="selim@student.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={registerMutation.isPending}
              maxLength={200}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="register-password">Password</Label>
            <Input
              id="register-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={registerMutation.isPending}
              minLength={10}
              maxLength={128}
              autoComplete="new-password"
              required
            />
            <p className="text-xs text-slate-500">At least 10 characters.</p>
          </div>

          {registerMutation.isError && (
            <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <p>{getErrorMessage(registerMutation.error)}</p>
            </div>
          )}

          <Button type="submit" className="w-full" disabled={registerMutation.isPending}>
            {registerMutation.isPending ? 'Creating account...' : 'Sign up'}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
