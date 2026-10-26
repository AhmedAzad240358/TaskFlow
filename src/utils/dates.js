// Date helpers. A due date is a plain "YYYY-MM-DD" string that always means a LOCAL calendar day.
// We never call new Date("2026-10-26"): that parses as UTC and can shift the day.

const DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
const isLeapYear = (year) => (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0
const pad = (number) => String(number).padStart(2, '0')

// True only for real calendar dates written exactly as YYYY-MM-DD.
// 2026-02-29 and 2026-13-01 are invalid, 2028-02-29 is valid.
export function isValidDateString(value) {
  if (typeof value !== 'string') return false
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  if (!match) return false
  const year = Number(match[1])
  const month = Number(match[2])
  const day = Number(match[3])
  if (month < 1 || month > 12 || day < 1) return false
  const lastDay = month === 2 && isLeapYear(year) ? 29 : DAYS_IN_MONTH[month - 1]
  return day <= lastDay
}

// Today's local date as YYYY-MM-DD. The "now" argument exists so tests can pass a fixed date.
export function todayString(now = new Date()) {
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
}

// TF-REQ-006: overdue = due date before today AND not Completed. Due today is NOT overdue.
// YYYY-MM-DD strings compare correctly with < because they are zero-padded.
export function isOverdue(task, today = todayString()) {
  return Boolean(task.dueDate) && task.dueDate < today && task.status !== 'Completed'
}

const SHORT_DATE = { month: 'short', day: 'numeric', year: 'numeric' }

// "2026-10-26" -> "Oct 26, 2026"
export function formatDueDate(dateString) {
  const [year, month, day] = dateString.split('-').map(Number)
  const date = new Date(2000, 0, 1)
  date.setFullYear(year, month - 1, day) // setFullYear keeps years 0-99 as written
  return date.toLocaleDateString('en-US', SHORT_DATE)
}

// ISO timestamp -> "Oct 26, 2026" (in the browser's local time zone)
export function formatTimestamp(isoString) {
  return new Date(isoString).toLocaleDateString('en-US', SHORT_DATE)
}

// "Monday, October 26, 2026" for the top bar
export function formatToday(now = new Date()) {
  return now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}
