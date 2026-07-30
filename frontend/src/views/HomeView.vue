<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElIcon } from 'element-plus'

const router = useRouter()

const features = ref([
  {
    icon: 'ChatDotRound',
    title: 'AI Chat',
    description: 'Local models + Cloud APIs. Multi-model switching.',
    route: '/chat',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    iconColor: '#fff'
  },
  {
    icon: 'Picture',
    title: 'AI Image',
    description: 'Text-to-image, image-to-image, outpainting.',
    route: '/image',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    iconColor: '#fff'
  },
  {
    icon: 'VideoCamera',
    title: 'Media AI',
    description: 'OCR, speech-to-text, AI voiceover, subtitles.',
    route: '/media',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    iconColor: '#fff'
  },
  {
    icon: 'Document',
    title: 'Office Tools',
    description: 'PDF toolkit, Word/Excel AI, exam analyzer.',
    route: '/office',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    iconColor: '#fff'
  },
  {
    icon: 'Code',
    title: 'Code Helper',
    description: 'Code generation, debugging, scaffolding.',
    route: '/code',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    iconColor: '#fff'
  },
  {
    icon: 'Grid',
    title: 'Plugins',
    description: 'Extensible plugin ecosystem, marketplace.',
    route: '/plugins',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    iconColor: '#333'
  }
])

const stats = ref([
  { value: '5+', label: 'AI Modules' },
  { value: '100%', label: 'Private' },
  { value: '0', label: 'Config Needed' },
  { value: '∞', label: 'Possibilities' }
])

const animatedStats = ref([0, 0, 0, 0])
const mounted = ref(false)

onMounted(() => {
  mounted.value = true
  animateStats()
})

function animateStats() {
  const targets = [5, 100, 0, 0]
  const duration = 1500
  const steps = 60
  const interval = duration / steps

  let step = 0
  const timer = setInterval(() => {
    step++
    const progress = step / steps
    animatedStats.value = targets.map(t => Math.round(t * progress))
    if (step >= steps) {
      clearInterval(timer)
      animatedStats.value = targets.map(t => t === 0 ? 0 : t)
    }
  }, interval)
}

function navigateTo(route: string) {
  router.push(route)
}
</script>

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="blob blob1"></div>
        <div class="blob blob2"></div>
        <div class="blob blob3"></div>
      </div>
      <div class="hero-content">
        <div class="badge">
          <span class="badge-dot"></span>
          Free & Open Source
        </div>
        <h1 class="hero-title">
          <span class="title-main">OpenAll-In-AI</span>
          <span class="title-sub">Your All-in-One AI Toolbox</span>
        </h1>
        <p class="hero-description">
          Stop juggling 10 different AI tools. Everything you need —
          <strong>chat, image gen, OCR, PDF, code, audio/video</strong> —
          in one beautiful, private, local toolbox.
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" class="cta-btn" @click="navigateTo('/chat')">
            <el-icon style="margin-right: 8px;"><ChatDotRound /></el-icon>
            Start Chatting Now
          </el-button>
          <el-button size="large" class="ghost-btn" @click="navigateTo('/code')">
            <el-icon style="margin-right: 8px;"><Code /></el-icon>
            Explore Tools
          </el-button>
        </div>
        <div class="hero-stats">
          <div class="stat-item" v-for="(stat, index) in stats" :key="index">
            <div class="stat-value">
              {{ animatedStats[index] }}{{ stat.value.includes('+') ? '+' : '' }}{{ stat.value.includes('%') ? '%' : '' }}
            </div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="section-header">
        <h2>🧰 Powerful Features</h2>
        <p>Six comprehensive AI modules. Infinite possibilities.</p>
      </div>
      <div class="features-grid">
        <div
          v-for="feature in features"
          :key="feature.route"
          class="feature-card"
          :class="{ 'mounted': mounted }"
          :style="{ '--delay': `${features.indexOf(feature) * 80}ms` }"
          @click="navigateTo(feature.route)"
        >
          <div class="feature-icon-wrapper" :style="{ background: feature.gradient }">
            <el-icon :size="28" :color="feature.iconColor">
              <component :is="feature.icon" />
            </el-icon>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
          <div class="feature-arrow">
            →
          </div>
        </div>
      </div>
    </section>

    <!-- Comparison Section -->
    <section class="comparison-section">
      <div class="section-header">
        <h2>🆚 Why Choose Us?</h2>
        <p>OpenAll-In-AI offers more value than any single AI app.</p>
      </div>
      <div class="comparison-grid">
        <div class="comparison-item">
          <div class="comparison-icon">🔒</div>
          <h4>100% Private</h4>
          <p>All processing happens locally. Your data never leaves your machine.</p>
        </div>
        <div class="comparison-item">
          <div class="comparison-icon">⚡</div>
          <h4>Zero Config</h4>
          <p>Download, double-click, and go. No Python setup, no CUDA, no API keys.</p>
        </div>
        <div class="comparison-item">
          <div class="comparison-icon">🦊</div>
          <h4>Lightweight</h4>
          <p>Runs smoothly on 8GB RAM laptops with local AI models.</p>
        </div>
        <div class="comparison-item">
          <div class="comparison-icon">🔌</div>
          <h4>Extensible</h4>
          <p>Open plugin SDK. Build custom tools in minutes.</p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>Ready to supercharge your productivity?</h2>
        <p>Join thousands of users who've already made the switch.</p>
        <div class="cta-buttons">
          <el-button type="primary" size="large" class="cta-btn" @click="navigateTo('/chat')">
            Get Started Free
          </el-button>
          <el-button size="large" class="ghost-btn" @click="navigateTo('/settings')">
            Configure API
          </el-button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: #fafbfc;
}

