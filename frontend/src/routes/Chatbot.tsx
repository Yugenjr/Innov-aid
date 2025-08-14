import { useMemo, useRef, useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'

const scenarios = [
  'Build an emergency fund',
  'Pay off credit card debt',
  'Invest $200 per month',
  'Improve my credit score',
]

type Message = {
  role: 'user' | 'assistant'
  content: string
  provider?: string
  error?: boolean
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [mode, setMode] = useState<'student' | 'professional'>('professional')
  const [mountAnim, setMountAnim] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => { const t = setTimeout(()=>setMountAnim(true), 10); return () => clearTimeout(t) }, [])

  const chatMutation = useMutation({
    mutationFn: async (payload: { user_input: string, user_mode: string, scenario_context?: string }) => {
      const { data } = await api.post('/api/chat', payload)
      return data as { response: string, provider?: string, used_fallback?: boolean }
    },
    onSuccess: (data) => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        provider: data.provider
      }])
      setTimeout(() => scrollRef.current?.scrollIntoView({ behavior: 'smooth' }), 10)
    },
    onError: (error: any) => {
      console.error('Chat API Error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        error: true
      }])
      setTimeout(() => scrollRef.current?.scrollIntoView({ behavior: 'smooth' }), 10)
    }
  })

  const send = (override?: string) => {
    const text = (override ?? input).trim()
    if (!text) return
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')
    setTimeout(() => scrollRef.current?.scrollIntoView({ behavior: 'smooth' }), 10)
    chatMutation.mutate({ user_input: text, user_mode: mode })
  }

  const formatResponse = (content: string) => {
    // Split content into paragraphs and format lists
    const paragraphs = content.split('\n').filter(p => p.trim())

    return paragraphs.map((paragraph, index) => {
      // Check if it's a numbered list item
      if (/^\d+\./.test(paragraph.trim())) {
        return (
          <div key={index} className="mb-2">
            <span className="font-semibold text-indigo-600">{paragraph.match(/^\d+\./)?.[0]}</span>
            <span className="ml-2">{paragraph.replace(/^\d+\.\s*/, '')}</span>
          </div>
        )
      }
      // Check if it's a bullet point
      else if (/^[•\-\*]/.test(paragraph.trim())) {
        return (
          <div key={index} className="mb-2 ml-4">
            <span className="text-indigo-600 mr-2">•</span>
            <span>{paragraph.replace(/^[•\-\*]\s*/, '')}</span>
          </div>
        )
      }
      // Regular paragraph
      else {
        return (
          <p key={index} className="mb-2">
            {paragraph}
          </p>
        )
      }
    })
  }

  const header = useMemo(() => (
    <div className={`relative overflow-hidden rounded-xl p-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow transform transition ${mountAnim ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
      <div className="absolute -top-8 -right-8 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
      <div className="absolute -bottom-8 -left-8 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
      <div className="relative flex items-center justify-between">
        <h1 className="text-2xl font-bold">Your AI Finance Coach</h1>
        <select value={mode} onChange={e => setMode(e.target.value as any)} className="text-indigo-700 bg-white px-2 py-1 rounded">
          <option value="student">Student</option>
          <option value="professional">Professional</option>
        </select>
      </div>
      <p className="mt-1 text-white/90 text-sm">Ask anything about budgeting, saving, investing, debt, taxes, and more.</p>
    </div>
  ), [mode, mountAnim])

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      {header}

      <div className={`flex flex-wrap gap-2 transform transition ${mountAnim ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}`}>
        {scenarios.map(s => (
          <button key={s} onClick={() => send(s)} className="px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200 text-sm transition">
            {s}
          </button>
        ))}
      </div>

      <Card className={`rounded-2xl h-[60vh] overflow-y-auto space-y-3 ${mountAnim ? 'opacity-100' : 'opacity-0'} transition`}>
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-10">Start with a quick scenario or ask your own question.</div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-up`} style={{animationDelay: `${i*40}ms`}}>
            <div className={`max-w-[75%] px-4 py-3 rounded-2xl shadow-sm transition-transform ${
              m.role === 'user'
                ? 'bg-indigo-600 text-white rounded-br-sm'
                : m.error
                  ? 'bg-red-50 border border-red-200 text-red-800 rounded-bl-sm'
                  : 'bg-gray-50 border border-gray-200 rounded-bl-sm'
            }`}>
              {m.role === 'user' ? (
                <div>{m.content}</div>
              ) : (
                <div>
                  {m.error ? (
                    <div className="flex items-center gap-2">
                      <span className="text-red-500">⚠️</span>
                      <span>{m.content}</span>
                    </div>
                  ) : (
                    <div>
                      {formatResponse(m.content)}
                      {m.provider && (
                        <div className="mt-2 pt-2 border-t border-gray-200 text-xs text-gray-500">
                          Powered by {m.provider === 'granite' ? 'Granite AI' : m.provider === 'gemini' ? 'Gemini AI' : 'Rule-based system'}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {chatMutation.isPending && (
          <div className="flex justify-start animate-fade-up">
            <div className="max-w-[75%] px-4 py-3 rounded-2xl bg-gray-50 border border-gray-200 rounded-bl-sm">
              <div className="flex items-center gap-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce [animation-delay:150ms]"></span>
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce [animation-delay:300ms]"></span>
                </div>
                <span className="text-gray-600 text-sm">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </Card>

      <div className="sticky bottom-4">
        <div className="bg-white rounded-full shadow-lg border flex items-center p-2 gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send()}
            placeholder="Ask about budgeting, investing, credit…"
            className="flex-1 outline-none px-3 py-2"
            disabled={chatMutation.isPending}
          />
          <Button
            onClick={() => send()}
            className="rounded-full"
            disabled={chatMutation.isPending || !input.trim()}
          >
            {chatMutation.isPending ? 'Sending...' : 'Send'}
          </Button>
        </div>
      </div>
    </div>
  )
}

