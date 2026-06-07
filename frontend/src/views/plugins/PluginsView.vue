<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { pluginsApi } from '@/api'
import { ElMessage } from 'element-plus'

const installedPlugins = ref<any[]>([])
const marketPlugins = ref<any[]>([])
const loading = ref(false)

onMounted(async () => {
  await fetchPlugins()
})

async function fetchPlugins() {
  loading.value = true
  try {
    const [installed, market] = await Promise.all([
      pluginsApi.list(),
      pluginsApi.listMarket()
    ])
    installedPlugins.value = installed
    marketPlugins.value = market.plugins
  } catch (error) {
    console.error('Fetch plugins failed:', error)
  } finally {
    loading.value = false
  }
}

async function handleInstall(pluginId: string) {
  try {
    await pluginsApi.install(pluginId)
    ElMessage.success('插件安装成功')
    await fetchPlugins()
  } catch (error) {
    console.error('Install failed:', error)
  }
}

async function handleUninstall(pluginId: string) {
  try {
    await pluginsApi.uninstall(pluginId)
    ElMessage.success('插件卸载成功')
    await fetchPlugins()
  } catch (error) {
    console.error('Uninstall failed:', error)
  }
}

async function handleToggle(pluginId: string, enabled: boolean) {
  try {
    if (enabled) {
      await pluginsApi.enable(pluginId)
    } else {
      await pluginsApi.disable(pluginId)
    }
    await fetchPlugins()
  } catch (error) {
    console.error('Toggle failed:', error)
  }
}
</script>

<template>
  <div class="plugins-container">
    <el-page-header @back="$router.back()" content="插件市场" />

    <el-tabs style="margin-top: 20px;">
      <el-tab-pane label="已安装插件">
        <el-row :gutter="20">
          <el-col :span="8" v-for="plugin in installedPlugins" :key="plugin.id">
            <el-card class="plugin-card">
              <template #header>
                <div class="plugin-header">
                  <span>{{ plugin.name }}</span>
                  <el-switch
                    :model-value="plugin.enabled"
                    @change="handleToggle(plugin.id, $event)"
                  />
                </div>
              </template>
              <p>{{ plugin.description }}</p>
              <div class="plugin-footer">
                <span class="version">v{{ plugin.version }}</span>
                <span class="author">by {{ plugin.author }}</span>
              </div>
              <el-button
                type="danger"
                size="small"
                style="margin-top: 10px; width: 100%;"
                @click="handleUninstall(plugin.id)"
              >
                卸载
              </el-button>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="installedPlugins.length === 0" description="暂无已安装插件" />
      </el-tab-pane>

      <el-tab-pane label="插件市场">
        <el-row :gutter="20">
          <el-col :span="8" v-for="plugin in marketPlugins" :key="plugin.id">
            <el-card class="plugin-card">
              <template #header>
                <span>{{ plugin.name }}</span>
              </template>
              <p>{{ plugin.description }}</p>
              <div class="plugin-footer">
                <span class="version">v{{ plugin.version }}</span>
                <span class="author">by {{ plugin.author }}</span>
              </div>
              <el-button
                type="primary"
                size="small"
                style="margin-top: 10px; width: 100%;"
                @click="handleInstall(plugin.id)"
              >
                安装
              </el-button>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="marketPlugins.length === 0" description="暂无插件" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.plugins-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.plugin-card {
  margin-bottom: 20px;
}

.plugin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plugin-footer {
  margin-top: 10px;
  font-size: 12px;
  color: #999;
}

.version {
  margin-right: 10px;
}
</style>
