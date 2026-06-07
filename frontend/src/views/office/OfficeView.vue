<script setup lang="ts">
import { ref } from 'vue'
import { officeApi } from '@/api'
import { ElMessage } from 'element-plus'

const activeTab = ref('pdf')
const pdfFile = ref<File | null>(null)
const pdfOperation = ref('split')
const pdfPages = ref('1-3')
const pdfResult = ref('')

async function handlePdfUpload(file: { raw?: File; status?: string }) {
  pdfFile.value = file.raw || (file as any)
}

async function handlePdfOperation() {
  if (!pdfFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', pdfFile.value)

  try {
    let res
    if (pdfOperation.value === 'split') {
      formData.append('pages', pdfPages.value)
      res = await officeApi.pdfSplit(formData)
    } else if (pdfOperation.value === 'summary') {
      res = await officeApi.pdfSummary(formData)
    } else {
      res = await officeApi.pdfConvert(formData)
    }
    pdfResult.value = res?.message || res?.summary || '操作完成'
    ElMessage.success('操作完成')
  } catch (error) {
    console.error('PDF operation failed:', error)
  }
}
</script>

<template>
  <div class="office-container">
    <el-page-header @back="$router.back()" content="办公工具" />

    <el-tabs v-model="activeTab" style="margin-top: 20px;">
      <el-tab-pane label="PDF工具" name="pdf">
        <el-card>
          <template #header>
            <span>PDF处理</span>
          </template>

          <el-select v-model="pdfOperation" style="width: 200px;">
            <el-option label="拆分" value="split" />
            <el-option label="合并" value="merge" />
            <el-option label="加密" value="encrypt" />
            <el-option label="解密" value="decrypt" />
            <el-option label="转图片" value="convert" />
            <el-option label="AI总结" value="summary" />
          </el-select>

          <el-input
            v-if="pdfOperation === 'split'"
            v-model="pdfPages"
            placeholder="页面范围，如 1-3,5,7-10"
            style="margin-top: 10px; width: 200px;"
          />

          <el-upload
            :auto-upload="false"
            :on-change="handlePdfUpload"
            accept=".pdf"
            style="margin-top: 10px;"
          >
            <el-button type="primary">选择PDF文件</el-button>
          </el-upload>

          <el-button
            type="primary"
            style="margin-top: 10px;"
            @click="handlePdfOperation"
          >
            执行操作
          </el-button>

          <div v-if="pdfResult" class="result-area">
            <h4>结果:</h4>
            <p>{{ pdfResult }}</p>
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="Word工具" name="word">
        <el-card>
          <template #header>
            <span>Word文档处理</span>
          </template>

          <el-upload :auto-upload="false" accept=".docx">
            <el-button type="primary">选择Word文件</el-button>
          </el-upload>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="Excel工具" name="excel">
        <el-card>
          <template #header>
            <span>Excel表格处理</span>
          </template>

          <el-upload :auto-upload="false" accept=".xlsx,.xls">
            <el-button type="primary">选择Excel文件</el-button>
          </el-upload>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.office-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.result-area {
  margin-top: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}
</style>
