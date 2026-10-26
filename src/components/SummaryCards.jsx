import { CircleCheck, Clock, ListChecks, ListTodo } from 'lucide-react'

// Always counts ALL tasks, no matter which search or filters are active.
export default function SummaryCards({ tasks }) {
  const countOf = (status) => tasks.filter((task) => task.status === status).length
  const cards = [
    { label: 'Total Tasks', count: tasks.length, icon: ListChecks, tone: 'primary' },
    { label: 'To Do', count: countOf('To Do'), icon: ListTodo, tone: 'neutral' },
    { label: 'In Progress', count: countOf('In Progress'), icon: Clock, tone: 'warning' },
    { label: 'Completed', count: countOf('Completed'), icon: CircleCheck, tone: 'success' },
  ]

  return (
    <section className="summary" aria-label="Task summary">
      {cards.map(({ label, count, icon: Icon, tone }) => (
        <div key={label} className="summary-card">
          <span className={`summary-icon tone-${tone}`}>
            <Icon size={22} aria-hidden="true" />
          </span>
          <div>
            <p className="summary-label">{label}</p>
            <p className="summary-count">{count}</p>
          </div>
        </div>
      ))}
    </section>
  )
}
