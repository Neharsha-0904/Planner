import { useState } from 'react'
import { useTasks } from '../hooks/useTasks'
import TaskCard from '../components/TaskCard'
import TaskForm from '../components/TaskForm'
import type { Task } from '../types'

export default function TodayView() {
  const { data: tasks, isLoading } = useTasks('today')
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  if (isLoading) {
    return <div className="text-text-muted">Loading today&apos;s tasks...</div>
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Today</h1>
          <p className="text-sm text-text-secondary mt-1">
            {new Date().toLocaleDateString('en-IN', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="bg-accent text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-accent-hover transition-colors"
        >
          + Add Task
        </button>
      </div>

      {tasks && tasks.length > 0 ? (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onEdit={setEditingTask} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-text-muted">
          <p className="text-lg">No tasks for today</p>
          <p className="text-sm mt-1">Add a task or pull one from your backlog</p>
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
