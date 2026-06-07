import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Request failed'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default api

// Chat API
export const chatApi = {
  sendMessage: (data: { content: string; session_id?: string; model?: string }): Promise<{ message: any; session: any }> =>
    api.post('/chat/send', data),

  getHistory: (sessionId: string): Promise<{ session_id: string; messages: any[] }> =>
    api.get(`/chat/history/${sessionId}`),

  createSession: (data?: { title?: string; model?: string }): Promise<any> =>
    api.post('/chat/session', data),

  deleteSession: (sessionId: string): Promise<any> =>
    api.delete(`/chat/session/${sessionId}`),

  listSessions: (): Promise<{ sessions: any[] }> =>
    api.get('/chat/sessions'),

  listModels: (): Promise<any[]> =>
    api.get('/chat/models'),

  downloadModel: (modelName: string): Promise<any> =>
    api.post('/chat/models/download', null, { params: { model_name: modelName } })
}

// Media API
export const mediaApi = {
  textToSpeech: (data: { text: string; lang?: string; speed?: number }) =>
    api.post('/media/tts', data),

  speechToText: (formData: FormData) =>
    api.post('/media/asr', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  ocrRecognize: (formData: FormData) =>
    api.post('/media/ocr', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  audioDenoise: (formData: FormData) =>
    api.post('/media/denoise', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  generateImage: (data: { prompt: string; negative_prompt?: string; width?: number; height?: number }) =>
    api.post('/media/image/generate', null, { params: data }),

  getTaskStatus: (taskId: string) =>
    api.get(`/media/tasks/${taskId}`)
}

// Office API
export const officeApi = {
  pdfSplit: (formData: FormData) =>
    api.post('/office/pdf/split', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  pdfMerge: (formData: FormData) =>
    api.post('/office/pdf/merge', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  pdfEncrypt: (formData: FormData) =>
    api.post('/office/pdf/encrypt', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  pdfDecrypt: (formData: FormData) =>
    api.post('/office/pdf/decrypt', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  pdfConvert: (formData: FormData, targetFormat: string = 'images') =>
    api.post('/office/pdf/convert', formData, { params: { target_format: targetFormat } }),

  pdfSummary: (formData: FormData, maxLength: number = 500) =>
    api.post('/office/pdf/summary', formData, { params: { max_length: maxLength } }),

  docxProcess: (formData: FormData) =>
    api.post('/office/docx/process', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),

  excelProcess: (formData: FormData) =>
    api.post('/office/excel/process', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
}

// Code API
export const codeApi = {
  generate: (data: { prompt: string; language: string; context?: string }) =>
    api.post('/code/generate', data),

  fix: (data: { code: string; language: string; error_message?: string }) =>
    api.post('/code/fix', data),

  comment: (data: { code: string; language: string }) =>
    api.post('/code/comment', data),

  optimize: (data: { code: string; language: string }) =>
    api.post('/code/optimize', data),

  scaffold: (data: { project_type: string; project_name: string; requirements?: string[] }) =>
    api.post('/code/scaffold', data),

  debugApi: (data: { method: string; url: string; headers?: object; params?: object; body?: object }) =>
    api.post('/code/debug', data)
}

// Plugins API
export const pluginsApi = {
  list: () =>
    api.get('/plugins'),

  listMarket: () =>
    api.get('/plugins/market'),

  get: (pluginId: string) =>
    api.get(`/plugins/${pluginId}`),

  install: (pluginId: string, version?: string) =>
    api.post('/plugins/install', null, { params: { plugin_id: pluginId, version } }),

  uninstall: (pluginId: string) =>
    api.post('/plugins/uninstall', null, { params: { plugin_id: pluginId } }),

  enable: (pluginId: string) =>
    api.post(`/plugins/enable/${pluginId}`),

  disable: (pluginId: string) =>
    api.post(`/plugins/disable/${pluginId}`)
}
