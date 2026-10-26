// Run with: npm test   (plain node:assert, no test framework)
import assert from 'node:assert/strict'
import { isOverdue, isValidDateString, todayString } from './dates.js'
import { validateTask } from './validation.js'

// A valid form; each check below changes one field.
const valid = { title: 'Write report', description: '', priority: 'Medium', status: 'To Do', dueDate: '' }
const check = (changes) => validateTask({ ...valid, ...changes })

let passed = 0
function test(name, fn) {
  fn()
  passed++
  console.log(`  ok  ${name}`)
}

// TF-REQ-001 / TF-REQ-002 : title
test('valid baseline has no errors', () => assert.deepEqual(check({}), {}))
test('empty title is required', () => assert.equal(check({ title: '' }).title, 'Title is required.'))
test('whitespace-only title is required', () => assert.equal(check({ title: '     ' }).title, 'Title is required.'))
test('title of 2 characters is too short', () => assert.equal(check({ title: 'ab' }).title, 'Title must be at least 3 characters.'))
test('title of 3 characters is valid', () => assert.equal(check({ title: 'abc' }).title, undefined))
test('title of 80 characters is valid', () => assert.equal(check({ title: 'a'.repeat(80) }).title, undefined))
test('title of 81 characters is too long', () => assert.equal(check({ title: 'a'.repeat(81) }).title, 'Title must be 80 characters or fewer.'))
test('spaces around the title are trimmed before counting', () => {
  assert.equal(check({ title: '  ab  ' }).title, 'Title must be at least 3 characters.')
  assert.equal(check({ title: `  ${'a'.repeat(80)}  ` }).title, undefined)
})
test('emoji count as 1 character (code points)', () => {
  assert.equal(check({ title: '😀'.repeat(80) }).title, undefined) // 80 code points, 160 UTF-16 units
  assert.equal(check({ title: '😀'.repeat(81) }).title, 'Title must be 80 characters or fewer.')
  assert.equal(check({ title: '😀😀' }).title, 'Title must be at least 3 characters.')
  assert.equal(check({ title: '😀😀😀' }).title, undefined)
})

// TF-REQ-003 : description
test('description is optional', () => assert.equal(check({ description: '' }).description, undefined))
test('description of 500 characters is valid', () => assert.equal(check({ description: 'a'.repeat(500) }).description, undefined))
test('description of 501 characters is invalid', () =>
  assert.equal(check({ description: 'a'.repeat(501) }).description, 'Description must be 500 characters or fewer.'))
test('description counts emoji as 1 character', () => {
  assert.equal(check({ description: '😀'.repeat(500) }).description, undefined)
  assert.equal(check({ description: '😀'.repeat(501) }).description, 'Description must be 500 characters or fewer.')
})

// TF-REQ-004 / TF-REQ-005 : priority and status
test('Low, Medium and High priorities are valid', () => {
  for (const priority of ['Low', 'Medium', 'High']) assert.equal(check({ priority }).priority, undefined)
})
test('invalid priority is rejected', () => {
  for (const priority of ['Urgent', 'high', '', undefined]) {
    assert.equal(check({ priority }).priority, 'Please select a valid priority.')
  }
})
test('To Do, In Progress and Completed statuses are valid', () => {
  for (const status of ['To Do', 'In Progress', 'Completed']) assert.equal(check({ status }).status, undefined)
})
test('invalid status is rejected', () => {
  for (const status of ['Done', 'completed', '', undefined]) {
    assert.equal(check({ status }).status, 'Please select a valid status.')
  }
})

// TF-REQ-006 : due date
const BAD_DATE = 'Please enter a valid date (YYYY-MM-DD).'
test('due date is optional', () => {
  for (const dueDate of ['', null, undefined]) assert.equal(check({ dueDate }).dueDate, undefined)
})
test('valid dates are accepted (including past dates)', () => {
  for (const dueDate of ['2026-10-26', '2000-01-01', '2028-02-29', '2000-02-29', '2026-12-31']) {
    assert.equal(check({ dueDate }).dueDate, undefined, dueDate)
  }
})
test('malformed dates are rejected', () => {
  for (const dueDate of ['26-10-2026', '2026/10/26', '2026-1-5', 'tomorrow', '2026-10-26T00:00', ' 2026-10-26', '202026-01-01', 20261026]) {
    assert.equal(check({ dueDate }).dueDate, BAD_DATE, String(dueDate))
  }
})
test('impossible dates are rejected', () => {
  for (const dueDate of ['2026-02-29', '1900-02-29', '2026-13-01', '2026-00-10', '2026-04-31', '2026-01-00', '2026-01-32']) {
    assert.equal(check({ dueDate }).dueDate, BAD_DATE, dueDate)
    assert.equal(isValidDateString(dueDate), false, dueDate)
  }
})

// TF-REQ-006 : overdue rule (uses today's real local date)
test('overdue: yesterday is overdue, today is not, Completed is never overdue', () => {
  const now = new Date()
  const yesterday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1)
  const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1)
  const today = todayString(now)

  assert.equal(isOverdue({ dueDate: todayString(yesterday), status: 'To Do' }), true)
  assert.equal(isOverdue({ dueDate: todayString(yesterday), status: 'In Progress' }), true)
  assert.equal(isOverdue({ dueDate: today, status: 'To Do' }), false)
  assert.equal(isOverdue({ dueDate: todayString(tomorrow), status: 'To Do' }), false)
  assert.equal(isOverdue({ dueDate: todayString(yesterday), status: 'Completed' }), false)
  assert.equal(isOverdue({ dueDate: '', status: 'To Do' }), false)
})
test('overdue: fixed-date checks', () => {
  assert.equal(isOverdue({ dueDate: '2026-10-25', status: 'To Do' }, '2026-10-26'), true)
  assert.equal(isOverdue({ dueDate: '2026-10-26', status: 'To Do' }, '2026-10-26'), false)
  assert.equal(isOverdue({ dueDate: '2025-12-31', status: 'To Do' }, '2026-01-01'), true) // year boundary
  assert.equal(isOverdue({ dueDate: '2026-10-01', status: 'Completed' }, '2026-10-26'), false)
})

console.log(`\n${passed} checks passed`)
