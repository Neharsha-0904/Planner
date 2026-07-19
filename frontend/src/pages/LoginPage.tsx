import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../api/client'
import type { LoginRequest, TokenResponse } from '../types'

export default function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await client.post<TokenResponse>('/auth/login', {
        email,
        password,
      } satisfies LoginRequest)
      localStorage.setItem('planner_token', data.access_token)
      navigate('/')
    } catch {
      setError('Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg-app">
      <div className="w-full max-w-sm">
        <div className="bg-bg-card rounded-lg border border-border p-8">
          <h1 className="text-2xl font-bold text-center mb-6 text-text-primary">⚡ Planner</h1>
          {error && (
            <div className="bg-[rgba(239,78,82,0.16)] text-[#F2888A] text-sm px-3 py-2 rounded mb-4">{error}</div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:ring-2 focus:ring-accent focus:border-accent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:ring-2 focus:ring-accent focus:border-accent"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-accent text-white py-2 rounded-md font-medium hover:bg-accent-hover disabled:opacity-50 transition-colors"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
