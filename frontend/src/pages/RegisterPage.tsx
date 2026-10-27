import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'
import { useRegister } from '@/queries/auth/useRegister'
import { getErrorMessage, type ErrorMessageConfig } from '@/api/error'


const RegisterErrors: ErrorMessageConfig = {
  statusMessages: {
    409: 'This email is already registered.',
    422: 'Please check your details: name 2-80 characters, a valid email, password 10-128 characters.',
  },
  defaultMessage: 'Registration failed. Please try again.'
}

export default function RegisterPage() {
  const navigate = useNavigate()
  const registerMutation = useRegister()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleRegister = (e: React.SubmitEvent) => {
    e.preventDefault()

    registerMutation.mutate(
      { name, email, password },
      {
        onSuccess: () => {
          navigate('/login')
        }
      }
    )
  }

  return (
    <div
      className="relative flex h-screen w-screen items-center justify-center bg-cover bg-center bg-no-repeat px-4"
      style={{ backgroundImage: "url('/assets/login-bg.png')" }}
    >
      <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm z-0">
        <div className="relative z-10 flex h-full w-full items-center justify-center px-4">
          <Card className="relative z-10 w-full max-w-md shadow-2xl border-slate-200/50">
            <CardHeader className="space-y-2 text-center">
              <CardTitle className="text-2xl font-bold tracking-tight">Create an account</CardTitle>
              <CardDescription>
                Sign up to report and track incidents
              </CardDescription>
            </CardHeader>
            <CardContent>
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
                    <p>{getErrorMessage(registerMutation.error, RegisterErrors)}</p>
                  </div>
                )}

                <Button type="submit" className="w-full" disabled={registerMutation.isPending}>
                  {registerMutation.isPending ? 'Creating account...' : 'Sign up'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}