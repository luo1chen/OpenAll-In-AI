# OpenAll-In-AI 项目规范文档

## 1. 项目概述

**项目名称**: OpenAll-In-AI  
**项目类型**: 跨平台AI聚合工具箱  
**核心功能**: 整合大模型对话、AI绘图、OCR、文档解析、代码生成、音视频处理、PDF工具的一站式本地部署AI工具箱  
**目标用户**: 学生、上班族、程序员、自媒体从业者

---

## 2. 技术架构

### 2.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端 | Vue3 + Element Plus | 静态网页打包，内嵌无需额外浏览器 |
| 后端 | Python FastAPI | 轻量易读，新手易改源码 |
| 模型推理 | llama.cpp | 轻量化推理框架 |
| 打包工具 | PyInstaller | Windows/macOS/Linux跨平台打包 |

### 2.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Vue3)                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │AI对话模块│ │多媒体模块│ │办公模块 │ │代码助手 │ │插件系统│ │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ │
└───────┼──────────┼──────────┼──────────┼──────────┼───────┘
        │          │          │          │          │
        └──────────┴──────────┴──────────┴──────────┘
                              │
                    ┌─────────┴─────────┐
                    │   FastAPI Gateway  │
                    │   (API Router)     │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────┴───────┐    ┌────────┴────────┐   ┌────────┴────────┐
│  AI Model Mgr │    │   Office Tools   │   │   Plugin SDK    │
│  (llama.cpp)  │    │  (PDF/Word/Excel)│   │                 │
└───────────────┘    └──────────────────┘   └─────────────────┘
```

---

## 3. 目录结构

```
OpenAll-In-AI/
├── docs/                    # 项目使用文档
├── frontend/                # Vue前端源码
│   ├── src/
│   │   ├── api/            # API调用封装
│   │   ├── components/     # 公共组件
│   │   ├── views/          # 页面视图
│   │   │   ├── ai-chat/    # AI对话模块
│   │   │   ├── media/      # 多媒体模块
│   │   │   ├── office/     # 办公工具模块
│   │   │   ├── code-helper/# 代码助手模块
│   │   │   └── plugins/    # 插件市场
│   │   ├── stores/         # Pinia状态管理
│   │   ├── router/         # Vue Router配置
│   │   └── utils/          # 工具函数
│   └── package.json
├── backend/                 # FastAPI后端逻辑
│   ├── main.py             # 应用入口
│   ├── api/                # API路由
│   │   ├── chat.py         # AI对话API
│   │   ├── media.py        # 多媒体API
│   │   ├── office.py       # 办公工具API
│   │   ├── code.py         # 代码助手API
│   │   └── plugins.py      # 插件API
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置管理
│   │   └── security.py     # 安全相关
│   ├── model_manager/      # 大模型管理
│   │   ├── downloader.py   # 模型下载
│   │   ├── inference.py     # 推理引擎
│   │   └── registry.py     # 模型注册表
│   ├── services/          # 业务逻辑层
│   │   ├── chat_service.py
│   │   ├── ocr_service.py
│   │   ├── pdf_service.py
│   │   └── code_service.py
│   ├── plugins/           # 插件系统
│   │   ├── sdk.py          # 插件SDK
│   │   ├── loader.py       # 插件加载器
│   │   └── market.py       # 插件市场
│   ├── tools/             # 工具模块
│   │   ├── pdf_tool.py
│   │   ├── office_tool.py
│   │   └── media_tool.py
│   └── requirements.txt
├── plugins/                # 官方内置插件
├── scripts/               # 打包、一键启动脚本
├── tests/                 # 测试文件
│   ├── backend/           # 后端测试
│   └── frontend/          # 前端测试
├── releases/              # 预编译安装包
├── requirements.txt       # Python依赖清单
├── main.py               # 项目启动入口
└── README.md
```

---

## 4. 功能模块详细规范

### 4.1 模块1: 全能AI对话引擎

#### 4.1.1 本地离线模型
- **功能**: 一键自动下载Qwen/Llama3/Gemma轻量化开源大模型
- **实现要求**:
  - 自动检测硬件配置（内存、GPU）
  - 智能推荐适配大小的本地模型
  - 自动断点下载权重
  - 模型文件校验（MD5/SHA256）

#### 4.1.2 多API聚合
- **功能**: 国内外主流大模型接口统一配置面板
- **支持模型**:
  - OpenAI GPT系列
  - 阿里通义千问
  - 讯飞星火
  - DeepSeek
  - 本地Llama/QQwen/Gemma
- **实现要求**:
  - 统一对话格式
  - 一键切换模型
  - API Key安全管理
  - 调用频率限制

#### 4.1.3 特色功能
- **角色预设**: 代码专家、论文润色、职场文案、学习答疑
- **对话存档**: 本地SQLite存储
- **Markdown导出**: 支持导出对话记录
- **长文档总结**: 万字文本一键提炼摘要

#### 4.1.4 API设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/chat/send | 发送对话消息 |
| GET | /api/chat/history/{session_id} | 获取对话历史 |
| POST | /api/chat/session | 创建新对话 |
| DELETE | /api/chat/session/{session_id} | 删除对话 |
| GET | /api/models | 获取可用模型列表 |
| POST | /api/models/download | 下载模型 |
| GET | /api/models/download/status | 获取下载状态 |

#### 4.1.5 数据模型

```python
# Chat Session
class ChatSession:
    id: str  # UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model: str
    system_prompt: str

