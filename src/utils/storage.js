import { normalizeValues } from './tasks.js'
import { validateTask } from './validation.js'

export const STORAGE_KEY = 'taskflow_tasks'
export const BACKUP_KEY = 'taskflow_tasks_backup'

const CORRUPTED = 'Saved task data was corrupted and could not be loaded. A backup was kept.'

function keepBackup(raw) {
  try {
    localStorage.setItem(BACKUP_KEY, raw)
  } catch {
    // Nothing more we can do if storage is full or blocked.
  }
}

// A saved entry is kept only if it passes the same rules as the form, has a string id and a real createdAt.
function toSavedTask(item, seenIds) {
  if (!item || typeof item !== 'object') return null
  if (typeof item.id !== 'string' || item.id === '' || seenIds.has(item.id)) return null
  if (Object.keys(validateTask(item)).length > 0) return null
  if (!Number.isFinite(Date.parse(item.createdAt))) return null
  const updatedAt = Number.isFinite(Date.parse(item.updatedAt)) ? item.updatedAt : item.createdAt
  return { id: item.id, ...normalizeValues(item), createdAt: item.createdAt, updatedAt }
}

// Never throws. Returns { tasks, warning } where warning is null or { message, canReset }.
export function loadTasks() {
  let raw
  try {
    raw = localStorage.getItem(STORAGE_KEY)
  } catch {
    return {
      tasks: [],
      warning: { message: 'Browser storage is unavailable, so tasks cannot be loaded or saved.', canReset: false },
    }
  }
  if (raw === null) return { tasks: [], warning: null }

  let data
  try {
    data = JSON.parse(raw)
  } catch {
    data = null
  }
  if (!Array.isArray(data)) {
    keepBackup(raw)
    return { tasks: [], warning: { message: CORRUPTED, canReset: true } }
  }

  const seenIds = new Set()
  const tasks = []
  for (const item of data) {
    const task = toSavedTask(item, seenIds)
    if (task) {
      seenIds.add(task.id)
      tasks.push(task)
    }
  }

  const skipped = data.length - tasks.length
  if (skipped === 0) return { tasks, warning: null }
  keepBackup(raw)
  const noun = skipped === 1 ? 'entry was' : 'entries were'
  return {
    tasks,
    warning: { message: `${skipped} saved ${noun} invalid and skipped. A backup was kept.`, canReset: false },
  }
}

// Returns true if the write worked, false if the browser refused it.
export function saveTasks(tasks) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
    return true
  } catch {
    return false
  }
}

// Used by the "Reset storage" button. The backup copy is kept on purpose.
export function resetStorage() {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // Ignore: storage is unavailable.
  }
}
