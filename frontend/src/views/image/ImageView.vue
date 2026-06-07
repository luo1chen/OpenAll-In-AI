<script setup lang="ts">
import { ref } from 'vue'
import { mediaApi } from '@/api'
import { ElMessage } from 'element-plus'

const prompt = ref('')
const negativePrompt = ref('')
const width = ref(512)
const height = ref(512)
const steps = ref(20)
const loading = ref(false)
const generatedImages = ref<string[]>([])

async function handleGenerate() {
  if (!prompt.value) {
    ElMessage.warning('请输入图片描述')
    return
  }

  loading.value = true
  try {
    const res = await mediaApi.generateImage({
      prompt: prompt.value,
      negative_prompt: negativePrompt.value || undefined,
      width: width.value,
      height: height.value
    })

    ElMessage.success('图片生成任务已提交')
    // 模拟生成结果
    generatedImages.value.push('https://via.placeholder.com/512x512')
  } catch (error) {
    console.error('Generate failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="image-container">
    <el-page-header @back="$router.back()" content="AI绘图" />

    <div class="image-layout">
      <aside class="settings-panel">
        <el-card>
          <template #header>
            <span>生成设置</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="图片描述 (Prompt)">
              <el-input
                v-model="prompt"
                type="textarea"
                :rows="4"
                placeholder="描述你想要生成的图片..."
              />
            </el-form-item>

            <el-form-item label="反向提示词 (Negative Prompt)">
              <el-input
                v-model="negativePrompt"
                type="textarea"
                :rows="2"
                placeholder="不想要的内容..."
              />
            </el-form-item>

            <el-form-item label="尺寸">
              <el-select v-model="width" style="width: 100px;">
                <el-option label="256" :value="256" />
                <el-option label="512" :value="512" />
                <el-option label="768" :value="768" />
                <el-option label="1024" :value="1024" />
              </el-select>
              <span style="margin: 0 10px;">×</span>
              <el-select v-model="height" style="width: 100px;">
                <el-option label="256" :value="256" />
                <el-option label="512" :value="512" />
                <el-option label="768" :value="768" />
                <el-option label="1024" :value="1024" />
              </el-select>
            </el-form-item>

            <el-form-item label="生成步数">
              <el-slider v-model="steps" :min="1" :max="50" show-input />
            </el-form-item>

            <el-button
              type="primary"
              style="width: 100%;"
              @click="handleGenerate"
              :loading="loading"
            >
              生成图片
            </el-button>
          </el-form>
        </el-card>
      </aside>

      <main class="preview-panel">
        <el-card>
          <template #header>
            <span>生成结果</span>
          </template>

          <div v-if="generatedImages.length === 0" class="empty-preview">
            <el-icon :size="64" color="#ccc"><Picture /></el-icon>
            <p>生成的图片将显示在这里</p>
          </div>

          <div v-else class="image-grid">
            <el-image
              v-for="(img, index) in generatedImages"
              :key="index"
              :src="img"
              fit="contain"
              class="generated-image"
            />
          </div>
        </el-card>
      </main>
    </div>
  </div>
</template>

<style scoped>
.image-container {
  padding: 20px;
  height: calc(100vh - 40px);
}

.image-layout {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  height: calc(100% - 80px);
}

.settings-panel {
  width: 350px;
  flex-shrink: 0;
}

.preview-panel {
  flex: 1;
}

.preview-panel .el-card {
  height: 100%;
}

.preview-panel .el-card__body {
  height: calc(100% - 60px);
  overflow-y: auto;
}

.empty-preview {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(256px, 1fr));
  gap: 16px;
}

.generated-image {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>
