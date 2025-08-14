import React from 'react'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'gradient'
}

export default function Button({ variant='primary', className='', ...props }: Props) {
  const base = 'relative overflow-hidden inline-flex items-center justify-center rounded-lg px-4 py-2 transition active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed'
  const styles = {
    primary: 'bg-indigo-600 text-white hover:bg-indigo-700 shadow',
    secondary: 'bg-white text-indigo-700 border border-indigo-200 hover:bg-indigo-50',
    ghost: 'bg-transparent text-indigo-700 hover:bg-indigo-50',
    gradient: 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow hover:opacity-95',
  }[variant]
  return (
    <button className={`${base} ${styles} ${className}`} {...props}>
      <span className="relative z-10">{props.children}</span>
      {variant==='gradient' && (
        <span className="absolute inset-0 -translate-x-full bg-white/30 [mask-image:linear-gradient(90deg,transparent,white,transparent)] animate-[shine_2.2s_ease-in-out_infinite]"></span>
      )}
    </button>
  )
}

