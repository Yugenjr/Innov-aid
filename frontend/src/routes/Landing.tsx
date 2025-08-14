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
              <div className="text-sm text-gray-500 mb-3">AI-Powered Financial Advice</div>

              {/* Chat Demo */}
              <div className="space-y-3">
                <div className="flex justify-end">
                  <div className="bg-indigo-600 text-white rounded-2xl rounded-br-sm px-4 py-2 max-w-xs">
                    "How should I budget as a college student?"
                  </div>
                </div>

                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 max-w-sm">
                    <div className="text-sm">
                      <div className="font-semibold text-indigo-600 mb-1">🎓 Student Budgeting Guide</div>
                      <div className="space-y-1 text-xs">
                        <div><span className="font-semibold">1.</span> Track expenses with apps like Mint</div>
                        <div><span className="font-semibold">2.</span> Follow 50/30/20 rule</div>
                        <div><span className="font-semibold">3.</span> Cook meals, buy used textbooks</div>
                      </div>
                      <div className="text-xs text-gray-500 mt-2 pt-1 border-t">
                        Powered by Granite AI
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {/* Shine */}
            <div className="pointer-events-none absolute -inset-x-1 -top-1/2 h-full bg-gradient-to-b from-white/40 to-transparent blur-2xl" />
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">Everything you need for financial success</h2>
          <p className="text-gray-600 mt-2">Comprehensive tools powered by AI to help you make smart money decisions</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: '🤖 AI Financial Advisor',
              desc: 'Get personalized advice from our AI chatbot. Switch between student and professional modes for tailored guidance.',
              link: '/chat'
            },
            {
              title: '📊 Budget Tracker',
              desc: 'Analyze your spending with the 50/30/20 rule. Visualize expenses with interactive charts and get actionable insights.',
              link: '/budget'
            },
            {
              title: '💰 Savings Goals',
              desc: 'Plan your savings journey with smart projections. Track progress and see exactly when you\'ll reach your goals.',
              link: '/savings'
            },
            {
              title: '📈 Investment Calculator',
              desc: 'Project portfolio growth with compound interest. Understand different risk profiles and investment strategies.',
              link: '/investment'
            },
            {
              title: '🎤 Voice Interface',
              desc: 'Speak naturally to get financial advice. Record questions and hear AI responses with speech-to-speech technology.',
              link: '/speech'
            },
            {
              title: '🔐 Smart Validation',
              desc: 'Enhanced form validation with real-time feedback. Secure authentication with loading states and error handling.',
              link: '/signin'
            },
          ].map((f, i) => (
            <Link key={i} to={f.link} className="group">
              <div className="bg-white rounded-xl p-6 shadow hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border group-hover:border-indigo-200 animate-fade-up h-full" style={{animationDelay: `${(i+1)*60}ms`}}>
                <div className="flex items-start gap-4">
                  <div className="text-2xl">{f.title.split(' ')[0]}</div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold group-hover:text-indigo-600 transition-colors">{f.title.substring(2)}</h3>
                    <p className="text-gray-600 mt-2 text-sm leading-relaxed">{f.desc}</p>
                    <div className="mt-3 text-indigo-600 text-sm font-medium group-hover:translate-x-1 transition-transform">
                      Try it now →
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
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

