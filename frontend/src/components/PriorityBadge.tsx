import { Priority } from '../types'

const priorityConfig: Record<Priority, { label: string; classes: string }> = {
  [Priority.P0]: { label: 'P0', classes: 'bg-[rgba(239,78,82,0.16)] text-[#F2888A]' },
  [Priority.P1]: { label: 'P1', classes: 'bg-[rgba(245,165,36,0.16)] text-[#F7BE5A]' },
  [Priority.P2]: { label: 'P2', classes: 'bg-[rgba(107,116,134,0.16)] text-text-muted' },
}

export default function PriorityBadge({ priority }: { priority: Priority }) {
  const config = priorityConfig[priority]
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded ${config.classes}`}>
      {config.label}
    </span>
  )
}
