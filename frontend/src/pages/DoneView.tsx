import { useTasks } from '../hooks/useTasks'
import TaskCard from '../components/TaskCard'

export default function DoneView() {
  const { data: tasks, isLoading } = useTasks('done')

  if (isLoading) {
    return <div className="text-text-muted">Loading completed tasks...</div>
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Done</h1>
        <p className="text-sm text-text-secondary mt-1">
          {tasks?.length ?? 0} completed task(s)
        </p>
      </div>

      {tasks && tasks.length > 0 ? (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} showComplete={false} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-text-muted">
          <p className="text-lg">No completed tasks yet</p>
          <p className="text-sm mt-1">Get to work!</p>
        </div>
      )}
    </div>
  )
}
