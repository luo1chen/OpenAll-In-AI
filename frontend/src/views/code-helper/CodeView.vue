<script setup lang="ts">
import { ref } from 'vue'
import { codeApi } from '@/api'
import { ElMessage } from 'element-plus'

const activeTab = ref('generate')
const codeInput = ref('')
const language = ref('python')
const codeResult = ref('')
const loading = ref(false)

// Scaffold
const scaffoldType = ref('vue-fastapi')
const scaffoldName = ref('')
const scaffoldResult = ref<any>(null)

// API Debug
const apiMethod = ref('GET')
const apiUrl = ref('')
const apiResult = ref('')

async function handleGenerate() {
  if (!codeInput.value) return

  loading.value = true
  try {
    const res = await codeApi.generate({
      prompt: codeInput.value,
      language: language.value
    })
    codeResult.value = res.code
  } catch (error) {
    console.error('Generate failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleFix() {
  if (!codeInput.value) return

  loading.value = true
  try {
    const res = await codeApi.fix({
      code: codeInput.value,
      language: language.value
    })
    codeResult.value = res.fixed_code
  } catch (error) {
    console.error('Fix failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleComment() {
  if (!codeInput.value) return

  loading.value = true
  try {
    const res = await codeApi.comment({
      code: codeInput.value,
      language: language.value
    })
    codeResult.value = res.commented_code
  } catch (error) {
    console.error('Comment failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleOptimize() {
  if (!codeInput.value) return

  loading.value = true
  try {
    const res = await codeApi.optimize({
      code: codeInput.value,
      language: language.value
    })
    codeResult.value = res.optimized_code
  } catch (error) {
    console.error('Optimize failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleScaffold() {
  if (!scaffoldName.value) {
    ElMessage.warning('请输入项目名称')
    return
  }

  loading.value = true
  try {
    const res = await codeApi.scaffold({
      project_type: scaffoldType.value,
      project_name: scaffoldName.value
    })
    scaffoldResult.value = res
    ElMessage.success('项目脚手架生成成功')
  } catch (error) {
    console.error('Scaffold failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleApiDebug() {
  if (!apiUrl.value) {
    ElMessage.warning('请输入API URL')
    return
  }

  loading.value = true
  try {
    const res = await codeApi.debugApi({
      method: apiMethod.value,
      url: apiUrl.value
    })
    apiResult.value = JSON.stringify(res, null, 2)
  } catch (error) {
    console.error('API debug failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="code-container">
    <el-page-header @back="$router.back()" content="代码助手" />

    <el-tabs v-model="activeTab" style="margin-top: 20px;">
      <el-tab-pane label="代码生成" name="generate">
        <el-card>
          <el-select v-model="language" style="width: 150px;">
            <el-option label="Python" value="python" />
            <el-option label="JavaScript" value="javascript" />
            <el-option label="TypeScript" value="typescript" />
            <el-option label="Java" value="java" />
            <el-option label="C++" value="cpp" />
            <el-option label="Go" value="go" />
          </el-select>

          <el-input
            v-model="codeInput"
            type="textarea"
            :rows="6"
            placeholder="描述你想要生成的代码..."
            style="margin-top: 10px;"
          />

          <div style="margin-top: 10px;">
            <el-button type="primary" @click="handleGenerate" :loading="loading">生成</el-button>
            <el-button @click="handleFix">纠错</el-button>
            <el-button @click="handleComment">加注释</el-button>
            <el-button @click="handleOptimize">优化</el-button>
          </div>

          <div v-if="codeResult" class="result-area">
            <h4>生成结果:</h4>
            <el-input v-model="codeResult" type="textarea" :rows="10" readonly />
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="项目脚手架" name="scaffold">
        <el-card>
          <el-select v-model="scaffoldType" style="width: 200px;">
            <el-option label="Vue3 + FastAPI" value="vue-fastapi" />
            <el-option label="React + Node.js" value="react-nodejs" />
            <el-option label="Python脚本" value="python-script" />
          </el-select>

          <el-input
            v-model="scaffoldName"
            placeholder="项目名称"
            style="margin-top: 10px; width: 200px;"
          />

          <el-button type="primary" style="margin-top: 10px;" @click="handleScaffold">
            生成脚手架
          </el-button>

          <div v-if="scaffoldResult" class="result-area">
            <h4>生成的文件:</h4>
            <el-tag v-for="file in scaffoldResult.files" :key="file" style="margin: 5px;">
              {{ file }}
            </el-tag>
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="API调试" name="api-debug">
        <el-card>
          <el-select v-model="apiMethod" style="width: 100px;">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
          </el-select>

          <el-input
            v-model="apiUrl"
            placeholder="API URL"
            style="margin-top: 10px;"
          />

          <el-button type="primary" style="margin-top: 10px;" @click="handleApiDebug">
            调试
          </el-button>

          <div v-if="apiResult" class="result-area">
            <h4>诊断结果:</h4>
            <pre>{{ apiResult }}</pre>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.code-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.result-area {
  margin-top: 20px;
}

.result-area pre {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
}
</style>
