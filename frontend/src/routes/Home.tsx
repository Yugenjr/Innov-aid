export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Personal Finance App</h1>
      <p className="text-gray-600">Welcome! Explore the Chatbot, and soon Budget, Savings, Investments, and Speech features.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded-lg shadow">
          <h2 className="font-semibold mb-2">💬 Finance Chatbot</h2>
          <p>Ask questions about budgeting, investing, and more.</p>
        </div>
        <div className="p-4 bg-white rounded-lg shadow opacity-70">
          <h2 className="font-semibold mb-2">📊 Budget Tracker</h2>
          <p>Coming soon: analyze spending and 50/30/20 rule.</p>
        </div>
      </div>
    </div>
  )
}

