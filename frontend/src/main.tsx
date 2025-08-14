import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import RootLayout from './routes/RootLayout'
import Landing from './routes/Landing'
import SignIn from './routes/SignIn'
import Chatbot from './routes/Chatbot'
import Budget from './routes/Budget'
import Savings from './routes/Savings'
import Investment from './routes/Investment'
import FraudDetection from './routes/FraudDetection'
import { AuthProvider, useAuth } from './auth/AuthContext'

function ProtectedRoute({ element }: { element: JSX.Element }) {
  const { user } = useAuth()
  return user ? element : <Landing />
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <Landing /> },
      { path: 'signin', element: <SignIn /> },
      { path: 'chat', element: <ProtectedRoute element={<Chatbot />} /> },
      { path: 'budget', element: <Budget /> },
      { path: 'savings', element: <Savings /> },
      { path: 'investment', element: <Investment /> },
      { path: 'fraud-detection', element: <FraudDetection /> },
    ],
  },
])

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>
)

