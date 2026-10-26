import { ClipboardList, FilterX, SearchX } from 'lucide-react'
import EmptyState from './EmptyState'
import TaskCard from './TaskCard'

// Shows the task cards, or the right empty state when there is nothing to show.
export default function TaskList({
  totalCount,
  tasks,
  search,
  today,
  onEdit,
  onDelete,
  onStatusChange,
  onCreate,
  onClearSearch,
  onClearFilters,
}) {
  const query = search.trim()

  if (totalCount === 0) {
    return (
      <EmptyState
        icon={ClipboardList}
        title="No tasks yet"
        text="Tasks you create will appear here."
        actionLabel="Create your first task"
        onAction={onCreate}
      />
    )
  }

  if (tasks.length === 0 && query !== '') {
    return (
      <EmptyState
        icon={SearchX}
        title={`No tasks match "${query}"`}
        text="Try a different search term."
        actionLabel="Clear search"
        onAction={onClearSearch}
      />
    )
  }

  if (tasks.length === 0) {
    return (
      <EmptyState
        icon={FilterX}
        title="No tasks match the current filters"
        text="Try changing or clearing your filters."
        actionLabel="Clear filters"
        onAction={onClearFilters}
      />
    )
  }

  return (
    <>
      <p className="result-count">
        Showing {tasks.length} of {totalCount} {totalCount === 1 ? 'task' : 'tasks'}
      </p>
      <ul className="task-list">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} today={today} onEdit={onEdit} onDelete={onDelete} onStatusChange={onStatusChange} />
        ))}
      </ul>
    </>
  )
}
