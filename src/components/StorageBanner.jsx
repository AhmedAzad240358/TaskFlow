import { TriangleAlert, X } from 'lucide-react'

export default function StorageBanner({ warning, onReset, onDismiss }) {
  return (
    <div className="banner" role="alert">
      <TriangleAlert size={20} aria-hidden="true" />
      <p>{warning.message}</p>
      {warning.canReset && (
        <button type="button" className="button button-secondary" onClick={onReset}>
          Reset storage
        </button>
      )}
      <button type="button" className="icon-button" aria-label="Dismiss warning" onClick={onDismiss}>
        <X size={18} aria-hidden="true" />
      </button>
    </div>
  )
}
