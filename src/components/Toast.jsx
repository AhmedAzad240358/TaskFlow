import { useEffect } from 'react'
import { CircleAlert, CircleCheck, X } from 'lucide-react'

// Pass a new key from the parent for every toast so the 3-second timer restarts.
export default function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  const Icon = type === 'error' ? CircleAlert : CircleCheck
  return (
    <div className={`toast toast-${type}`} role={type === 'error' ? 'alert' : 'status'}>
      <Icon size={20} aria-hidden="true" />
      <span className="toast-message">{message}</span>
      <button type="button" className="icon-button toast-close" aria-label="Dismiss notification" onClick={onClose}>
        <X size={18} aria-hidden="true" />
      </button>
    </div>
  )
}
