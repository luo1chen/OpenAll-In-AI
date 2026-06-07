import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ai-chat/ChatView.vue')
    },
    {
      path: '/chat/:sessionId',
      name: 'chat-session',
      component: () => import('@/views/ai-chat/ChatView.vue')
    },
    {
      path: '/image',
      name: 'image',
      component: () => import('@/views/image/ImageView.vue')
    },
    {
      path: '/media',
      name: 'media',
      component: () => import('@/views/media/MediaView.vue')
    },
    {
      path: '/office',
      name: 'office',
      component: () => import('@/views/office/OfficeView.vue')
    },
    {
      path: '/code',
      name: 'code',
      component: () => import('@/views/code-helper/CodeView.vue')
    },
    {
      path: '/plugins',
      name: 'plugins',
      component: () => import('@/views/plugins/PluginsView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/settings/SettingsView.vue')
    }
  ]
})

export default router
