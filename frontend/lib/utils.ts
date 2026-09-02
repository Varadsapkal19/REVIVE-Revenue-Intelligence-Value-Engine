import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount)
}

export function formatLakhs(amount: number): string {
  if (amount >= 100000) {
    const lakhs = amount / 100000
    return `₹${lakhs.toFixed(1)}L`
  }
  return formatCurrency(amount)
}

export function getPriorityColor(priority: string): string {
  switch (priority.toLowerCase()) {
    case 'critical': return 'text-danger dark:text-danger-light'
    case 'high': return 'text-brand dark:text-brand-light'
    case 'medium': return 'text-warning dark:text-warning-light'
    default: return 'text-neutral-700 dark:text-neutral-200'
  }
}

export function getRootCauseLabel(rootCause: string): string {
  return rootCause.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

export function getActionLabel(action: string): string {
  return action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

export function getStatusBadgeClass(status: string): string {
  switch (status.toLowerCase()) {
    case 'authorized':
    case 'recovered':
      return 'bg-success-light text-success-dark border-success'
    case 'blocked':
    case 'failed':
      return 'bg-danger-light text-danger-dark border-danger'
    case 'pending':
    case 'processing':
      return 'bg-warning-light text-warning-dark border-warning'
    default:
      return 'bg-neutral-100 text-neutral-700 border-neutral-200'
  }
}
