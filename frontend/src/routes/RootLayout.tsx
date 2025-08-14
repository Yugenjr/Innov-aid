import { Outlet, Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function RootLayout() {
  const linkClass = ({isActive}:{isActive:boolean}) => isActive ? 'font-semibold underline' : 'hover:opacity-90'
  const { user, signOut } = useAuth()
  const nav = useNavigate()
  const onSignOut = () => { signOut(); nav('/') }
  return (
    <div className="min-h-screen flex flex-col relative">
      {/* decorative gradient glows */}
      <div className="pointer-events-none absolute -z-10 top-24 left-10 w-72 h-72 bg-purple-300/40 blur-3xl rounded-full" />
      <div className="pointer-events-none absolute -z-10 bottom-24 right-10 w-72 h-72 bg-indigo-300/40 blur-3xl rounded-full" />
      <header className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white sticky top-0 z-20">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="font-extrabold text-xl tracking-tight">🏦 Finance App</Link>
          <nav className="flex items-center gap-4">
            <NavLink to="/" className={linkClass}>Home</NavLink>
            <NavLink to="/chat" className={linkClass}>Chatbot</NavLink>
            <NavLink to="/fraud-detection" className={linkClass}>🔒 Fraud Detection</NavLink>
            <NavLink to="/budget" className={linkClass}>Budget</NavLink>
            <NavLink to="/savings" className={linkClass}>Savings</NavLink>
            <NavLink to="/investment" className={linkClass}>Investment</NavLink>
            {!user ? (
              <NavLink to="/signin" className="ml-4 px-3 py-1.5 rounded bg-white/10 hover:bg-white/20">Sign In</NavLink>
            ) : (
              <button onClick={onSignOut} className="ml-4 px-3 py-1.5 rounded bg-white/10 hover:bg-white/20">Sign Out</button>
            )}
          </nav>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6 flex-1">
        <Outlet />
      </main>
      <footer className="border-t py-4 text-center text-sm text-gray-500 bg-white/60 backdrop-blur">
        © {new Date().getFullYear()} Finance Chatbot
      </footer>
    </div>
  )
}

