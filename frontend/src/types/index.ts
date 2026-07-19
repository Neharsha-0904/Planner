export enum Priority {
  P0 = 'p0',
  P1 = 'p1',
  P2 = 'p2',
}

export enum TaskStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  DONE = 'done',
  BACKLOG = 'backlog',
}

export interface Task {
  id: string
  user_id: string
  title: string
  description: string | null
  priority: Priority
  status: TaskStatus
  created_at: string
  due_date: string | null
  scheduled_for: string | null
  completed_at: string | null
  estimated_minutes: number | null
  actual_minutes: number | null
  parent_task_id: string | null
  milestone_id: string | null
  tags: string[] | null
  recurrence_rule: Record<string, unknown> | null
  rolled_over_count: number
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: Priority
  status?: TaskStatus
  due_date?: string
  scheduled_for?: string
  estimated_minutes?: number
  parent_task_id?: string
  milestone_id?: string
  tags?: string[]
  recurrence_rule?: Record<string, unknown>
}

export interface TaskUpdate extends Partial<TaskCreate> {}

export interface User {
  id: string
  name: string
  email: string
  timezone: string
  prefs: Record<string, unknown> | null
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
