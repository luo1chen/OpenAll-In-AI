<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'
import { ElMessage } from 'element-plus'

const chatStore = useChatStore()

const openaiEnabled = ref(false)
const openaiKey = ref('')
const dashscopeEnabled = ref(false)
const dashscopeKey = ref('')
const selectedModel = ref('qwen2.5-7b')

onMounted(() => {
  chatStore.fetchModels()
})

async function saveApiSettings() {
  // Save API settings
  ElMessage.success('API设置已保存')
}

async function downloadModel(modelName: string) {
  try {
    await chatStore.downloadModel(modelName)
    ElMessage.success('模型下载任务已启动')
  } catch (error) {
    console.error('Download failed:', error)
  }
}
</script>

<template>
  <div class="settings-container">
    <el-page-header @back="$router.back()" content="设置" />

    <el-tabs style="margin-top: 20px;">
      <el-tab-pane label="API配置">
        <el-card>
          <template #header>
            <span>云端API配置</span>
          </template>

          <el-form label-position="top">
            <el-divider content-position="left">OpenAI</el-divider>
            <el-form-item label="启用">
              <el-switch v-model="openaiEnabled" />
            </el-form-item>
            <el-form-item label="API Key">
              <el-input
                v-model="openaiKey"
                type="password"
                placeholder="sk-..."
                show-password
              />
            </el-form-item>

            <el-divider content-position="left">阿里云通义千问</el-divider>
            <el-form-item label="启用">
              <el-switch v-model="dashscopeEnabled" />
            </el-form-item>
            <el-form-item label="API Key">
              <el-input
                v-model="dashscopeKey"
                type="password"
                placeholder="sk-..."
                show-password
              />
            </el-form-item>

            <el-button type="primary" @click="saveApiSettings">
              保存设置
            </el-button>
          </el-form>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="模型管理">
        <el-card>
          <template #header>
            <span>本地模型管理</span>
          </template>

          <el-table :data="chatStore.models" style="width: 100%">
            <el-table-column prop="name" label="模型名称" width="200" />
            <el-table-column prop="size" label="大小" width="120">
              <template #default="{ row }">
                {{ (row.size / 1e9).toFixed(1) }} GB
              </template>
            </el-table-column>
            <el-table-column prop="dtype" label="数据类型" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'downloaded' ? 'success' : 'info'">
                  {{ row.status === 'downloaded' ? '已下载' : '可下载' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button
                  v-if="row.status !== 'downloaded'"
                  type="primary"
                  size="small"
                  @click="downloadModel(row.name)"
                >
                  下载
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="通用设置">
        <el-card>
          <template #header>
            <span>通用设置</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="默认模型">
              <el-select v-model="selectedModel" style="width: 200px;">
                <el-option
                  v-for="model in chatStore.models"
                  :key="model.name"
                  :label="model.name"
                  :value="model.name"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="主题">
              <el-radio-group>
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
                <el-radio label="auto">跟随系统</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-button type="primary">保存设置</el-button>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
</style>
