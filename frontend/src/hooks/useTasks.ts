import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'
import type { Task, TaskCreate, TaskUpdate } from '../types'

export function useTasks(view: 'today' | 'backlog' | 'done') {
  return useQuery<Task[]>({
    queryKey: ['tasks', view],
    queryFn: async () => {
      const { data } = await client.get(`/tasks?view=${view}`)
      return data
    },
  })
}

export function useCreateTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (body: TaskCreate) => {
      const { data } = await client.post('/tasks', body)
      return data as Task
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export function useUpdateTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, ...body }: TaskUpdate & { id: string }) => {
      const { data } = await client.put(`/tasks/${id}`, body)
      return data as Task
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export function useCompleteTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      const { data } = await client.post(`/tasks/${id}/complete`)
      return data as Task
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export function useDeleteTask() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await client.delete(`/tasks/${id}`)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}
