// Helpers for building, searching, filtering and sorting tasks. No React in here.

export const SORT_OPTIONS = [
  { value: 'newest', label: 'Newest first' },
  { value: 'oldest', label: 'Oldest first' },
  { value: 'due-soonest', label: 'Due date: soonest' },
  { value: 'due-latest', label: 'Due date: latest' },
]

// crypto.randomUUID only exists on https:// and localhost, so keep a fallback.
export function newId() {
  const uuid = globalThis.crypto?.randomUUID?.()
  return uuid ?? `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

// The form values that get saved: title and description are trimmed, no date becomes "".
export function normalizeValues(values) {
  return {
    title: values.title.trim(),
    description: (values.description ?? '').trim(),
    priority: values.priority,
    status: values.status,
    dueDate: values.dueDate || '',
  }
}

export function buildTask(values) {
  const now = new Date().toISOString()
  return { id: newId(), ...normalizeValues(values), createdAt: now, updatedAt: now }
}

// Search + status + priority combine with AND (TF-REQ-019), then the list is sorted.
export function filterAndSortTasks(tasks, { search, status, priority, sort }) {
  const query = search.trim().toLowerCase()
  const matches = tasks.filter(
    (task) =>
      (status === 'All' || task.status === status) &&
      (priority === 'All' || task.priority === priority) &&
      (query === '' || task.title.toLowerCase().includes(query) || task.description.toLowerCase().includes(query)),
  )

  const created = (task) => Date.parse(task.createdAt)
  const newestFirst = (a, b) => created(b) - created(a)
  // direction 1 = soonest first, -1 = latest first. Tasks without a due date always go last.
  const byDueDate = (direction) => (a, b) => {
    if (!a.dueDate && !b.dueDate) return newestFirst(a, b)
    if (!a.dueDate) return 1
    if (!b.dueDate) return -1
    if (a.dueDate === b.dueDate) return newestFirst(a, b)
    return (a.dueDate < b.dueDate ? -1 : 1) * direction
  }
  const comparators = {
    newest: newestFirst,
    oldest: (a, b) => created(a) - created(b),
    'due-soonest': byDueDate(1),
    'due-latest': byDueDate(-1),
  }
  return matches.sort(comparators[sort] ?? newestFirst)
}
