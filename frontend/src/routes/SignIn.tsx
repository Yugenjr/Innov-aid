import { FormEvent, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import { useNavigate } from 'react-router-dom'

type ValidationErrors = {
  email?: string
  password?: string
}

export default function SignIn() {
  const { signIn } = useAuth()
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({})
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const validateEmail = (email: string): string | undefined => {
    if (!email) return 'Email is required'
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) return 'Please enter a valid email address'
    return undefined
  }

  const validatePassword = (password: string): string | undefined => {
    if (!password) return 'Password is required'
    if (password.length < 6) return 'Password must be at least 6 characters'
    return undefined
  }

  const validateForm = (): boolean => {
    const errors: ValidationErrors = {}

    const emailError = validateEmail(email)
    const passwordError = validatePassword(password)

    if (emailError) errors.email = emailError
    if (passwordError) errors.password = passwordError

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setValidationErrors({})

    if (!validateForm()) return

    setIsLoading(true)
    try {
      await signIn(email, password)
      nav('/chat')
    } catch (err: any) {
      setError(err.message || 'Sign-in failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-[70vh] grid place-items-center px-4">
      <form onSubmit={submit} className="bg-white rounded-xl shadow-lg p-8 w-full max-w-md space-y-6 border">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Welcome back</h1>
          <p className="mt-2 text-gray-600">Sign in to your account</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center gap-2">
            <span className="text-red-500">⚠️</span>
            <span className="text-red-700 text-sm">{error}</span>
          </div>
        )}

        <div className="space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-gray-700">Email address</span>
            <input
              type="email"
              className={`mt-1 w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition ${
                validationErrors.email ? 'border-red-300 bg-red-50' : 'border-gray-300'
              }`}
              value={email}
              onChange={e => {
                setEmail(e.target.value)
                if (validationErrors.email) {
                  setValidationErrors(prev => ({ ...prev, email: undefined }))
                }
              }}
              placeholder="Enter your email"
              disabled={isLoading}
            />
            {validationErrors.email && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
            )}
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700">Password</span>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                className={`mt-1 w-full border rounded-lg px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition ${
                  validationErrors.password ? 'border-red-300 bg-red-50' : 'border-gray-300'
                }`}
                value={password}
                onChange={e => {
                  setPassword(e.target.value)
                  if (validationErrors.password) {
                    setValidationErrors(prev => ({ ...prev, password: undefined }))
                  }
                }}
                placeholder="Enter your password"
                disabled={isLoading}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isLoading}
              >
                <span className="text-gray-400 hover:text-gray-600">
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </span>
              </button>
            </div>
            {validationErrors.password && (
              <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
            )}
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-indigo-600 text-white rounded-lg py-3 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Signing in...
            </div>
          ) : (
            'Sign In'
          )}
        </button>
      </form>
    </div>
  )
}

