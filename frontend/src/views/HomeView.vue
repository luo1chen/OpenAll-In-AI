<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const features = ref([
  {
    icon: 'ChatDotRound',
    title: 'AI对话',
    description: '支持本地模型和云端API，一键切换多模型',
    route: '/chat',
    color: '#409eff'
  },
  {
    icon: 'Picture',
    title: 'AI绘图',
    description: '文生图、图生图、扩图，本地轻量级出图',
    route: '/image',
    color: '#67c23a'
  },
  {
    icon: 'VideoCamera',
    title: '多媒体处理',
    description: 'OCR识别、语音转文字、AI配音',
    route: '/media',
    color: '#e6a23c'
  },
  {
    icon: 'Document',
    title: '办公工具',
    description: 'PDF拆分合并、Word/Excel智能处理',
    route: '/office',
    color: '#f56c6c'
  },
  {
    icon: 'Code',
    title: '代码助手',
    description: '代码生成、纠错、优化、接口调试',
    route: '/code',
    color: '#909399'
  },
  {
    icon: 'Grid',
    title: '插件市场',
    description: '插件生态系统，可扩展功能',
    route: '/plugins',
    color: '#409eff'
  }
])
</script>

<template>
  <div class="home">
    <div class="header">
      <div class="logo">
        <h1>OpenAll-In-AI</h1>
        <p>一站式本地部署AI聚合工具箱</p>
      </div>
    </div>

    <div class="features">
      <el-row :gutter="20">
        <el-col :span="8" v-for="feature in features" :key="feature.route">
          <div class="feature-card" @click="router.push(feature.route)">
            <div class="feature-icon" :style="{ backgroundColor: feature.color }">
              <el-icon :size="32">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="quick-start">
      <h2>快速开始</h2>
      <el-card>
        <pre><code># Windows
双击 Start.exe

# Linux/macOS
git clone https://github.com/xxx/OpenAll-In-AI.git
cd OpenAll-In-AI
python main.py</code></pre>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 60px;
}

.logo h1 {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 10px;
}

.logo p {
  font-size: 18px;
  color: #666;
}

.features {
  margin-bottom: 60px;
}

.feature-card {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: #fff;
}

.feature-card h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.feature-card p {
  color: #666;
  font-size: 14px;
}

.quick-start h2 {
  margin-bottom: 20px;
  text-align: center;
}

.quick-start pre {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
}
</style>
