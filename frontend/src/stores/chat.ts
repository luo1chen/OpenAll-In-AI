import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatApi } from '@/api'

export interface ChatMessage {
  id: string
  session_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  created_at: string
}

export interface ChatSession {
  id: string
  title: string
  model: string
  system_prompt?: string
  created_at: string
  updated_at: string
}

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const currentSessionId = ref<string | null>(null)
  const messages = ref<ChatMessage[]>([])
  const models = ref<any[]>([])
  const loading = ref(false)

  async function fetchSessions() {
    try {
      const res = await chatApi.listSessions()
      sessions.value = res.sessions
    } catch (error) {
      console.error('Failed to fetch sessions:', error)
    }
  }

  async function createSession(data?: { title?: string; model?: string }) {
    try {
      const res = await chatApi.createSession(data)
      sessions.value.unshift(res)
      currentSessionId.value = res.id
      messages.value = []
      return res
    } catch (error) {
      console.error('Failed to create session:', error)
      throw error
    }
  }

  async function deleteSession(sessionId: string) {
    try {
      await chatApi.deleteSession(sessionId)
      sessions.value = sessions.value.filter(s => s.id !== sessionId)
      if (currentSessionId.value === sessionId) {
        currentSessionId.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('Failed to delete session:', error)
      throw error
    }
  }

  async function fetchHistory(sessionId: string) {
    try {
      const res = await chatApi.getHistory(sessionId)
      messages.value = res.messages
      currentSessionId.value = sessionId
    } catch (error) {
      console.error('Failed to fetch history:', error)
      throw error
    }
  }

  async function sendMessage(content: string) {
    loading.value = true
    try {
      const res = await chatApi.sendMessage({
        content,
        session_id: currentSessionId.value || undefined
      })
      messages.value.push(res.message)
      if (res.session && !sessions.value.find(s => s.id === res.session.id)) {
        sessions.value.unshift(res.session)
      }
      currentSessionId.value = res.session.id
      return res
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchModels() {
    try {
      const res = await chatApi.listModels()
      models.value = res
    } catch (error) {
      console.error('Failed to fetch models:', error)
    }
  }

  async function downloadModel(modelName: string) {
    try {
      await chatApi.downloadModel(modelName)
    } catch (error) {
      console.error('Failed to download model:', error)
      throw error
    }
  }

  return {
    sessions,
    currentSessionId,
    messages,
    models,
    loading,
    fetchSessions,
    createSession,
    deleteSession,
    fetchHistory,
    sendMessage,
    fetchModels,
    downloadModel
  }
})
