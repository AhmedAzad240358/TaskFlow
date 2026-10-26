import { ChevronsLeft, ChevronsRight, CheckCheck, CircleCheck, Circle, Clock, LayoutDashboard, ListChecks, User, X } from 'lucide-react'

const NAV_ITEMS = [
  { label: 'Dashboard', icon: LayoutDashboard },
  { label: 'All Tasks', icon: ListChecks },
  { label: 'To Do', icon: Circle },
  { label: 'In Progress', icon: Clock },
  { label: 'Completed', icon: CircleCheck },
]

// Desktop: always visible, can shrink to icons. Mobile (under 768px): a drawer opened by the hamburger.
export default function Sidebar({ active, onNavigate, collapsed, onToggleCollapse, open, onClose }) {
  const className = ['sidebar', collapsed && 'collapsed', open && 'open'].filter(Boolean).join(' ')

  return (
    <aside className={className}>
      <div className="sidebar-header">
        <span className="logo" aria-hidden="true">
          <CheckCheck size={20} />
        </span>
        <span className="brand-name">TaskFlow</span>
        <button type="button" className="icon-button sidebar-close" aria-label="Close menu" onClick={onClose}>
          <X size={20} aria-hidden="true" />
        </button>
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        {NAV_ITEMS.map(({ label, icon: Icon }) => (
          <button
            key={label}
            type="button"
            className={label === active ? 'nav-item active' : 'nav-item'}
            aria-current={label === active ? 'page' : undefined}
            aria-label={label}
            title={label}
            onClick={() => onNavigate(label)}
          >
            <Icon size={20} aria-hidden="true" />
            <span className="nav-label">{label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="profile">
          <span className="avatar" aria-hidden="true">
            <User size={18} />
          </span>
          <div className="profile-text">
            <p className="profile-name">TaskFlow User</p>
            <p className="profile-note">Personal workspace</p>
          </div>
        </div>
        <button
          type="button"
          className="icon-button collapse-button"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          aria-expanded={!collapsed}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          onClick={onToggleCollapse}
        >
          {collapsed ? <ChevronsRight size={20} aria-hidden="true" /> : <ChevronsLeft size={20} aria-hidden="true" />}
        </button>
      </div>
    </aside>
  )
}
