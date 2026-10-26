export default function EmptyState({ icon: Icon, title, text, actionLabel, onAction }) {
  return (
    <div className="empty-state">
      <Icon size={40} aria-hidden="true" />
      <h3>{title}</h3>
      <p>{text}</p>
      <button type="button" className="button button-primary" onClick={onAction}>
        {actionLabel}
      </button>
    </div>
  )
}
