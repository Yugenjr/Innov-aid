import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../api/client'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis } from 'recharts'
import Button from '../components/Button'
import Card from '../components/Card'

export default function Budget() {
  const [form, setForm] = useState({
    monthly_income: 3000,
    rent: 1000,
    utilities: 150,
    insurance: 200,
    food: 400,
    transportation: 300,
    entertainment: 200,
    other: 150,
  })

  const mutation = useMutation({
    mutationFn: async () => {
      const { data } = await api.post('/api/budget/analyze', form)
      return data as any
    },
  })

  const colors = ['#6366f1','#22c55e','#ef4444','#f59e0b','#06b6d4','#a78bfa','#64748b']

  const submit = () => mutation.mutate()

  return (
    <div className="space-y-4">
      <div className="relative overflow-hidden rounded-xl p-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow">
        <h1 className="text-2xl font-bold">Budget Tracker</h1>
        <p className="text-white/90 text-sm">Analyze your monthly cashflow and compare against the 50/30/20 rule.</p>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Card className="space-y-3">
          <h2 className="font-semibold">Inputs</h2>
          {Object.entries(form).map(([k,v]) => (
            <label key={k} className="flex items-center gap-2">
              <span className="w-48 capitalize">{k.replace('_',' ')}</span>
              <input type="number" className="border rounded px-2 py-1 flex-1" value={v as number}
                onChange={e => setForm(prev => ({...prev, [k]: Number(e.target.value)}))} />
            </label>
          ))}
          <Button variant="gradient" onClick={submit}>Analyze</Button>
        </Card>
        <Card>
          {mutation.data ? (
            <div className="space-y-4 animate-fade-up">
              <div className="grid grid-cols-3 gap-3 text-center">
                <div>
                  <div className="text-sm text-gray-500">Income</div>
                  <div className="text-lg font-semibold">${form.monthly_income.toLocaleString()}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Expenses</div>
                  <div className="text-lg font-semibold">${mutation.data.total_expenses.toLocaleString(undefined, {maximumFractionDigits:2})}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Remaining</div>
                  <div className={`text-lg font-semibold ${mutation.data.remaining>=0?'text-emerald-600':'text-rose-600'}`}>
                    ${mutation.data.remaining.toLocaleString(undefined, {maximumFractionDigits:2})}
                  </div>
                </div>
              </div>

              <div className="h-64">
                <ResponsiveContainer>
                  <PieChart>
                    <Pie data={Object.entries(mutation.data.breakdown).map(([name, amount]) => ({name, value: amount}))} dataKey="value" nameKey="name" outerRadius={80}>
                      {Object.entries(mutation.data.breakdown).map((_, i) => (
                        <Cell key={i} fill={colors[i % colors.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="h-64">
                <ResponsiveContainer>
                  <BarChart data={["Needs","Wants","Savings"].map(cat => ({
                    category: cat,
                    Target: mutation.data.rule_50_30_20[cat].target,
                    Actual: mutation.data.rule_50_30_20[cat].actual,
                  }))}>
                    <XAxis dataKey="category" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="Target" fill="#94a3b8" />
                    <Bar dataKey="Actual" fill="#6366f1" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          ) : (
            <div className="text-gray-500">Fill inputs and click Analyze to see results.</div>
          )}
        </Card>
      </div>
    </div>
  )
}

