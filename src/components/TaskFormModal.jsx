import { useState } from 'react'
import Modal from './Modal'
import {
  DESCRIPTION_MAX,
  PRIORITIES,
  STATUSES,
  TITLE_MAX,
  countChars,
  validateTask,
} from '../utils/validation'

const EMPTY_FORM = { title: '', description: '', priority: 'Medium', status: 'To Do', dueDate: '' }

// One form for both "New Task" (no task prop) and "Edit Task" (task prop).
// The modal is only mounted while open, so the form starts fresh every time it opens.
export default function TaskFormModal({ task, onSave, onClose }) {
  const isEdit = Boolean(task)
  const [values, setValues] = useState(
    task
      ? {
          title: task.title,
          description: task.description,
          priority: task.priority,
          status: task.status,
          dueDate: task.dueDate || '',
        }
      : EMPTY_FORM,
  )
  const [submitted, setSubmitted] = useState(false)

  // Errors appear on the first submit, then stay live while the user edits.
  const errors = submitted ? validateTask(values) : {}

  const titleLength = countChars(values.title.trim())
  const descriptionLength = countChars(values.description.trim())

  function handleChange(event) {
    setValues({ ...values, [event.target.name]: event.target.value })
  }

  function handleSubmit(event) {
    event.preventDefault()
    setSubmitted(true)
    const found = validateTask(values)
    const firstInvalid = Object.keys(found)[0]
    if (firstInvalid) {
      event.currentTarget.elements.namedItem(firstInvalid)?.focus()
      return // invalid: do not save, keep the modal open
    }
    onSave(values)
  }

  const invalid = (field) => (errors[field] ? 'true' : 'false')

  return (
    <Modal title={isEdit ? 'Edit Task' : 'New Task'} onClose={onClose}>
      <form onSubmit={handleSubmit} noValidate>
        <div className="modal-body">
          <div className="field">
            <label htmlFor="task-title">Task Title</label>
            <input
              id="task-title"
              name="title"
              type="text"
              placeholder="e.g. Write Weekly Report"
              value={values.title}
              onChange={handleChange}
              aria-required="true"
              aria-invalid={invalid('title')}
              aria-describedby="task-title-count task-title-error"
              autoComplete="off"
              data-autofocus
            />
            <div className="field-meta">
              <span>Required, 3 to 80 characters</span>
              <span id="task-title-count" className={titleLength > TITLE_MAX ? 'counter counter-over' : 'counter'}>
                {titleLength} / {TITLE_MAX}
              </span>
            </div>
            {errors.title && (
              <p id="task-title-error" className="field-error">
                {errors.title}
              </p>
            )}
          </div>

          <div className="field">
            <label htmlFor="task-description">Description</label>
            <textarea
              id="task-description"
              name="description"
              rows={4}
              placeholder="Optional details about the task"
              value={values.description}
              onChange={handleChange}
              aria-invalid={invalid('description')}
              aria-describedby="task-description-count task-description-error"
            />
            <div className="field-meta">
              <span>Optional</span>
              <span
                id="task-description-count"
                className={descriptionLength > DESCRIPTION_MAX ? 'counter counter-over' : 'counter'}
              >
                {descriptionLength} / {DESCRIPTION_MAX}
              </span>
            </div>
            {errors.description && (
              <p id="task-description-error" className="field-error">
                {errors.description}
              </p>
            )}
          </div>

          <div className="field-row">
            <div className="field">
              <label htmlFor="task-priority">Priority</label>
              <select
                id="task-priority"
                name="priority"
                value={values.priority}
                onChange={handleChange}
                aria-invalid={invalid('priority')}
                aria-describedby="task-priority-error"
              >
                {PRIORITIES.map((priority) => (
                  <option key={priority} value={priority}>
                    {priority}
                  </option>
                ))}
              </select>
              {errors.priority && (
                <p id="task-priority-error" className="field-error">
                  {errors.priority}
                </p>
              )}
            </div>

            <div className="field">
              <label htmlFor="task-status">Status</label>
              <select
                id="task-status"
                name="status"
                value={values.status}
                onChange={handleChange}
                aria-invalid={invalid('status')}
                aria-describedby="task-status-error"
              >
                {STATUSES.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
              {errors.status && (
                <p id="task-status-error" className="field-error">
                  {errors.status}
                </p>
              )}
            </div>
          </div>

          <div className="field">
            <label htmlFor="task-dueDate">Due Date</label>
            <input
              id="task-dueDate"
              name="dueDate"
              type="date"
              value={values.dueDate}
              onChange={handleChange}
              aria-invalid={invalid('dueDate')}
              aria-describedby="task-dueDate-hint task-dueDate-error"
            />
            <div className="field-meta">
              <span id="task-dueDate-hint">Optional</span>
            </div>
            {errors.dueDate && (
              <p id="task-dueDate-error" className="field-error">
                {errors.dueDate}
              </p>
            )}
          </div>
        </div>

        <div className="modal-footer">
          <button type="button" className="button button-secondary" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="button button-primary">
            {isEdit ? 'Save Changes' : 'Create Task'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
