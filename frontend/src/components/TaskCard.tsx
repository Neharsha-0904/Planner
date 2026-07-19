import type { Task } from '../types'
import PriorityBadge from './PriorityBadge'
import AgingIndicator from './AgingIndicator'
import { useCompleteTask, useDeleteTask } from '../hooks/useTasks'

interface TaskCardProps {
  task: Task
  showComplete?: boolean
  onEdit?: (task: Task) => void
}

export default function TaskCard({ task, showComplete = true, onEdit }: TaskCardProps) {
  const completeMutation = useCompleteTask()
  const deleteMutation = useDeleteTask()

  return (
    <div className="bg-bg-card rounded-lg border border-border p-4 hover:border-accent/30 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <PriorityBadge priority={task.priority} />
            <AgingIndicator count={task.rolled_over_count} />
            {task.due_date && (
              <span className="text-xs text-text-secondary">Due: {task.due_date}</span>
            )}
          </div>
          <h3 className="font-medium text-text-primary truncate">{task.title}</h3>
          {task.description && (
            <p className="text-sm text-text-secondary mt-1 line-clamp-2">{task.description}</p>
          )}
          {task.tags && task.tags.length > 0 && (
            <div className="flex gap-1 mt-2">
              {task.tags.map((tag) => (
                <span key={tag} className="text-xs bg-[rgba(107,116,134,0.16)] text-text-secondary px-2 py-0.5 rounded">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="flex flex-col gap-1">
          {showComplete && (
            <button
              onClick={() => completeMutation.mutate(task.id)}
              disabled={completeMutation.isPending}
              className="text-xs px-2 py-1 bg-[rgba(52,211,153,0.16)] text-status-done rounded hover:bg-[rgba(52,211,153,0.24)] transition-colors"
            >
              ✓ Done
            </button>
          )}
          {onEdit && (
            <button
              onClick={() => onEdit(task)}
              className="text-xs px-2 py-1 bg-[rgba(107,116,134,0.16)] text-text-secondary rounded hover:bg-[rgba(107,116,134,0.24)] transition-colors"
            >
              Edit
            </button>
          )}
          <button
            onClick={() => {
              if (confirm('Delete this task?')) deleteMutation.mutate(task.id)
            }}
            disabled={deleteMutation.isPending}
            className="text-xs px-2 py-1 bg-[rgba(239,78,82,0.16)] text-[#F2888A] rounded hover:bg-[rgba(239,78,82,0.24)] transition-colors"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  )
}
