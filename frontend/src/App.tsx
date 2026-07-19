import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import TodayView from './pages/TodayView'
import BacklogView from './pages/BacklogView'
import DoneView from './pages/DoneView'
import MonthlyView from './pages/MonthlyView'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('planner_token')
  if (!token) return <Navigate to="/login" replace />
  return <Layout>{children}</Layout>
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <TodayView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/monthly"
        element={
          <ProtectedRoute>
            <MonthlyView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/backlog"
        element={
          <ProtectedRoute>
            <BacklogView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/done"
        element={
          <ProtectedRoute>
            <DoneView />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}
