export default function AgingIndicator({ count }: { count: number }) {
  if (count < 3) return null

  return (
    <span
      className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-[rgba(239,78,82,0.16)] text-[#F2888A]"
      title={`Rolled over ${count} time(s)`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-priority-p0" />
      rolled over {count}×
    </span>
  )
}
