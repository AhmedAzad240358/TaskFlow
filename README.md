# TaskFlow

A single-user task manager built with React + Vite. It is the software under test for an SQA project, so behaviour and on-screen text are kept predictable.

## Run it

```
npm install
npm run dev      # http://localhost:5173
npm test         # validation + overdue checks (plain node:assert)
npm run build    # production build into dist/
```

No backend, login or API key. Data lives in the browser's localStorage.

## Storage

- Tasks: localStorage key `taskflow_tasks` (JSON array).
- If that value is not valid JSON or not an array, the raw text is copied to `taskflow_tasks_backup`, the app starts empty and shows a warning banner with a "Reset storage" button (removes `taskflow_tasks`, keeps the backup).
- Saved entries with a missing id, bad title/priority/status/due date, missing createdAt or a duplicate id are skipped and counted in the banner (no Reset button in that case, the other tasks stay).
- Task fields: `id`, `title`, `description`, `priority`, `status`, `dueDate` (`YYYY-MM-DD` or `""`), `createdAt`, `updatedAt` (ISO timestamps).

## Requirements traceability

| Requirement | Where it is implemented |
|---|---|
| TF-REQ-001 Required title | `src/utils/validation.js` (`validateTask`), inline message in `src/components/TaskFormModal.jsx` |
| TF-REQ-002 Title length 3-80 (code points, trimmed) | `src/utils/validation.js` (`countChars`, `TITLE_MIN`, `TITLE_MAX`), counter in `TaskFormModal.jsx` |
| TF-REQ-003 Description max 500 + counter | `validation.js`, counter in `TaskFormModal.jsx` |
| TF-REQ-004 Priority Low/Medium/High, default Medium | `validation.js` (`PRIORITIES`), `TaskFormModal.jsx` (default + dropdown) |
| TF-REQ-005 Status To Do/In Progress/Completed, default To Do | `validation.js` (`STATUSES`), `TaskFormModal.jsx` (default + dropdown) |
| TF-REQ-006 Due date + overdue | `src/utils/dates.js` (`isValidDateString`, `isOverdue`), `src/components/TaskCard.jsx` (Overdue badge, red date) |
| TF-REQ-007 Successful creation | `src/App.jsx` (`createTask`, `commit`), `src/utils/tasks.js` (`buildTask`), `src/utils/storage.js` (`saveTasks`), `Toast.jsx` |
| TF-REQ-008 Cancel creation | `TaskFormModal.jsx` Cancel button, `Modal.jsx` (Escape, X, backdrop) |
| TF-REQ-009 Prefilled edit form | `TaskFormModal.jsx` (`task` prop), `App.jsx` (edit modal keyed by task id) |
| TF-REQ-010 Successful editing | `App.jsx` (`updateTask`): keeps `id` and `createdAt`, sets `updatedAt` |
| TF-REQ-011 Invalid editing | `TaskFormModal.jsx` (`handleSubmit`): modal stays open, nothing is saved |
| TF-REQ-012 Cancel editing | `Modal.jsx` / `TaskFormModal.jsx`: unsaved changes are discarded |
| TF-REQ-013 Delete confirmation | `src/components/ConfirmDeleteModal.jsx` |
| TF-REQ-014 Confirm deletion | `App.jsx` (`deleteTask`) |
| TF-REQ-015 Cancel deletion | `ConfirmDeleteModal.jsx` Cancel button |
| TF-REQ-016 Status updates | `App.jsx` (`changeStatus`), status dropdown in `TaskCard.jsx`, counts in `SummaryCards.jsx` |
| TF-REQ-017 Completed tasks | `dates.js` (`isOverdue` ignores Completed), `SummaryCards.jsx` (own count) |
| TF-REQ-018 Priority updates | Edit modal (`TaskFormModal.jsx`), priority filter in `TaskToolbar.jsx` / `src/utils/tasks.js` |
| TF-REQ-019 Search | `src/utils/tasks.js` (`filterAndSortTasks`), search inputs in `TopBar.jsx` and `TaskToolbar.jsx` (shared state) |

## Exact messages (for expected results)

Validation (shown under the field; the form is not saved while any is showing):

| Case | Message |
|---|---|
| Title empty or only spaces | `Title is required.` |
| Title under 3 characters (after trimming) | `Title must be at least 3 characters.` |
| Title over 80 characters (after trimming) | `Title must be 80 characters or fewer.` |
| Description over 500 characters (after trimming) | `Description must be 500 characters or fewer.` |
| Priority not Low/Medium/High | `Please select a valid priority.` |
| Status not To Do/In Progress/Completed | `Please select a valid status.` |
| Due date not a real YYYY-MM-DD date | `Please enter a valid date (YYYY-MM-DD).` |

Notes: length is counted in Unicode code points (an emoji = 1). Leading/trailing spaces are trimmed before counting and before saving. The inputs have no `maxLength`, so 81 and 501 characters can be typed. The counters read `n / 80` and `n / 500` and turn red when over. After the first failed submit the messages update live.

Toasts (auto-close after about 3 seconds, or click the X):

| Action | Toast |
|---|---|
| Create | `Task created successfully.` |
| Edit | `Task updated successfully.` |
| Delete | `Task deleted successfully.` |
| Status changed from the list | `Task status updated.` |
| Browser refused the save (storage full/blocked) | `Could not save tasks to browser storage.` |

Empty states:

| Case | Title | Button |
|---|---|---|
| No tasks at all | `No tasks yet` | `Create your first task` |
| Search has no hits | `No tasks match "<query>"` | `Clear search` |
| Filters have no hits | `No tasks match the current filters` | `Clear filters` |

Storage warnings:

- `Saved task data was corrupted and could not be loaded. A backup was kept.`
- `<n> saved entry was invalid and skipped. A backup was kept.` / `<n> saved entries were invalid and skipped. A backup was kept.`
- `Browser storage is unavailable, so tasks cannot be loaded or saved.`

Dialog text: "New Task" (Cancel / Create Task), "Edit Task" (Cancel / Save Changes), "Delete Task" with `Are you sure you want to delete "<title>"? This cannot be undone.` (Cancel / Confirm Delete).

## Behaviour notes

- Overdue = due date earlier than today (local date) and status not Completed. Due today is not overdue (it shows a "Due today" badge instead).
- The summary cards always count all tasks, ignoring search and filters.
- Search is case-insensitive, trims the query, and matches part of a title or description. Search, status and priority filters combine with AND.
- Sort: Newest first (default), Oldest first, Due date: soonest, Due date: latest. Tasks with no due date are always last in the due-date sorts.
- Sidebar: Dashboard and All Tasks show every status; To Do / In Progress / Completed set the status filter (and the page title follows). Collapse button on desktop, drawer under 768px.
