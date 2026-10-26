import { useEffect, useId, useRef } from 'react'
import { X } from 'lucide-react'

// Shared dialog shell for the task form and the delete confirmation.
// Escape, the X button and a click on the dark backdrop all call onClose (same as Cancel).
// Put data-autofocus on the element that should receive focus when the dialog opens.
export default function Modal({ title, onClose, children }) {
  const titleId = useId()
  const dialogRef = useRef(null)
  const openerRef = useRef(document.activeElement)
  const onCloseRef = useRef(onClose)
  onCloseRef.current = onClose // always call the newest onClose without re-running the effect

  useEffect(() => {
    const opener = openerRef.current
    const onKeyDown = (event) => {
      if (event.key === 'Escape') onCloseRef.current()
    }
    document.addEventListener('keydown', onKeyDown)
    document.body.classList.add('modal-open')
    dialogRef.current.querySelector('[data-autofocus]')?.focus()

    return () => {
      document.removeEventListener('keydown', onKeyDown)
      document.body.classList.remove('modal-open')
      opener?.focus?.() // give focus back to the button that opened the dialog
    }
  }, [])

  return (
    <div
      className="modal-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby={titleId} ref={dialogRef}>
        <div className="modal-header">
          <h2 id={titleId}>{title}</h2>
          <button type="button" className="icon-button" aria-label="Close" onClick={onClose}>
            <X size={20} aria-hidden="true" />
          </button>
        </div>
        {children}
      </div>
    </div>
  )
}
