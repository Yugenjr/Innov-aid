import React, { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { fraudAPI, FraudDetectionResponse } from '../api/client'

const FraudDetection: React.FC = () => {
  const [content, setContent] = useState('')
  const [analysisType, setAnalysisType] = useState<'general' | 'financial'>('general')
  const [result, setResult] = useState<FraudDetectionResponse | null>(null)

  const fraudMutation = useMutation({
    mutationFn: (data: { content: string; type: 'general' | 'financial' }) => {
      if (data.type === 'financial') {
        return fraudAPI.analyzeFinancial(data.content)
      } else {
        return fraudAPI.detectFraud(data.content, data.type)
      }
    },
    onSuccess: (data) => {
      setResult(data)
    },
    onError: (error) => {
      console.error('Fraud detection error:', error)
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (content.trim()) {
      fraudMutation.mutate({ content: content.trim(), type: analysisType })
    }
  }

  const handleClear = () => {
    setContent('')
    setResult(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔒 FraudAwarenessGPT
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI-powered fraud detection to protect you from scams, phishing, and financial fraud.
            Paste suspicious content below for analysis.
          </p>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Analysis Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Analysis Type
              </label>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="general"
                    checked={analysisType === 'general'}
                    onChange={(e) => setAnalysisType(e.target.value as 'general')}
                    className="mr-2 text-red-600"
                  />
                  <span className="text-sm">General Scam Detection</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="financial"
                    checked={analysisType === 'financial'}
                    onChange={(e) => setAnalysisType(e.target.value as 'financial')}
                    className="mr-2 text-red-600"
                  />
                  <span className="text-sm">Financial Fraud Analysis</span>
                </label>
              </div>
            </div>

            {/* Content Input */}
            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                Suspicious Content to Analyze
              </label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste emails, messages, investment offers, or any suspicious content here..."
                className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 resize-none"
                required
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                type="submit"
                disabled={fraudMutation.isPending || !content.trim()}
                className="flex-1 bg-red-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {fraudMutation.isPending ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Analyzing...
                  </span>
                ) : (
                  '🔍 Analyze for Fraud'
                )}
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              🛡️ Analysis Results
            </h2>
            
            {/* Detection Status */}
            <div className={`p-4 rounded-lg mb-4 ${
              result.detected_content === 'None' || result.detected_content === 'No scam detected.' 
                ? 'bg-green-50 border border-green-200' 
                : 'bg-red-50 border border-red-200'
            }`}>
              <div className="flex items-start gap-3">
                <div className="text-2xl">
                  {result.detected_content === 'None' || result.detected_content === 'No scam detected.' ? '✅' : '⚠️'}
                </div>
                <div>
                  <h3 className={`font-semibold ${
                    result.detected_content === 'None' || result.detected_content === 'No scam detected.'
                      ? 'text-green-800' 
                      : 'text-red-800'
                  }`}>
                    {result.detected_content === 'None' || result.detected_content === 'No scam detected.'
                      ? 'No Fraud Detected' 
                      : 'Potential Fraud Detected'}
                  </h3>
                  <p className={`mt-1 ${
                    result.detected_content === 'None' || result.detected_content === 'No scam detected.'
                      ? 'text-green-700' 
                      : 'text-red-700'
                  }`}>
                    {result.detected_content}
                  </p>
                </div>
              </div>
            </div>

            {/* Awareness Message */}
            <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg mb-4">
              <h4 className="font-semibold text-blue-800 mb-2">💡 Awareness Message</h4>
              <p className="text-blue-700">{result.awareness_message}</p>
            </div>

            {/* Technical Details */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-800 mb-2">🔧 Analysis Details</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Provider:</span>
                  <span className="ml-2 font-medium">{result.provider}</span>
                </div>
                <div>
                  <span className="text-gray-600">Model:</span>
                  <span className="ml-2 font-medium">{result.model}</span>
                </div>
                <div>
                  <span className="text-gray-600">Analysis Type:</span>
                  <span className="ml-2 font-medium capitalize">{result.analysis_type}</span>
                </div>
                <div>
                  <span className="text-gray-600">Status:</span>
                  <span className={`ml-2 font-medium ${result.success ? 'text-green-600' : 'text-red-600'}`}>
                    {result.success ? 'Success' : 'Failed'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {fraudMutation.isError && (
          <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
            <h4 className="font-semibold text-red-800 mb-2">❌ Error</h4>
            <p className="text-red-700">
              Failed to analyze content. Please try again or check your connection.
            </p>
          </div>
        )}

        {/* Tips */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-2xl">
          <h3 className="text-xl font-bold text-gray-900 mb-4">🛡️ Fraud Prevention Tips</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div>
              <h4 className="font-semibold mb-2">🚨 Red Flags to Watch For:</h4>
              <ul className="space-y-1">
                <li>• Urgent requests for money or personal info</li>
                <li>• Too-good-to-be-true investment offers</li>
                <li>• Requests to send money via wire transfer</li>
                <li>• Poor grammar and spelling in official emails</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">✅ Stay Safe:</h4>
              <ul className="space-y-1">
                <li>• Verify sender identity independently</li>
                <li>• Never share passwords or PINs</li>
                <li>• Research investment opportunities thoroughly</li>
                <li>• Trust your instincts - if it feels wrong, it probably is</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FraudDetection