/* Hero Section */
.hero {
  position: relative;
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s infinite ease-in-out;
}

.blob1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.blob2 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  bottom: -100px;
  left: -50px;
  animation-delay: -7s;
}

.blob3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  top: 50%;
  left: 50%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 60px 20px;
  max-width: 800px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 100px;
  font-size: 14px;
  color: #667eea;
  margin-bottom: 24px;
  animation: fadeInDown 0.6s ease;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.hero-title {
  margin-bottom: 20px;
  animation: fadeInUp 0.6s ease;
}

.title-main {
  display: block;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  margin-bottom: 12px;
}

.title-sub {
  display: block;
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  color: #666;
  font-weight: 500;
}

.hero-description {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.8;
  max-width: 600px;
  margin: 0 auto 32px;
  animation: fadeInUp 0.6s ease 0.1s both;
}

.hero-description strong {
  color: #333;
  font-weight: 600;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 48px;
  animation: fadeInUp 0.6s ease 0.2s both;
}

.cta-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  padding: 14px 32px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  transition: all 0.3s !important;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}

.cta-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5) !important;
}

.ghost-btn {
  padding: 14px 32px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  background: rgba(255, 255, 255, 0.8) !important;
  border: 2px solid #e0e0e0 !important;
  color: #333 !important;
  transition: all 0.3s !important;
}

.ghost-btn:hover {
  border-color: #667eea !important;
  color: #667eea !important;
  transform: translateY(-2px) !important;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
  flex-wrap: wrap;
  animation: fadeInUp 0.6s ease 0.3s both;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #888;
  margin-top: 4px;
}

/* Features Section */
.features-section {
  padding: 80px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-header h2 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #222;
  margin-bottom: 12px;
}

.section-header p {
  font-size: 1.1rem;
  color: #666;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.feature-card {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s ease var(--delay) forwards;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  border-color: transparent;
}

.feature-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.feature-card:hover .feature-icon-wrapper {
  transform: scale(1.1);
}

.feature-card h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 8px;
}

.feature-card p {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
}

.feature-arrow {
  position: absolute;
  top: 32px;
  right: 32px;
  font-size: 1.5rem;
  color: #ccc;
  transition: all 0.3s;
}

.feature-card:hover .feature-arrow {
  color: #667eea;
  transform: translateX(4px);
}

/* Comparison Section */
.comparison-section {
  padding: 80px 20px;
  background: linear-gradient(180deg, #fff 0%, #f8f9ff 100%);
}

.comparison-grid {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 32px;
}

.comparison-item {
  text-align: center;
  padding: 32px 24px;
  background: #fff;
  border-radius: 20px;
  transition: all 0.3s;
}

.comparison-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
}

.comparison-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.comparison-item h4 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 8px;
}

.comparison-item p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  padding: 100px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
}

.cta-content h2 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 12px;
}

.cta-content p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 32px;
}

.cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-section .cta-btn {
  background: #fff !important;
  color: #667eea !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.cta-section .cta-btn:hover {
  background: #f8f8ff !important;
  color: #5a6fd8 !important;
}

.cta-section .ghost-btn {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 2px solid rgba(255, 255, 255, 0.5) !important;
  color: #fff !important;
}

.cta-section .ghost-btn:hover {
  background: rgba(255, 255, 255, 0.2) !important;
  border-color: #fff !important;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .hero {
    min-height: 90vh;
    padding: 40px 20px;
  }

  .hero-stats {
    gap: 24px;
  }

  .stat-value {
    font-size: 2rem;
  }

  .features-section,
  .comparison-section,
  .cta-section {
    padding: 60px 20px;
  }

  .section-header h2 {
    font-size: 1.8rem;
  }

  .comparison-grid {
    grid-template-columns: 1fr;
  }
}
</style>