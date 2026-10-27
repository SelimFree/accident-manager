import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { Button, buttonVariants } from '@/components/ui/button'
import RegisterModal from '@/components/auth/RegisterModal'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { LogOut, ShieldAlert, HomeIcon } from 'lucide-react'
import RoleGuard from '@/guards/RoleGuard'
import { useQueryClient } from '@tanstack/react-query'
import { accidentKeys } from '@/queries/accidents/accidentKeys'

export default function Navbar() {
    const queryClient = useQueryClient()
    const navigate = useNavigate()
    const logout = useAuthStore((state) => state.logout)
    const user = useAuthStore((state) => state.user)
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
    const [isRegisterOpen, setIsRegisterOpen] = useState(false)

    const handleLogout = () => {
        logout()
        queryClient.removeQueries({ queryKey: [...accidentKeys.all, 'mine'] })
        queryClient.removeQueries({ queryKey: [...accidentKeys.all, 'adminQueue'] })
        queryClient.invalidateQueries({ queryKey: accidentKeys.lists() })
        navigate('/')
    }

    const initials = user?.name ? user.name.substring(0, 2).toUpperCase() : 'UP'

    return (
        <header className="h-14 border-b bg-white px-4 flex items-center justify-between shadow-xs sticky top-0 z-40 shrink-0">
            <div className="flex items-center gap-2">
                <Link to="/" className="flex items-center gap-2 hover:opacity-90 transition-opacity">
                    <img
                        src="/android-chrome-512x512.png"
                        alt="Accident Manager Logo"
                        className="h-8 w-8 rounded-md object-contain shadow-sm border border-slate-200"
                    />
                    <h1 className="font-bold text-base text-slate-800">Accident Manager</h1>
                </Link>
            </div>

            <div className="flex items-center gap-4">
                {!isAuthenticated ? (
                    <>
                        <Link to="/login" className={buttonVariants({ variant: "ghost" })}>
                            Log in
                        </Link>
                        <Button onClick={() => setIsRegisterOpen(true)}>
                            Sign up
                        </Button>
                        <RegisterModal open={isRegisterOpen} onOpenChange={setIsRegisterOpen} />
                    </>
                ) : (
                    <DropdownMenu>
                        <DropdownMenuTrigger className="rounded-full outline-none focus-visible:ring-2 focus-visible:ring-slate-400">
                            <Avatar className="h-8 w-8 hover:opacity-80 transition-opacity">
                                <AvatarFallback className="bg-slate-800 text-white text-xs">
                                    {initials}
                                </AvatarFallback>
                            </Avatar>
                        </DropdownMenuTrigger>

                        <DropdownMenuContent className="w-56 z-2000" align="end">
                            <DropdownMenuGroup>
                                <DropdownMenuLabel className="font-normal">
                                    <div className="flex flex-col space-y-1">
                                        <p className="text-sm font-medium leading-none">{user?.name}</p>
                                        <p className="text-xs leading-none text-slate-500">{user?.email}</p>
                                    </div>
                                </DropdownMenuLabel>
                            </DropdownMenuGroup>

                            <DropdownMenuSeparator />

                            <DropdownMenuItem onClick={() => navigate('/')} className="cursor-pointer">
                                <HomeIcon className="mr-2 h-4 w-4" />
                                <span>Home</span>
                            </DropdownMenuItem>

                            <DropdownMenuSeparator />

                            <RoleGuard allowedRoles="admin">
                                <DropdownMenuItem onClick={() => navigate('/admin')} className="cursor-pointer">
                                    <ShieldAlert className="mr-2 h-4 w-4" />
                                    <span>Admin Dashboard</span>
                                </DropdownMenuItem>
                                <DropdownMenuSeparator />
                            </RoleGuard>

                            <DropdownMenuItem onClick={handleLogout} className="text-red-600 cursor-pointer">
                                <LogOut className="mr-2 h-4 w-4" />
                                <span>Log out</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                )}
            </div>
        </header>
    )
}