import { Pencil, Trash2 } from 'lucide-react'
import { STATUSES } from '../utils/validation'
import { formatDueDate, formatTimestamp, isOverdue } from '../utils/dates'

export default function TaskCard({ task, today, onEdit, onDelete, onStatusChange }) {
  const overdue = isOverdue(task, today)
  const dueToday = task.dueDate === today && task.status !== 'Completed'
  const className = ['task-card', overdue && 'overdue', task.status === 'Completed' && 'completed']
    .filter(Boolean)
    .join(' ')

  return (
    <li className={className}>
      <div className="task-main">
        <div className="task-head">
          <h3 className="task-title">{task.title}</h3>
          <span className={`badge priority-${task.priority.toLowerCase()}`} title={`Priority: ${task.priority}`}>
            {task.priority}
          </span>
          <span className={`badge status-${task.status.toLowerCase().replace(' ', '-')}`} title={`Status: ${task.status}`}>
            {task.status}
          </span>
          {overdue && <span className="badge badge-overdue">Overdue</span>}
          {dueToday && <span className="badge badge-due-today">Due today</span>}
        </div>

        {task.description && <p className="task-description">{task.description}</p>}

        <p className="task-meta">
          {task.dueDate && (
            <span className={overdue ? 'due-date overdue-text' : 'due-date'}>Due: {formatDueDate(task.dueDate)}</span>
          )}
          <span>Created: {formatTimestamp(task.createdAt)}</span>
        </p>
      </div>

      <div className="task-actions">
        <select
          className="status-select"
          aria-label={`Change status of ${task.title}`}
          value={task.status}
          onChange={(event) => onStatusChange(task.id, event.target.value)}
        >
          {STATUSES.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
        <button type="button" className="button button-secondary" aria-label={`Edit ${task.title}`} onClick={() => onEdit(task.id)}>
          <Pencil size={16} aria-hidden="true" />
          Edit
        </button>
        <button type="button" className="button button-danger-outline" aria-label={`Delete ${task.title}`} onClick={() => onDelete(task.id)}>
          <Trash2 size={16} aria-hidden="true" />
          Delete
        </button>
      </div>
    </li>
  )
}
