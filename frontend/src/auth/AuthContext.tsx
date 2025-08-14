import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'

export type User = { email: string }

type AuthContextType = {
  user: User | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem('fc_user')
    if (stored) setUser(JSON.parse(stored))
  }, [])

  const signIn = async (email: string, password: string) => {
    // Simple client-side auth stub; replace with real API later
    if (!email || !password) throw new Error('Enter email and password')
    const u = { email }
    localStorage.setItem('fc_user', JSON.stringify(u))
    setUser(u)
  }

  const signOut = () => {
    localStorage.removeItem('fc_user')
    setUser(null)
  }

  const value = useMemo(() => ({ user, signIn, signOut }), [user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

