import { useEffect, useRef, useState } from 'react'
import { api } from '../api/client'
import Button from '../components/Button'
import Card from '../components/Card'

export default function Speech() {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const [chunks, setChunks] = useState<Blob[]>([])
  const [recording, setRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [ttsAudio, setTtsAudio] = useState<string | null>(null)

  useEffect(() => {
    return () => { if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') mediaRecorderRef.current.stop() }
  }, [])

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const rec = new MediaRecorder(stream)
    setChunks([])
    rec.ondataavailable = (e) => setChunks(prev => [...prev, e.data])
    rec.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' })
      const form = new FormData()
      form.append('file', blob, 'audio.webm')
      const { data } = await api.post('/api/speech/transcribe', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      setTranscript(data.text || '')
    }
    mediaRecorderRef.current = rec
    rec.start()
    setRecording(true)
  }
  const stop = () => {
    mediaRecorderRef.current?.stop()
    setRecording(false)
  }

  const speak = async () => {
    if (!transcript.trim()) return
    const chat = await api.post('/api/chat', { user_input: transcript, user_mode: 'professional' })
    const answer = chat.data.response
    const { data } = await api.post('/api/speech/tts', { text: answer })
    setTtsAudio(`data:audio/mp3;base64,${data.audio_base64}`)
  }

  return (
    <div className="space-y-4 max-w-3xl mx-auto">
      <div className="relative overflow-hidden rounded-xl p-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow">
        <h1 className="text-2xl font-bold">Speech-to-Speech</h1>
        <p className="text-white/90 text-sm">Record your voice, get an AI answer, and hear it back.</p>
      </div>
      <Card className="space-y-3">
        <div className="flex flex-wrap gap-2">
          {!recording ? (
            <Button variant="gradient" onClick={start}>Start Recording</Button>
          ) : (
            <Button variant="gradient" onClick={stop}>Stop</Button>
          )}
          <Button onClick={speak}>Ask &amp; Speak</Button>
        </div>
        <div>
          <div className="text-sm text-gray-500">Transcript</div>
          <textarea className="w-full border rounded p-2" rows={4} value={transcript} onChange={e => setTranscript(e.target.value)} />
        </div>
        {ttsAudio && (
          <audio src={ttsAudio} controls autoPlay className="w-full" />
        )}
      </Card>
    </div>
  )
}

