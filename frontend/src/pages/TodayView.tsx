import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useTasks } from '../hooks/useTasks'
import TaskCard from '../components/TaskCard'
import TaskForm from '../components/TaskForm'
import client from '../api/client'
import type { Task } from '../types'

interface ClassSlot {
  id: string
  name: string
  course_code: string
  start_time: string
  end_time: string
  location: string
  day_of_week: number
}

export default function TodayView() {
  const { data: tasks, isLoading } = useTasks('today')
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  // Get today's classes
  const todayDow = new Date().getDay() // 0=Sun
  const plannerDow = todayDow === 0 ? 6 : todayDow - 1 // Convert to 0=Mon

  const { data: classSlots } = useQuery<ClassSlot[]>({
    queryKey: ['class-slots'],
    queryFn: async () => {
      const { data } = await client.get('/class-slots')
      return data
    },
  })

  const todayClasses = classSlots?.filter(s => s.day_of_week === plannerDow)
    .sort((a, b) => a.start_time.localeCompare(b.start_time)) || []

  // Filter out classes that have already ended
  const now = new Date()
  const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
  const upcomingClasses = todayClasses.filter(c => c.end_time > currentTime)

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

      {/* Today's Classes (auto-hide after end time) */}
      {upcomingClasses.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xs font-semibold text-text-muted uppercase mb-2">Classes Remaining</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            {upcomingClasses.map((c) => (
              <div key={c.id} className="flex items-center gap-2 bg-[rgba(124,107,240,0.08)] border border-accent/20 rounded-lg px-3 py-2">
                <span className="text-xs font-mono text-accent">{c.start_time}–{c.end_time}</span>
                <span className="text-sm text-text-primary font-medium truncate">{c.name}</span>
                <span className="text-xs text-text-muted ml-auto truncate max-w-[120px]">{c.location}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tasks */}
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
