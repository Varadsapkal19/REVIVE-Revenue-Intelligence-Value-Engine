'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard, AlertTriangle, FileText, Play,
  FlaskConical, Shield, BookOpen, Scale
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { name: 'Overview',        href: '/dashboard',      icon: LayoutDashboard },
  { name: 'Revenue Risk',    href: '/revenue-risk',   icon: AlertTriangle },
  { name: 'Recovery Cases',  href: '/cases',          icon: FileText },
  { name: 'Simulator',       href: '/simulator',      icon: Play },
  { name: 'Experiments',     href: '/experiments',    icon: FlaskConical },
  { name: 'Policies',        href: '/policies',       icon: Shield },
  { name: 'Audit Log',       href: '/audit',          icon: BookOpen },
  { name: 'Judge Mode',      href: '/judge-mode',     icon: Scale },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-60 bg-neutral-900 h-screen flex flex-col text-neutral-200 shrink-0">
      {/* Logo */}
      <div className="p-4 flex items-center gap-3 border-b border-neutral-800">
        <img
          src="/logo.jpg"
          alt="REVIVE Logo"
          className="w-10 h-10 object-contain rounded-lg shadow-md border border-neutral-800"
        />
        <div>
          <h1 className="font-bold text-white text-base tracking-tight leading-none">REVIVE</h1>
          <p className="text-xs text-neutral-500 mt-0.5">Recovery Intelligence</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-3 overflow-y-auto">
        <p className="px-4 py-2 text-[10px] uppercase tracking-widest text-neutral-600 font-semibold">
          Navigation
        </p>
        <ul className="space-y-0.5 px-2">
          {navItems.map(item => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150',
                    isActive
                      ? 'bg-brand text-white shadow-sm'
                      : 'text-neutral-400 hover:bg-neutral-800 hover:text-neutral-100'
                  )}
                >
                  <item.icon className={cn('w-4 h-4 shrink-0', isActive ? 'text-white' : 'text-neutral-500')} />
                  {item.name}
                  {item.name === 'Judge Mode' && (
                    <span className="ml-auto text-[10px] bg-brand-700 text-brand-100 px-1.5 py-0.5 rounded font-bold tracking-wide">
                      ⭐
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-neutral-800">
        <div className="text-xs text-neutral-600 space-y-1">
          <p className="font-mono">v1.0.0 · Production</p>
        </div>
      </div>
    </div>
  );
}
