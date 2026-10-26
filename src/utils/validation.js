import { isValidDateString } from './dates.js'

// The only values the app accepts (TF-REQ-004 and TF-REQ-005).
export const PRIORITIES = ['Low', 'Medium', 'High']
export const STATUSES = ['To Do', 'In Progress', 'Completed']

export const TITLE_MIN = 3
export const TITLE_MAX = 80
export const DESCRIPTION_MAX = 500

// Length in Unicode code points, so an emoji counts as 1 character (string.length would say 2).
export const countChars = (text) => [...text].length

// Checks a task form (or a saved task) and returns { fieldName: message }.
// An empty object means the values are valid. Used by create, edit and the storage loader.
export function validateTask(values) {
  const errors = {}

  // TF-REQ-001 / TF-REQ-002: trim first, then count characters.
  const titleLength = countChars(typeof values.title === 'string' ? values.title.trim() : '')
  if (titleLength === 0) errors.title = 'Title is required.'
  else if (titleLength < TITLE_MIN) errors.title = `Title must be at least ${TITLE_MIN} characters.`
  else if (titleLength > TITLE_MAX) errors.title = `Title must be ${TITLE_MAX} characters or fewer.`

  // TF-REQ-003: optional, up to 500 characters (leading/trailing spaces are not counted or saved).
  const description = values.description ?? ''
  if (typeof description !== 'string' || countChars(description.trim()) > DESCRIPTION_MAX) {
    errors.description = `Description must be ${DESCRIPTION_MAX} characters or fewer.`
  }

  // TF-REQ-004 / TF-REQ-005: only the listed values are allowed.
  if (!PRIORITIES.includes(values.priority)) errors.priority = 'Please select a valid priority.'
  if (!STATUSES.includes(values.status)) errors.status = 'Please select a valid status.'

  // TF-REQ-006: optional; if present it must be a real YYYY-MM-DD date. Past dates are fine.
  const { dueDate } = values
  if (dueDate !== undefined && dueDate !== null && dueDate !== '' && !isValidDateString(dueDate)) {
    errors.dueDate = 'Please enter a valid date (YYYY-MM-DD).'
  }

  return errors
}
