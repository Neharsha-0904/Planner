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

      {/* Skill Map Diagram */}
      <div className="bg-bg-card border border-border rounded-lg p-4 mb-6">
        <h2 className="text-sm font-semibold text-text-secondary uppercase mb-3">Skill Dependency Map</h2>
        <div className="overflow-x-auto">
          <SkillMap done={done.map(m => m.title)} />
        </div>
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

// ─── Skill Map Visual ───────────────────────────────────────────────────────

interface SkillNode {
  id: string
  label: string
  x: number
  y: number
  status: 'done' | 'active' | 'upcoming'
}

interface SkillEdge {
  from: string
  to: string
}

const nodes: SkillNode[] = [
  // Row 1: Foundations
  { id: 'python', label: 'Python Deep', x: 80, y: 40, status: 'active' },
  { id: 'math', label: '3B1B Math', x: 250, y: 40, status: 'active' },
  { id: 'dsa', label: 'DSA/LeetCode', x: 420, y: 40, status: 'active' },
  // Row 2: ML Core
  { id: 'andrew_ml', label: 'Andrew Ng ML', x: 80, y: 120, status: 'upcoming' },
  { id: 'andrew_dl', label: 'Deep Learning', x: 250, y: 120, status: 'upcoming' },
  { id: 'karpathy', label: 'Karpathy ZtH', x: 420, y: 120, status: 'upcoming' },
  // Row 3: Advanced
  { id: 'mlops', label: 'MLOps Spec', x: 80, y: 200, status: 'upcoming' },
  { id: 'hf_nlp', label: 'HuggingFace NLP', x: 250, y: 200, status: 'upcoming' },
  { id: 'chip', label: 'Chip Huyen Book', x: 420, y: 200, status: 'upcoming' },
  // Row 4: Certs
  { id: 'aws_aip', label: 'AWS AI Pract ✓', x: 580, y: 40, status: 'done' },
  { id: 'ai102', label: 'MS AI-102 ✓', x: 580, y: 90, status: 'done' },
  { id: 'claude', label: 'Claude Arch ✓', x: 580, y: 140, status: 'done' },
  { id: 'aws_ml', label: 'AWS ML Eng', x: 580, y: 200, status: 'upcoming' },
  { id: 'aws_saa', label: 'AWS SAA', x: 580, y: 250, status: 'upcoming' },
  // Row 5: Projects
  { id: 'p1', label: 'Fraud Detection', x: 160, y: 290, status: 'upcoming' },
  { id: 'p2', label: 'Multi-Agent RAG', x: 360, y: 290, status: 'upcoming' },
  { id: 'portfolio', label: 'Portfolio Site', x: 560, y: 340, status: 'upcoming' },
  // Goal
  { id: 'goal', label: '🎯 ML Engineer', x: 330, y: 380, status: 'upcoming' },
]

const edges: SkillEdge[] = [
  { from: 'python', to: 'andrew_ml' },
  { from: 'math', to: 'andrew_ml' },
  { from: 'math', to: 'karpathy' },
  { from: 'andrew_ml', to: 'andrew_dl' },
  { from: 'andrew_dl', to: 'karpathy' },
  { from: 'andrew_dl', to: 'mlops' },
  { from: 'karpathy', to: 'hf_nlp' },
  { from: 'mlops', to: 'p1' },
  { from: 'andrew_ml', to: 'p1' },
  { from: 'hf_nlp', to: 'p2' },
  { from: 'karpathy', to: 'p2' },
  { from: 'p1', to: 'p2' },
  { from: 'mlops', to: 'aws_ml' },
  { from: 'aws_ml', to: 'aws_saa' },
  { from: 'p2', to: 'portfolio' },
  { from: 'p1', to: 'goal' },
  { from: 'p2', to: 'goal' },
  { from: 'aws_saa', to: 'goal' },
  { from: 'dsa', to: 'goal' },
  { from: 'chip', to: 'goal' },
  { from: 'portfolio', to: 'goal' },
]

function SkillMap({ done }: { done: string[] }) {
  const getStatus = (node: SkillNode): 'done' | 'active' | 'upcoming' => {
    if (node.status === 'done') return 'done'
    if (done.some(d => node.label.toLowerCase().includes(d.toLowerCase().slice(0, 8)))) return 'done'
    return node.status
  }

  const colors = {
    done: { fill: '#34D399', stroke: '#059669', text: '#000' },
    active: { fill: '#7C6BF0', stroke: '#5B4BD4', text: '#fff' },
    upcoming: { fill: '#1A2130', stroke: '#2A3346', text: '#E7EAF0' },
  }

  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]))

  return (
    <svg viewBox="0 0 700 420" className="w-full h-auto min-h-[300px]">
      {/* Edges */}
      {edges.map((e, i) => {
        const from = nodeMap[e.from]
        const to = nodeMap[e.to]
        if (!from || !to) return null
        return (
          <line
            key={i}
            x1={from.x}
            y1={from.y + 12}
            x2={to.x}
            y2={to.y - 12}
            stroke="#2A3346"
            strokeWidth="1"
            opacity="0.6"
          />
        )
      })}
      {/* Nodes */}
      {nodes.map(node => {
        const status = getStatus(node)
        const c = colors[status]
        return (
          <g key={node.id}>
            <rect
              x={node.x - 55}
              y={node.y - 14}
              width={110}
              height={28}
              rx={6}
              fill={c.fill}
              stroke={c.stroke}
              strokeWidth={1.5}
            />
            <text
              x={node.x}
              y={node.y + 4}
              textAnchor="middle"
              fill={c.text}
              fontSize="9"
              fontWeight="500"
            >
              {node.label}
            </text>
          </g>
        )
      })}
    </svg>
  )
}
