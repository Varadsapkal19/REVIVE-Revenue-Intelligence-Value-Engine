import { Search, Bell, User } from 'lucide-react'

export function TopBar() {
  return (
    <div className="h-16 bg-white border-b border-neutral-200 flex items-center justify-between px-6">
      <div className="flex-1 max-w-md relative">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
        <input 
          type="text" 
          placeholder="Search cases, customers..." 
          className="w-full pl-10 pr-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent"
        />
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-warning-light text-warning-dark px-3 py-1 rounded-full text-xs font-semibold border border-warning">
          <span className="w-2 h-2 rounded-full bg-brand animate-pulse"></span>
          TEST MODE
        </div>
        <button className="text-neutral-500 hover:text-neutral-900 relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-danger rounded-full"></span>
        </button>
        <button className="w-8 h-8 rounded-full bg-neutral-200 flex items-center justify-center text-neutral-700">
          <User className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
