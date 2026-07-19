import { useQuery } from '@tanstack/react-query'
import client from '../api/client'

interface Milestone {
  id: string
  title: string
  category: string
  status: string
  target_date: string | null
  exam_date: string | null
  progress_pct: number
}

const statusColors: Record<string, string> = {
  done: 'bg-status-done/20 text-status-done border-status-done/30',
  in_progress: 'bg-accent/20 text-accent border-accent/30',
  not_started: 'bg-[rgba(107,116,134,0.16)] text-text-muted border-border',
}

const statusLabels: Record<string, string> = {
  done: '✓ Done',
  in_progress: 'In Progress',
  not_started: 'Not Started',
}

const categoryIcons: Record<string, string> = {
  certification: '🏅',
  course: '📚',
  project: '🚀',
}

export default function RoadmapView() {
  const { data: milestones, isLoading } = useQuery<Milestone[]>({
    queryKey: ['milestones'],
    queryFn: async () => {
      const { data } = await client.get('/milestones')
      return data
    },
  })

  if (isLoading) return <div className="text-text-muted">Loading roadmap...</div>

  const done = milestones?.filter(m => m.status === 'done') || []
  const inProgress = milestones?.filter(m => m.status === 'in_progress') || []
  const notStarted = milestones?.filter(m => m.status === 'not_started') || []

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Roadmap</h1>
        <p className="text-sm text-text-secondary mt-1">
          {done.length} completed • {inProgress.length} in progress • {notStarted.length} upcoming
        </p>
      </div>

      {/* Progress bar */}
      <div className="bg-bg-card border border-border rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-text-secondary">Overall Progress</span>
          <span className="text-sm font-medium text-text-primary">
            {milestones ? Math.round((done.length / milestones.length) * 100) : 0}%
          </span>
        </div>
        <div className="w-full h-2 bg-border rounded-full overflow-hidden">
          <div
            className="h-full bg-accent rounded-full transition-all"
            style={{ width: milestones ? `${(done.length / milestones.length) * 100}%` : '0%' }}
          />
        </div>
      </div>

      {/* Completed */}
      {done.length > 0 && (
        <Section title="Completed" milestones={done} />
      )}

      {/* In Progress */}
      {inProgress.length > 0 && (
        <Section title="In Progress" milestones={inProgress} />
      )}

      {/* Not Started */}
      {notStarted.length > 0 && (
        <Section title="Upcoming" milestones={notStarted} />
      )}
    </div>
  )
}

function Section({ title, milestones }: { title: string; milestones: Milestone[] }) {
  return (
    <div className="mb-6">
      <h2 className="text-sm font-semibold text-text-secondary uppercase mb-3">{title}</h2>
      <div className="space-y-2">
        {milestones.map(m => (
          <div key={m.id} className="bg-bg-card border border-border rounded-lg p-3 flex items-center gap-3">
            <span className="text-lg">{categoryIcons[m.category] || '📌'}</span>
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium text-text-primary truncate">{m.title}</h3>
              <div className="flex items-center gap-2 mt-0.5">
                {m.target_date && (
                  <span className="text-xs text-text-muted">Target: {m.target_date}</span>
                )}
                {m.exam_date && (
                  <span className="text-xs text-priority-p0">Exam: {m.exam_date}</span>
                )}
              </div>
            </div>
            <span className={`text-xs px-2 py-0.5 rounded border ${statusColors[m.status]}`}>
              {statusLabels[m.status]}
            </span>
            {m.status !== 'done' && m.progress_pct > 0 && (
              <div className="w-16 h-1.5 bg-border rounded-full overflow-hidden">
                <div className="h-full bg-accent rounded-full" style={{ width: `${m.progress_pct}%` }} />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
