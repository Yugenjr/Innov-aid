import axios from 'axios'

export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 600000, // 10 minute timeout for AI model loading
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error)

    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      error.message = 'Unable to connect to the server. Please make sure the backend is running.'
    } else if (error.response?.status === 500) {
      error.message = 'Server error. Please try again later.'
    } else if (error.response?.status === 404) {
      error.message = 'API endpoint not found.'
    }

    return Promise.reject(error)
  }
)

// Type definitions
export interface ChatRequest {
  user_input: string
  scenario_context?: string
  user_mode?: string
}

export interface ChatResponse {
  response: string
  provider: string
  used_fallback: boolean
}

export interface FraudDetectionRequest {
  content: string
  analysis_type?: string
}

export interface FraudDetectionResponse {
  detected_content: string
  awareness_message: string
  provider: string
  model: string
  success: boolean
  analysis_type?: string
}

// API functions
export const chatAPI = {
  sendMessage: (data: ChatRequest): Promise<ChatResponse> =>
    api.post('/api/chat', data).then(res => res.data),
}

export const fraudAPI = {
  detectFraud: (content: string, analysisType: string = 'general'): Promise<FraudDetectionResponse> =>
    api.post('/api/fraud/detect', { content, analysis_type: analysisType }).then(res => res.data),

  analyzeFinancial: (content: string): Promise<FraudDetectionResponse> =>
    api.post('/api/fraud/analyze-financial', { content, analysis_type: 'financial' }).then(res => res.data),
}

