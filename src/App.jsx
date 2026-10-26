import { useCallback, useRef, useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import SummaryCards from './components/SummaryCards'
import TaskToolbar from './components/TaskToolbar'
import TaskList from './components/TaskList'
import TaskFormModal from './components/TaskFormModal'
import ConfirmDeleteModal from './components/ConfirmDeleteModal'
import StorageBanner from './components/StorageBanner'
import Toast from './components/Toast'
import { loadTasks, resetStorage, saveTasks } from './utils/storage'
import { buildTask, filterAndSortTasks, normalizeValues } from './utils/tasks'
import { todayString } from './utils/dates'
import { STATUSES } from './utils/validation'

export default function App() {
  // Load once at startup. loadTasks never throws, even if localStorage holds garbage.
  const [initial] = useState(loadTasks)
  const [tasks, setTasks] = useState(initial.tasks)
  const [warning, setWarning] = useState(initial.warning)

  // Search is shared by the top bar and the toolbar.
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')
  const [priorityFilter, setPriorityFilter] = useState('All')
  const [sort, setSort] = useState('newest')

  const [view, setView] = useState('Dashboard') // 'Dashboard' or 'All Tasks'
  const [collapsed, setCollapsed] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [modal, setModal] = useState(null) // null | { type: 'create' } | { type: 'edit' | 'delete', id }
  const [toast, setToast] = useState(null)
  const toastCount = useRef(0)

  const showToast = (message, type = 'success') => setToast({ message, type, key: ++toastCount.current })
  const dismissToast = useCallback(() => setToast(null), [])
  const closeModal = () => setModal(null)

  // Every change goes through here: update the screen, save immediately, then show a toast.
  function commit(nextTasks, successMessage) {
    setTasks(nextTasks)
    if (saveTasks(nextTasks)) showToast(successMessage)
    else showToast('Could not save tasks to browser storage.', 'error')
  }

  function createTask(values) {
    commit([buildTask(values), ...tasks], 'Task created successfully.')
    closeModal()
  }

  function updateTask(id, values) {
    const changes = { ...normalizeValues(values), updatedAt: new Date().toISOString() }
    commit(tasks.map((task) => (task.id === id ? { ...task, ...changes } : task)), 'Task updated successfully.')
    closeModal()
  }

  function changeStatus(id, status) {
    if (!STATUSES.includes(status)) return
    const updatedAt = new Date().toISOString()
    commit(tasks.map((task) => (task.id === id ? { ...task, status, updatedAt } : task)), 'Task status updated.')
  }

  function deleteTask(id) {
    commit(tasks.filter((task) => task.id !== id), 'Task deleted successfully.')
    closeModal()
  }

  function clearFilters() {
    setSearch('')
    setStatusFilter('All')
    setPriorityFilter('All')
    setSort('newest')
  }

  // Dashboard and All Tasks show every status; the other three items set the status filter.
  function navigate(label) {
    if (STATUSES.includes(label)) {
      setStatusFilter(label)
    } else {
      setView(label)
      setStatusFilter('All')
    }
    setDrawerOpen(false)
  }

  function handleResetStorage() {
    resetStorage()
    setTasks([])
    setWarning(null)
  }

  const activeNav = statusFilter === 'All' ? view : statusFilter
  const visibleTasks = filterAndSortTasks(tasks, { search, status: statusFilter, priority: priorityFilter, sort })
  const editingTask = modal?.type === 'edit' ? tasks.find((task) => task.id === modal.id) : null
  const deletingTask = modal?.type === 'delete' ? tasks.find((task) => task.id === modal.id) : null

  return (
    <div className="app">
      <Sidebar
        active={activeNav}
        onNavigate={navigate}
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed(!collapsed)}
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      />
      {drawerOpen && <div className="drawer-overlay" onClick={() => setDrawerOpen(false)} />}

      <div className="main">
        <TopBar
          title={activeNav}
          search={search}
          onSearchChange={setSearch}
          onNewTask={() => setModal({ type: 'create' })}
          onOpenMenu={() => setDrawerOpen(true)}
        />

        <main className="content">
          {warning && (
            <StorageBanner warning={warning} onReset={handleResetStorage} onDismiss={() => setWarning(null)} />
          )}
          <SummaryCards tasks={tasks} />
          <TaskToolbar
            search={search}
            onSearchChange={setSearch}
            status={statusFilter}
            onStatusChange={setStatusFilter}
            priority={priorityFilter}
            onPriorityChange={setPriorityFilter}
            sort={sort}
            onSortChange={setSort}
            onClear={clearFilters}
          />
          <TaskList
            totalCount={tasks.length}
            tasks={visibleTasks}
            search={search}
            today={todayString()}
            onEdit={(id) => setModal({ type: 'edit', id })}
            onDelete={(id) => setModal({ type: 'delete', id })}
            onStatusChange={changeStatus}
            onCreate={() => setModal({ type: 'create' })}
            onClearSearch={() => setSearch('')}
            onClearFilters={clearFilters}
          />
        </main>
      </div>

      {modal?.type === 'create' && <TaskFormModal onSave={createTask} onClose={closeModal} />}
      {editingTask && (
        <TaskFormModal
          key={editingTask.id}
          task={editingTask}
          onSave={(values) => updateTask(editingTask.id, values)}
          onClose={closeModal}
        />
      )}
      {deletingTask && (
        <ConfirmDeleteModal task={deletingTask} onConfirm={() => deleteTask(deletingTask.id)} onClose={closeModal} />
      )}

      {toast && <Toast key={toast.key} message={toast.message} type={toast.type} onClose={dismissToast} />}
    </div>
  )
}
