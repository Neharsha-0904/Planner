import { useState } from 'react'
import { useCreateTask, useUpdateTask } from '../hooks/useTasks'
import { Priority, type Task, type TaskCreate } from '../types'

interface TaskFormProps {
  task?: Task | null
  onClose: () => void
}

export default function TaskForm({ task, onClose }: TaskFormProps) {
  const isEdit = !!task
  const createMutation = useCreateTask()
  const updateMutation = useUpdateTask()

  const [title, setTitle] = useState(task?.title ?? '')
  const [description, setDescription] = useState(task?.description ?? '')
  const [priority, setPriority] = useState<Priority>(task?.priority ?? Priority.P2)
  const [dueDate, setDueDate] = useState(task?.due_date ?? '')
  const [scheduledFor, setScheduledFor] = useState(task?.scheduled_for ?? '')
  const [estimatedMinutes, setEstimatedMinutes] = useState(task?.estimated_minutes?.toString() ?? '')
  const [tags, setTags] = useState(task?.tags?.join(', ') ?? '')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const payload: TaskCreate = {
      title,
      description: description || undefined,
      priority,
      due_date: dueDate || undefined,
      scheduled_for: scheduledFor || undefined,
      estimated_minutes: estimatedMinutes ? parseInt(estimatedMinutes) : undefined,
      tags: tags ? tags.split(',').map((t) => t.trim()).filter(Boolean) : undefined,
    }

    if (isEdit && task) {
      updateMutation.mutate({ id: task.id, ...payload }, { onSuccess: onClose })
    } else {
      createMutation.mutate(payload, { onSuccess: onClose })
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex justify-end z-50">
      <div className="w-full max-w-md bg-bg-sidebar h-full overflow-y-auto shadow-xl border-l border-border">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-text-primary">{isEdit ? 'Edit Task' : 'New Task'}</h2>
            <button onClick={onClose} className="text-text-muted hover:text-text-primary text-xl">
              ✕
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Title *</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:ring-2 focus:ring-accent focus:border-accent"
                placeholder="What needs to be done?"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary focus:ring-2 focus:ring-accent focus:border-accent"
                placeholder="Details..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary"
              >
                <option value={Priority.P0}>🔴 P0 — Critical</option>
                <option value={Priority.P1}>🟡 P1 — Important</option>
                <option value={Priority.P2}>⚪ P2 — Normal</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Due Date</label>
                <input
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Scheduled For</label>
                <input
                  type="date"
                  value={scheduledFor}
                  onChange={(e) => setScheduledFor(e.target.value)}
                  className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Estimated Minutes</label>
              <input
                type="number"
                value={estimatedMinutes}
                onChange={(e) => setEstimatedMinutes(e.target.value)}
                min="0"
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary"
                placeholder="e.g. 30"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Tags</label>
              <input
                type="text"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="w-full bg-bg-app border border-border rounded-md px-3 py-2 text-sm text-text-primary"
                placeholder="coursework, ml, cert-prep (comma-separated)"
              />
            </div>

            <div className="flex gap-3 pt-4">
              <button
                type="submit"
                disabled={createMutation.isPending || updateMutation.isPending}
                className="flex-1 bg-accent text-white py-2 px-4 rounded-md text-sm font-medium hover:bg-accent-hover disabled:opacity-50 transition-colors"
              >
                {isEdit ? 'Save Changes' : 'Create Task'}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-border rounded-md text-sm text-text-secondary hover:bg-bg-card transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
