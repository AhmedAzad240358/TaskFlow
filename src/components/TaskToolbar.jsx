import { Search } from 'lucide-react'
import { PRIORITIES, STATUSES } from '../utils/validation'
import { SORT_OPTIONS } from '../utils/tasks'

// The search box here and the one in the top bar share the same state (search in App).
export default function TaskToolbar({
  search,
  onSearchChange,
  status,
  onStatusChange,
  priority,
  onPriorityChange,
  sort,
  onSortChange,
  onClear,
}) {
  return (
    <section className="toolbar" aria-label="Task filters">
      <div className="field toolbar-search">
        <label htmlFor="toolbar-search">Search</label>
        <div className="search-box">
          <Search size={18} aria-hidden="true" />
          <input
            id="toolbar-search"
            type="search"
            placeholder="Search by title or description"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
          />
        </div>
      </div>

      <div className="field">
        <label htmlFor="filter-status">Status</label>
        <select id="filter-status" value={status} onChange={(event) => onStatusChange(event.target.value)}>
          <option value="All">All Statuses</option>
          {STATUSES.map((value) => (
            <option key={value} value={value}>
              {value}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="filter-priority">Priority</label>
        <select id="filter-priority" value={priority} onChange={(event) => onPriorityChange(event.target.value)}>
          <option value="All">All Priorities</option>
          {PRIORITIES.map((value) => (
            <option key={value} value={value}>
              {value}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="sort-by">Sort by</label>
        <select id="sort-by" value={sort} onChange={(event) => onSortChange(event.target.value)}>
          {SORT_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <button type="button" className="button button-secondary" onClick={onClear}>
        Clear Filters
      </button>
    </section>
  )
}
