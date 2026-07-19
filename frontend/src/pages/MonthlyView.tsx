import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { Task } from '../types'
import PriorityBadge from '../components/PriorityBadge'

interface ClassSlot {
  id: string
  name: string
  course_code: string
  day_of_week: number
  start_time: string
  end_time: string
  location: string
}

function getDaysInMonth(year: number, month: number) {
  return new Date(year, month + 1, 0).getDate()
}

function getFirstDayOfWeek(year: number, month: number) {
  return new Date(year, month, 1).getDay() // 0=Sun
}

function formatDate(year: number, month: number, day: number) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
}

export default function MonthlyView() {
  const today = new Date()
  const [year, setYear] = useState(today.getFullYear())
  const [month, setMonth] = useState(today.getMonth())
  const [selectedDate, setSelectedDate] = useState<string | null>(formatDate(today.getFullYear(), today.getMonth(), today.getDate()))

  const { data: allTasks } = useQuery<Task[]>({
    queryKey: ['tasks', 'all-for-month', year, month],
    queryFn: async () => {
      const { data } = await client.get('/tasks?view=all')
      return data
    },
  })

  const { data: classSlots } = useQuery<ClassSlot[]>({
    queryKey: ['class-slots'],
    queryFn: async () => {
      const { data } = await client.get('/class-slots')
      return data
    },
  })

  const daysInMonth = getDaysInMonth(year, month)
  const firstDay = getFirstDayOfWeek(year, month)
  const monthName = new Date(year, month).toLocaleString('en-IN', { month: 'long', year: 'numeric' })

  const prevMonth = () => {
    if (month === 0) { setYear(year - 1); setMonth(11) }
    else setMonth(month - 1)
  }
  const nextMonth = () => {
    if (month === 11) { setYear(year + 1); setMonth(0) }
    else setMonth(month + 1)
  }

  // Group tasks by date
  const tasksByDate: Record<string, Task[]> = {}
  allTasks?.forEach(t => {
    const d = t.scheduled_for
    if (d) {
      if (!tasksByDate[d]) tasksByDate[d] = []
      tasksByDate[d].push(t)
    }
  })

  // Get classes for selected date's day of week
  const selectedDayOfWeek = selectedDate ? new Date(selectedDate).getDay() : -1
  // Convert JS day (0=Sun) to our format (0=Mon)
  const plannerDow = selectedDayOfWeek === 0 ? 6 : selectedDayOfWeek - 1
  const selectedClasses = classSlots?.filter(s => s.day_of_week === plannerDow) || []
  const selectedTasks = selectedDate ? (tasksByDate[selectedDate] || []) : []

  const todayStr = formatDate(today.getFullYear(), today.getMonth(), today.getDate())

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Monthly Schedule</h1>
      </div>

      {/* Month navigation */}
      <div className="flex items-center justify-between mb-4 bg-bg-card rounded-lg border border-border p-3">
        <button onClick={prevMonth} className="text-text-secondary hover:text-text-primary px-3 py-1 rounded hover:bg-accent/10">←</button>
        <span className="text-lg font-semibold text-text-primary">{monthName}</span>
        <button onClick={nextMonth} className="text-text-secondary hover:text-text-primary px-3 py-1 rounded hover:bg-accent/10">→</button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Calendar grid */}
        <div className="lg:col-span-2 bg-bg-card rounded-lg border border-border p-4">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(d => (
              <div key={d} className="text-center text-xs font-medium text-text-muted py-1">{d}</div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-1">
            {/* Empty cells for offset (adjust for Mon start) */}
            {Array.from({ length: firstDay === 0 ? 6 : firstDay - 1 }).map((_, i) => (
              <div key={`empty-${i}`} className="h-16" />
            ))}
            {/* Day cells */}
            {Array.from({ length: daysInMonth }).map((_, i) => {
              const day = i + 1
              const dateStr = formatDate(year, month, day)
              const isToday = dateStr === todayStr
              const isSelected = dateStr === selectedDate
              const dayTasks = tasksByDate[dateStr] || []
              const hasTasks = dayTasks.length > 0
              const hasP0 = dayTasks.some(t => t.priority === 'p0')
              const hasP1 = dayTasks.some(t => t.priority === 'p1')

              return (
                <button
                  key={day}
                  onClick={() => setSelectedDate(dateStr)}
                  className={`h-16 rounded-md border text-left p-1 transition-colors flex flex-col ${
                    isSelected
                      ? 'border-accent bg-accent/10'
                      : isToday
                      ? 'border-accent/50 bg-accent/5'
                      : 'border-border hover:border-accent/30 hover:bg-bg-card/80'
                  }`}
                >
                  <span className={`text-xs font-medium ${isToday ? 'text-accent' : 'text-text-primary'}`}>
                    {day}
                  </span>
                  {hasTasks && (
                    <div className="flex gap-0.5 mt-auto">
                      {hasP0 && <span className="w-1.5 h-1.5 rounded-full bg-priority-p0" />}
                      {hasP1 && <span className="w-1.5 h-1.5 rounded-full bg-priority-p1" />}
                      <span className="text-[9px] text-text-muted ml-auto">{dayTasks.length}</span>
                    </div>
                  )}
                </button>
              )
            })}
          </div>
        </div>

        {/* Day detail panel */}
        <div className="bg-bg-card rounded-lg border border-border p-4 overflow-y-auto max-h-[600px]">
          {selectedDate ? (
            <>
              <h3 className="text-sm font-semibold text-text-primary mb-3">
                {new Date(selectedDate + 'T00:00').toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short' })}
              </h3>

              {/* Classes */}
              {selectedClasses.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-xs font-medium text-text-muted uppercase mb-2">Classes</h4>
                  <div className="space-y-1.5">
                    {selectedClasses.sort((a, b) => a.start_time.localeCompare(b.start_time)).map(c => (
                      <div key={c.id} className="flex items-center gap-2 text-xs bg-[rgba(124,107,240,0.08)] rounded px-2 py-1.5">
                        <span className="text-accent font-mono">{c.start_time}–{c.end_time}</span>
                        <span className="text-text-primary font-medium">{c.name}</span>
                        <span className="text-text-muted ml-auto truncate max-w-[100px]">{c.location}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tasks */}
              {selectedTasks.length > 0 ? (
                <div>
                  <h4 className="text-xs font-medium text-text-muted uppercase mb-2">Tasks ({selectedTasks.length})</h4>
                  <div className="space-y-2">
                    {selectedTasks.map(t => (
                      <div key={t.id} className="flex items-start gap-2 text-xs border border-border rounded px-2 py-1.5">
                        <PriorityBadge priority={t.priority} />
                        <span className="text-text-primary flex-1">{t.title}</span>
                        {t.estimated_minutes && (
                          <span className="text-text-muted">{t.estimated_minutes}m</span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="text-xs text-text-muted">No tasks scheduled for this day.</p>
              )}
            </>
          ) : (
            <p className="text-sm text-text-muted">Click a date to see the schedule.</p>
          )}
        </div>
      </div>
    </div>
  )
}
