import { useState } from 'react'
import { useTasks } from '../hooks/useTasks'
import TaskCard from '../components/TaskCard'
import TaskForm from '../components/TaskForm'
import { Priority, type Task } from '../types'

export default function BacklogView() {
  const { data: tasks, isLoading } = useTasks('backlog')
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [filterPriority, setFilterPriority] = useState<Priority | ''>('')

  if (isLoading) {
    return <div className="text-text-muted">Loading backlog...</div>
  }

  const filtered = tasks?.filter((t) => {
    if (filterPriority && t.priority !== filterPriority) return false
    return true
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Backlog</h1>
          <p className="text-sm text-text-secondary mt-1">
            {filtered?.length ?? 0} open task(s) — sorted by urgency
          </p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-accent text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-accent-hover transition-colors"
        >
          + Add Task
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-4">
        {(['', Priority.P0, Priority.P1, Priority.P2] as const).map((p) => (
          <button
            key={p}
            onClick={() => setFilterPriority(p)}
            className={`text-xs px-3 py-1.5 rounded-md border transition-colors ${
              filterPriority === p
                ? 'bg-accent text-white border-accent'
                : 'bg-bg-card text-text-secondary border-border hover:bg-bg-card/80'
            }`}
          >
            {p === '' ? 'All' : p.toUpperCase()}
          </button>
        ))}
      </div>

      {filtered && filtered.length > 0 ? (
        <div className="space-y-3">
          {filtered.map((task) => (
            <TaskCard key={task.id} task={task} onEdit={setEditingTask} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-text-muted">
          <p className="text-lg">Backlog is empty</p>
          <p className="text-sm mt-1">Nice work! Nothing piling up.</p>
        </div>
      )}

      {(showForm || editingTask) && (
        <TaskForm
          task={editingTask}
          onClose={() => {
            setShowForm(false)
            setEditingTask(null)
          }}
        />
      )}
    </div>
  )
}
