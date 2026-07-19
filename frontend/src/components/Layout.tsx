import { NavLink, useNavigate } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Today', icon: '📅' },
  { to: '/monthly', label: 'Monthly', icon: '🗓️' },
  { to: '/roadmap', label: 'Roadmap', icon: '🗺️' },
  { to: '/backlog', label: 'Backlog', icon: '📋' },
  { to: '/done', label: 'Done', icon: '✅' },
  { to: '#', label: 'Finance', icon: '💰', disabled: true },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('planner_token')
    navigate('/login')
  }

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-56 bg-bg-sidebar text-text-primary flex flex-col">
        <div className="p-4 border-b border-border">
          <h1 className="text-lg font-bold">⚡ Planner</h1>
        </div>
        <nav className="flex-1 py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.label}
              to={item.disabled ? '#' : item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 text-sm transition-colors ${
                  item.disabled
                    ? 'text-text-muted cursor-not-allowed'
                    : isActive
                    ? 'bg-accent/10 text-accent'
                    : 'text-text-secondary hover:bg-accent/5 hover:text-text-primary'
                }`
              }
              onClick={(e) => item.disabled && e.preventDefault()}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
              {item.disabled && (
                <span className="ml-auto text-xs bg-[rgba(107,116,134,0.16)] text-text-muted px-1.5 py-0.5 rounded">Soon</span>
              )}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-border">
          <button
            onClick={handleLogout}
            className="text-sm text-text-muted hover:text-text-primary transition-colors"
          >
            Logout
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-y-auto bg-bg-app p-6">{children}</main>
    </div>
  )
}
