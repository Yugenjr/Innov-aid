import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'

export default function Savings() {
  const [form, setForm] = useState({
    target_amount: 5000,
    current_amount: 500,
    monthly_contribution: 200,
  })

  const mutation = useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/api/savings/project', form)
      return data as { progress_pct: number, remaining: number, months_to_goal: number, projection_12mo: number[] }
    }
  })

  const submit = () => mutation.mutate()

  return (
    <div className="space-y-4">
      <div className="relative overflow-hidden rounded-xl p-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow">
        <h1 className="text-2xl font-bold">Savings Goals</h1>
        <p className="text-white/90 text-sm">Plan your path to targets and visualize monthly progress.</p>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Card className="space-y-3">
          {Object.entries(form).map(([k,v]) => (
            <label key={k} className="flex items-center gap-2">
              <span className="w-56 capitalize">{k.replace('_',' ')}</span>
              <input type="number" className="border rounded px-2 py-1 flex-1" value={v as number}
                onChange={e => setForm(prev => ({...prev, [k]: Number(e.target.value)}))} />
            </label>
          ))}
          <Button variant="gradient" onClick={submit}>Project</Button>
        </Card>
        <Card>
          {mutation.data ? (
            <div className="space-y-3 animate-fade-up">
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <div className="text-sm text-gray-500">Progress</div>
                  <div className="text-lg font-semibold">{mutation.data.progress_pct.toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Remaining</div>
                  <div className="text-lg font-semibold">${mutation.data.remaining.toLocaleString(undefined,{maximumFractionDigits:2})}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Months to goal</div>
                  <div className="text-lg font-semibold">{Number.isFinite(mutation.data.months_to_goal) ? mutation.data.months_to_goal.toFixed(1) : '—'}</div>
                </div>
              </div>
              <div>
                <h3 className="font-semibold mb-1">Next 12 months</h3>
                <ul className="grid grid-cols-2 gap-2 text-sm">
                  {mutation.data.projection_12mo.map((v, i) => (
                    <li key={i} className="flex justify-between border rounded px-2 py-1">
                      <span>Month {i+1}</span>
                      <span>${v.toLocaleString(undefined,{maximumFractionDigits:2})}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-1">Tips</h3>
                <ul className="list-disc ml-6 text-sm text-gray-700 space-y-1">
                  <li>Automate your savings contributions.</li>
                  <li>Increase contributions when income rises.</li>
                  <li>Review subscriptions and cut non-essentials.</li>
                  <li>Use high-yield accounts for emergency funds.</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="text-gray-500">Enter your goal and click Project.</div>
          )}
        </Card>
      </div>
    </div>
  )
}

