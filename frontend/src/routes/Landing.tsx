import { Link } from 'react-router-dom'
import Button from '../components/Button'

export default function Landing() {
  return (
    <div className="relative overflow-hidden">
      {/* Background gradient and glow */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-50 via-white to-purple-50" />
      <div className="absolute -z-10 top-1/3 -left-20 w-96 h-96 bg-purple-200/60 blur-3xl rounded-full" />
      <div className="absolute -z-10 bottom-1/4 -right-20 w-96 h-96 bg-indigo-200/60 blur-3xl rounded-full" />

      {/* Hero */}
      <section className="container mx-auto px-4 py-20 grid md:grid-cols-2 gap-8 items-center">
        <div className="animate-fade-up" style={{animationDelay: '40ms'}}>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight">
            Personal Finance, Reinvented
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Meet your AI-powered money coach. Master budgeting, saving, and investing with a delightful, conversational experience.
          </p>
          <div className="mt-8 flex gap-3">
            <Button as-child variant="gradient"><Link to="/signin">Get Started</Link></Button>
            <a href="#features" className="px-5 py-3 rounded-lg border border-gray-300 hover:bg-gray-50 transition">Learn more</a>
          </div>
        </div>
        <div className="relative animate-fade-up" style={{animationDelay: '120ms'}}>
          <div className="relative bg-white/70 backdrop-blur rounded-2xl shadow-xl p-6 border overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/10 to-purple-600/10" />
            <div className="relative">
              <div className="text-sm text-gray-500">Live Preview</div>
              <div className="mt-2 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 p-4 text-white shadow-inner">
                <p className="opacity-90">"How do I start investing with $200 per month?"</p>
                <div className="mt-3 p-3 bg-white/10 rounded">
                  <p>Start with a simple 80/20 stock-bond mix via low-fee index funds. Automate monthly contributions.</p>
                </div>
              </div>
            </div>
            {/* Shine */}
            <div className="pointer-events-none absolute -inset-x-1 -top-1/2 h-full bg-gradient-to-b from-white/40 to-transparent blur-2xl" />
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container mx-auto px-4 py-16 grid md:grid-cols-3 gap-6">
        {[
          { title: 'Smart Chatbot', desc: 'Context-aware guidance for students and professionals.' },
          { title: 'Budgeting Superpowers', desc: '50/30/20 rule comparisons and spending visuals.' },
          { title: 'Voice Ready', desc: 'Speak naturally. Get real-time answers with voice.' },
        ].map((f, i) => (
          <div key={i} className="bg-white rounded-xl p-6 shadow hover:shadow-xl hover:-translate-y-0.5 transition border animate-fade-up" style={{animationDelay: `${(i+1)*60}ms`}}>
            <div className="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 grid place-items-center font-bold">{i+1}</div>
            <h3 className="mt-4 text-xl font-semibold">{f.title}</h3>
            <p className="text-gray-600 mt-1">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* Logos / social proof */}
      <section className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-500 text-sm mb-4">Trusted by builders and learners from</div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 opacity-70">
          {['Alpha','Nova','Vertex','Pioneer','Orbit'].map((n,i)=>(
            <div key={i} className="h-12 rounded bg-white grid place-items-center shadow-sm animate-fade-in" style={{animationDelay: `${(i+1)*40}ms`}}>
              <span className="text-gray-400 font-semibold">{n}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-3xl md:text-4xl font-extrabold">Take control of your money today</h2>
        <p className="text-gray-600 mt-2">Join early adopters building wealth with confidence.</p>
        <Button variant="gradient" className="mt-6"><Link to="/signin">Sign In</Link></Button>
      </section>
    </div>
  )
}

