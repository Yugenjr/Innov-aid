import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'

export default function Investment() {
  const [form, setForm] = useState({
    initial_investment: 1000,
    monthly_investment: 300,
    annual_return_pct: 7,
    years: 20,
  })

  const mutation = useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/api/invest/calc', form)
      return data as { total_future_value: number, total_invested: number, total_gains: number }
    }
  })

  return (
    <div className="space-y-4">
      <div className="relative overflow-hidden rounded-xl p-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow">
        <h1 className="text-2xl font-bold">Investment Guide</h1>
        <p className="text-white/90 text-sm">Project your portfolio growth and understand risk profiles.</p>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Card className="space-y-3">
          {Object.entries(form).map(([k,v]) => (
            <label key={k} className="flex items-center gap-2">
              <span className="w-56 capitalize">{k.replace('_',' ')}</span>
              <input type={k==='years' ? 'number' : 'number'} className="border rounded px-2 py-1 flex-1" value={v as number}
                onChange={e => setForm(prev => ({...prev, [k]: Number(e.target.value)}))} />
            </label>
          ))}
          <Button variant="gradient" onClick={() => mutation.mutate()}>Calculate</Button>
        </Card>
        <Card>
          {mutation.data ? (
            <div className="grid grid-cols-3 gap-3 text-center animate-fade-up">
              <div>
                <div className="text-sm text-gray-500">Total Future Value</div>
                <div className="text-lg font-semibold">${mutation.data.total_future_value.toLocaleString(undefined,{maximumFractionDigits:2})}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total Invested</div>
                <div className="text-lg font-semibold">${mutation.data.total_invested.toLocaleString(undefined,{maximumFractionDigits:2})}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total Gains</div>
                <div className="text-lg font-semibold">${mutation.data.total_gains.toLocaleString(undefined,{maximumFractionDigits:2})}</div>
              </div>
            </div>
          ) : (
            <div className="text-gray-500">Enter parameters and calculate to see results.</div>
          )}
        </Card>
      </div>

      <Card>
        <h2 className="font-semibold mb-2">Risk Assessment (Guidance)</h2>
        <ul className="list-disc ml-6 text-sm text-gray-700 space-y-1">
          <li>Very Conservative: 70% Bonds, 30% Stocks</li>
          <li>Moderate: 60% Stocks, 40% Bonds</li>
          <li>Aggressive: 80% Stocks, 20% Bonds</li>
        </ul>
        <p className="text-xs text-gray-500 mt-2">Educational only, not financial advice.</p>
      </Card>
    </div>
  )
}

