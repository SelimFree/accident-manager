import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'
import { useLogin } from '@/queries/auth/useLogin'

export default function LoginPage() {
  const navigate = useNavigate()
  const loginMutation = useLogin()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = (e: React.SubmitEvent) => {
    e.preventDefault()

    loginMutation.mutate(
      { email, password },
      {
        onSuccess: (data) => {
          if (data.user.role === 'admin') {
            navigate('/admin')
          } else {
            navigate('/')
          }
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
              <CardTitle className="text-2xl font-bold tracking-tight">Welcome back</CardTitle>
              <CardDescription>
                Sign in to your Accident Manager account
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLogin} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="selim@student.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={loginMutation.isPending}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={loginMutation.isPending}
                    required
                  />
                </div>

                {loginMutation.isError && (
                  <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                    <AlertCircle className="h-4 w-4 shrink-0" />
                    <p>Invalid email or password. Please try again.</p>
                  </div>
                )}

                <Button type="submit" className="w-full" disabled={loginMutation.isPending}>
                  {loginMutation.isPending ? 'Signing in...' : 'Sign in'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

      </div>
    </div>

  )
}