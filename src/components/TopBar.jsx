import { Menu, Search } from 'lucide-react'
import { formatToday } from '../utils/dates'

export default function TopBar({ title, search, onSearchChange, onNewTask, onOpenMenu }) {
  return (
    <header className="topbar">
      <button type="button" className="icon-button menu-button" aria-label="Open menu" onClick={onOpenMenu}>
        <Menu size={22} aria-hidden="true" />
      </button>
      <div className="topbar-title">
        <h1>{title}</h1>
        <p className="current-date">{formatToday()}</p>
      </div>
      <div className="topbar-search">
        <Search size={18} aria-hidden="true" />
        <input
          id="topbar-search"
          type="search"
          placeholder="Search tasks..."
          aria-label="Search tasks"
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
        />
      </div>
      <button type="button" className="button button-primary" onClick={onNewTask}>
        + New Task
      </button>
    </header>
  )
}
