import React from 'react'

type Props = React.PropsWithChildren<{ className?: string, title?: string, subtitle?: string }>

export default function Card({ className='', title, subtitle, children }: Props) {
  return (
    <div className={`bg-white rounded-xl shadow border ${className}`}>
      {(title || subtitle) && (
        <div className="px-4 pt-4">
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
          {subtitle && <p className="text-sm text-gray-500 -mt-1">{subtitle}</p>}
        </div>
      )}
      <div className="p-4">
        {children}
      </div>
    </div>
  )
}