# Chat Message
class ChatMessage:
    id: str  # UUID
    session_id: str
    role: str  # user/assistant/system
    content: str
    created_at: datetime

# Model Info
class ModelInfo:
    name: str
    size: int
    dtype: str
    quantized: bool
    local_path: str
    status: str  # downloaded/downloading/available
```

---

### 4.2 模块2: 多媒体AI工作站

#### 4.2.1 AI绘画
- **功能**: 整合Stable Diffusion轻量化版本+FLUX小模型
- **特性**:
  - 文生图（Text-to-Image）
  - 图生图（Image-to-Image）
  - 扩图（Outpainting）
  - 背景消除（Background Removal）
- **实现要求**:
  - 本地出图，无需网络
  - 支持自定义分辨率
  - 支持风格预设

#### 4.2.2 音视频处理
- **功能**:
  - 语音转文字（ASR）
  - AI配音（TTS）
  - 视频字幕自动生成
  - 音频降噪
  - 短视频文案提取
- **实现要求**:
  - 支持MP3/WAV/MP4/AVI格式
  - 批量处理队列
  - 进度实时反馈

#### 4.2.3 OCR全格式
- **功能**:
  - 图片文字识别（PaddleOCR）
  - PDF文字识别
  - 截图文字识别
  - 公式识别
  - 表格提取
- **支持语言**: 中文、英文、日文、韩文

#### 4.2.4 API设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/media/tts | 文本转语音 |
| POST | /api/media/asr | 语音转文字 |
| POST | /api/media/ocr | OCR识别 |
| POST | /api/media/denoise | 音频降噪 |
| POST | /api/image/generate | 文生图 |
| POST | /api/image/edit | 图生图 |
| GET | /api/media/tasks/{task_id} | 获取任务状态 |

---

### 4.3 模块3: 文档&办公黑科技

#### 4.3.1 PDF工具箱
- **功能**:
  - PDF拆分
  - PDF合并
  - PDF加密/解密
  - PDF转Word
  - PDF转Excel
  - PDF转图片
  - AI总结PDF

#### 4.3.2 Word/Excel处理
- **功能**:
  - AI批量处理表格
  - 文档纠错
  - 批量文案改写
- **实现要求**:
  - 模板填充
  - 批量操作支持

#### 4.3.3 题库/笔记
- **功能**:
  - 试卷AI解析
  - 知识点归纳
  - 思维导图生成
- **输出格式**: Markdown、PDF

#### 4.3.4 API设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/office/pdf/split | PDF拆分 |
| POST | /api/office/pdf/merge | PDF合并 |
| POST | /api/office/pdf/encrypt | PDF加密 |
| POST | /api/office/pdf/convert | PDF格式转换 |
| POST | /api/office/pdf/summary | AI总结PDF |
| POST | /api/office/docx/process | Word文档处理 |
| POST | /api/office/excel/process | Excel批量处理 |
| POST | /api/office/notes/summary | 笔记总结 |

---

### 4.4 模块4: 程序员开发助手

#### 4.4.1 代码生成/纠错/注释
- **功能**:
  - 多语言代码生成（C/C++/Python/Java/JS）
  - 代码纠错
  - 自动注释生成
  - 代码优化建议
- **实现要求**:
  - 语法高亮
  - 代码片段缓存

#### 4.4.2 项目脚手架
- **功能**: 输入需求自动生成前后端简易项目模板
- **模板类型**:
  - Vue3 + FastAPI 前后端分离
  - React + Node.js
  - 纯Python脚本

#### 4.4.3 接口调试
- **功能**: 简易Postman替代工具
- **特性**:
  - 支持GET/POST/PUT/DELETE
  - 请求头/参数编辑
  - 响应格式化
  - AI自动生成接口入参

#### 4.4.4 API设计

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/code/generate | 代码生成 |
| POST | /api/code/fix | 代码纠错 |
| POST | /api/code/comment | 生成注释 |
| POST | /api/code/optimize | 代码优化 |
| POST | /api/code/scaffold | 项目脚手架 |
| POST | /api/code/debug | 接口调试 |

---

### 4.5 模块5: 插件生态系统

#### 4.5.1 插件SDK
- **功能**: 开放插件SDK，支持第三方插件接入
- **SDK规范**:
  - 插件目录结构标准化
  - 插件manifest.json声明
  - Hook钩子机制
  - 生命周期管理

#### 4.5.2 插件市场
- **功能**: 内置插件市场，一键安装
- **特性**:
  - 插件搜索
  - 版本管理
  - 依赖解析

#### 4.5.3 官方内置插件
- AI翻译插件
- 网盘解析插件
- 爬虫小工具

#### 4.5.4 API设计

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/plugins | 获取已安装插件 |
| GET | /api/plugins/market | 获取市场插件列表 |
| POST | /api/plugins/install | 安装插件 |
| POST | /api/plugins/uninstall | 卸载插件 |
| GET | /api/plugins/{plugin_id} | 获取插件详情 |

---

## 5. 前端页面结构

### 5.1 页面路由

| 路径 | 页面 | 描述 |
|------|------|------|
| / | 首页/仪表盘 | 功能入口、快捷操作 |
| /chat | AI对话 | 主对话界面 |
| /chat/{session_id} | 对话详情 | 单个对话会话 |
| /image | AI绘图 | 绘图工作台 |
| /media | 多媒体处理 | 音视频、OCR处理 |
| /office | 办公工具 | PDF、Word、Excel工具 |
| /code | 代码助手 | 代码生成、调试 |
| /plugins | 插件管理 | 插件市场、安装 |
| /settings | 设置 | API配置、模型管理 |

### 5.2 组件设计

```
views/
├── HomeView.vue              # 首页仪表盘
├── chat/
│   ├── ChatView.vue          # 对话主界面
│   ├── ChatSidebar.vue       # 对话列表侧边栏
│   ├── ChatMessage.vue       # 消息气泡
│   └── ChatInput.vue         # 输入框组件
├── image/
│   ├── ImageView.vue         # 绘图主界面
│   ├── PromptInput.vue       # 提示词输入
│   └── ImageGallery.vue      # 生成结果画廊
├── media/
│   ├── MediaView.vue         # 多媒体处理主界面
│   ├── OcrPanel.vue          # OCR面板
│   ├── TtsPanel.vue          # TTS面板
│   └── AsrPanel.vue          # ASR面板
├── office/
│   ├── OfficeView.vue        # 办公工具主界面
│   ├── PdfTool.vue           # PDF工具面板
│   ├── WordTool.vue          # Word工具面板
│   └── ExcelTool.vue         # Excel工具面板
├── code/
│   ├── CodeView.vue          # 代码助手主界面
│   ├── CodeEditor.vue        # 代码编辑器
│   └── ApiDebugger.vue       # API调试工具
├── plugins/
│   ├── PluginsView.vue       # 插件管理主界面
│   ├── PluginCard.vue        # 插件卡片
│   └── PluginDetail.vue      # 插件详情
└── settings/
    ├── SettingsView.vue      # 设置主界面
    ├── ApiConfig.vue         # API配置面板
    └── ModelManager.vue      # 模型管理面板
