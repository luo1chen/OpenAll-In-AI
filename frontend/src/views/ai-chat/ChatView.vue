<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { marked } from 'marked'
import hljs from 'highlight.js'

const route = useRoute()
const chatStore = useChatStore()

const inputMessage = ref('')
const messageListRef = ref<HTMLElement | null>(null)
const selectedModel = ref('')

onMounted(async () => {
  await chatStore.fetchSessions()
  await chatStore.fetchModels()

  if (route.params.sessionId) {
    await chatStore.fetchHistory(route.params.sessionId as string)
  }
})

watch(() => route.params.sessionId, async (newId) => {
  if (newId) {
    await chatStore.fetchHistory(newId as string)
  }
})

watch(() => chatStore.messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

function scrollToBottom() {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

async function handleSend() {
  if (!inputMessage.value.trim() || chatStore.loading) return

  const message = inputMessage.value
  inputMessage.value = ''

  try {
    await chatStore.sendMessage(message)
  } catch (error) {
    console.error('Send message failed:', error)
  }
}

async function handleNewChat() {
  await chatStore.createSession()
}

function formatTime(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function renderMarkdown(content: string) {
  return marked(content, {
    highlight: (code: string, lang: string) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return code
    }
  })
}
</script>

<template>
  <div class="chat-container">
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <el-button type="primary" style="width: 100%;" @click="handleNewChat">
          <el-icon><Plus /></el-icon> 新对话
        </el-button>
      </div>

      <div class="session-list">
        <div
          v-for="session in chatStore.sessions"
          :key="session.id"
          class="session-item"
          :class="{ active: session.id === chatStore.currentSessionId }"
          @click="chatStore.fetchHistory(session.id)"
        >
          <span class="session-title">{{ session.title }}</span>
          <el-icon
            class="delete-icon"
            @click.stop="chatStore.deleteSession(session.id)"
          >
            <Delete />
          </el-icon>
        </div>
      </div>
    </aside>

    <main class="chat-main">
      <div class="messages" ref="messageListRef">
        <div v-if="!chatStore.currentSessionId" class="empty-state">
          <el-icon :size="64" color="#ccc"><ChatDotRound /></el-icon>
          <p>选择一个对话或开始新对话</p>
        </div>

        <div
          v-for="msg in chatStore.messages"
          :key="msg.id"
          class="message"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-icon v-if="msg.role === 'user'" :size="24"><User /></el-icon>
            <el-icon v-else :size="24"><Robot /></el-icon>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="renderMarkdown(msg.content)"></div>
            <span class="message-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>
      </div>

      <div class="input-area">
        <el-select
          v-model="selectedModel"
          placeholder="选择模型"
          style="width: 150px; margin-right: 10px;"
        >
          <el-option
            v-for="model in chatStore.models"
            :key="model.name"
            :label="model.name"
            :value="model.name"
          />
        </el-select>

        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="输入消息..."
          style="flex: 1;"
          @keydown.enter.ctrl="handleSend"
        />

        <el-button
          type="primary"
          :loading="chatStore.loading"
          @click="handleSend"
          style="margin-left: 10px;"
        >
          发送
        </el-button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  height: 100vh;
}

.chat-sidebar {
  width: 280px;
  background: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.session-item {
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
  transition: background 0.2s;
}

.session-item:hover {
  background: #e8e8e8;
}

.session-item.active {
  background: #409eff;
  color: #fff;
}

.session-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.delete-icon {
  opacity: 0;
  transition: opacity 0.2s;
}

.session-item:hover .delete-icon {
  opacity: 1;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 12px;
}

.message.assistant .message-avatar {
  background: #409eff;
  color: #fff;
}

.message.user .message-avatar {
  background: #67c23a;
  color: #fff;
}

.message-content {
  max-width: 70%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  background: #f5f5f5;
  line-height: 1.6;
}

.message.user .message-text {
  background: #409eff;
  color: #fff;
}

.message-text :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  display: block;
}

.message.user .message-time {
  text-align: right;
}

.input-area {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
}
</style>
