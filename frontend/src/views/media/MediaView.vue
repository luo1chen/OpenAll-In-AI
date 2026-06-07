<script setup lang="ts">
import { ref } from 'vue'
import { mediaApi } from '@/api'
import { ElMessage } from 'element-plus'

const activeTab = ref('ocr')
const ocrFile = ref<any>(null)
const ocrResult = ref('')
const ttsText = ref('')
const ttsLang = ref('zh')
const ttsResult = ref('')

async function handleOcrUpload(file: any) {
  const formData = new FormData()
  formData.append('file', file.raw || file)

  try {
    const res = await mediaApi.ocrRecognize(formData)
    ocrResult.value = res.text || 'OCR completed'
    ElMessage.success('OCR识别完成')
  } catch (error) {
    console.error('OCR failed:', error)
  }
}

async function handleTts() {
  if (!ttsText.value) return

  try {
    const res = await mediaApi.textToSpeech({
      text: ttsText.value,
      lang: ttsLang.value
    })
    ElMessage.success('TTS任务已提交')
  } catch (error) {
    console.error('TTS failed:', error)
  }
}
</script>

<template>
  <div class="media-container">
    <el-page-header @back="$router.back()" content="多媒体处理" />

    <el-tabs v-model="activeTab" style="margin-top: 20px;">
      <el-tab-pane label="OCR识别" name="ocr">
        <el-card>
          <template #header>
            <span>图片文字识别</span>
          </template>

          <el-upload
            :auto-upload="false"
            :on-change="handleOcrUpload"
            :limit="1"
            accept="image/*"
          >
            <el-button type="primary">选择图片</el-button>
          </el-upload>

          <div v-if="ocrResult" class="result-area">
            <h4>识别结果:</h4>
            <el-input
              v-model="ocrResult"
              type="textarea"
              :rows="10"
              readonly
            />
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="语音合成" name="tts">
        <el-card>
          <template #header>
            <span>文本转语音</span>
          </template>

          <el-input
            v-model="ttsText"
            type="textarea"
            :rows="5"
            placeholder="输入要转换的文本"
          />

          <el-select v-model="ttsLang" style="margin-top: 10px;">
            <el-option label="中文" value="zh" />
            <el-option label="英文" value="en" />
            <el-option label="日文" value="ja" />
          </el-select>

          <el-button
            type="primary"
            style="margin-top: 10px;"
            @click="handleTts"
          >
            生成语音
          </el-button>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="语音转文字" name="asr">
        <el-card>
          <template #header>
            <span>语音转文字</span>
          </template>

          <el-upload
            :auto-upload="false"
            accept="audio/*"
          >
            <el-button type="primary">选择音频文件</el-button>
          </el-upload>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="音频降噪" name="denoise">
        <el-card>
          <template #header>
            <span>音频降噪</span>
          </template>

          <el-upload
            :auto-upload="false"
            accept="audio/*"
          >
            <el-button type="primary">选择音频文件</el-button>
          </el-upload>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.media-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.result-area {
  margin-top: 20px;
}

.result-area h4 {
  margin-bottom: 10px;
}
</style>
