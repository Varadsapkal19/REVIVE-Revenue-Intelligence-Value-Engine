import './globals.css'
import { AppLayout } from '@/components/layout/AppLayout'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'REVIVE — Revenue Recovery Intelligence',
  description: 'Autonomous Revenue Recovery Intelligence & Value Engine',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased bg-neutral-50">
        <AppLayout>{children}</AppLayout>
      </body>
    </html>
  )
}
