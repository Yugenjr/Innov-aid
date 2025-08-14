import { FormEvent, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function SignIn() {
  const { signIn } = useAuth()
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await signIn(email, password)
      nav('/chat')
    } catch (err: any) {
      setError(err.message || 'Sign-in failed')
    }
  }

  return (
    <div className="min-h-[70vh] grid place-items-center">
      <form onSubmit={submit} className="bg-white rounded-xl shadow p-6 w-full max-w-md space-y-4 border">
        <h1 className="text-2xl font-bold text-center">Welcome back</h1>
        {error && <div className="text-rose-600 text-sm">{error}</div>}
        <label className="block">
          <span className="text-sm text-gray-600">Email</span>
          <input type="email" className="mt-1 w-full border rounded px-3 py-2" value={email} onChange={e=>setEmail(e.target.value)} required />
        </label>
        <label className="block">
          <span className="text-sm text-gray-600">Password</span>
          <input type="password" className="mt-1 w-full border rounded px-3 py-2" value={password} onChange={e=>setPassword(e.target.value)} required />
        </label>
        <button type="submit" className="w-full bg-indigo-600 text-white rounded py-2 hover:bg-indigo-700 transition">Sign In</button>
      </form>
    </div>
  )
}

