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
    // Enhanced client-side auth validation
    if (!email || !password) {
      throw new Error('Please enter both email and password')
    }

    // Basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      throw new Error('Please enter a valid email address')
    }

    // Password length validation
    if (password.length < 6) {
      throw new Error('Password must be at least 6 characters long')
    }

    // Simulate API delay for better UX testing
    await new Promise(resolve => setTimeout(resolve, 1000))

    // For demo purposes, accept any valid email/password combination
    // In a real app, this would make an API call to authenticate
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