```

---

## 6. 测试策略 (TDD)

### 6.1 测试分层

1. **单元测试**: 各模块核心函数
2. **集成测试**: API端到端测试
3. **E2E测试**: 关键用户流程测试

### 6.2 测试框架

| 层级 | 框架 |
|------|------|
| 后端单元 | pytest |
| 后端集成 | pytest + httpx |
| 前端单元 | Vitest |
| 前端E2E | Playwright |

### 6.3 测试覆盖要求

- 核心业务逻辑覆盖率 > 80%
- API端点覆盖率 100%
- 关键用户路径100%覆盖

---

## 7. 配置管理

### 7.1 环境变量

```bash
# 后端配置
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./data/openall.db

# 模型配置
MODEL_CACHE_DIR=./models
DEFAULT_MODEL=qwen2.5-7b

# API配置（可选）
OPENAI_API_KEY=
DASHSCOPE_API_KEY=
SPARK_API_KEY=
DEEPSEEK_API_KEY=
```

### 7.2 配置文件

```json
// config.json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "models": {
    "cache_dir": "./models",
    "default": "qwen2.5-7b",
    "auto_download": true
  },
  "apis": {
    "openai": {
      "enabled": false,
      "api_key": ""
    },
    "dashscope": {
      "enabled": false,
      "api_key": ""
    }
  },
  "plugins": {
    "enabled": true,
    "market_url": "https://plugins.openall.ai"
  }
}
```

---

## 8. 验收标准

### 8.1 功能验收

- [ ] AI对话：支持本地模型和API调用，能创建会话、发送消息、查看历史
- [ ] AI绘图：能生成图片、保存到本地
- [ ] 多媒体：OCR能识别图片文字，TTS能生成语音
- [ ] 办公工具：PDF能拆分合并，能转换为图片
- [ ] 代码助手：能生成代码、能调用API调试
- [ ] 插件系统：能安装卸载插件

### 8.2 技术验收

- [ ] 前端能正常启动，无编译错误
- [ ] 后端API能正常启动，端口8000
- [ ] 前后端联调正常
- [ ] 所有API端点有对应测试
- [ ] 代码覆盖率 > 80%

### 8.3 用户体验验收

- [ ] 界面响应流畅，无明显卡顿
- [ ] 操作有适当loading提示
- [ ] 错误信息友好展示
- [ ] 支持深色/浅色主题

---

## 9. 开发阶段划分

### Phase 1: 项目基础设施
- 项目结构搭建
- FastAPI后端骨架
- Vue3前端骨架
- 数据库模型设计
- 基础API路由

### Phase 2: AI对话核心
- 模型管理器实现
- 对话API实现
- 前端对话界面

### Phase 3: 多媒体模块
- OCR服务实现
- TTS/ASR服务实现
- 图片生成基础功能

### Phase 4: 办公工具模块
- PDF工具实现
- Word/Excel处理基础

### Phase 5: 代码助手模块
- 代码生成服务
- API调试工具

### Phase 6: 插件系统
- 插件SDK实现
- 插件加载器
- 插件市场基础

### Phase 7: 完善与优化
- 单元测试补充
- 界面优化
- 文档完善
