import Modal from './Modal'

export default function ConfirmDeleteModal({ task, onConfirm, onClose }) {
  return (
    <Modal title="Delete Task" onClose={onClose}>
      <div className="modal-body">
        <p className="confirm-text">
          Are you sure you want to delete &quot;{task.title}&quot;? This cannot be undone.
        </p>
      </div>
      <div className="modal-footer">
        <button type="button" className="button button-secondary" onClick={onClose} data-autofocus>
          Cancel
        </button>
        <button type="button" className="button button-danger" onClick={onConfirm}>
          Confirm Delete
        </button>
      </div>
    </Modal>
  )
}
