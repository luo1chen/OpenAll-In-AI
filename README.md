# OpenAll-In-AI

<div align="center">

**All-in-One Local AI Toolbox**

[![GitHub stars](https://img.shields.io/github/stars/xxx/OpenAll-In-AI)](https://github.com/xxx/OpenAll-In-AI/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)

</div>

## Project Introduction

OpenAll-In-AI is an open-source, free AI toolbox that integrates large language model chat, AI image generation, OCR, document parsing, code generation, audio/video processing, and PDF tools. It can be launched with one click without complex configuration, supporting Windows/macOS/Linux platforms.

## Core Features

- **Zero-Code Deployment**: Double-click exe/Shell script to run directly. No Python environment, CUDA, or API keys required.
- **All-in-One Toolset**: Covers 5 major modules: AI Chat, AI Image Generation, Multimedia Processing, Office Tools, Code Assistant
- **Privacy First**: All data processed locally, never uploaded to cloud
- **Lightweight**: Runs local small models on laptops with 8GB RAM
- **Dual-Audience Design**: Ready-to-use for beginners, extensible for developers

## Feature Modules

### Module 1: All-Purpose AI Chat Engine
- Local Offline Models: One-click download of lightweight open-source models like Qwen/Llama3/Gemma
- Multi-API Aggregation: Unified configuration panel for OpenAI/Tongyi/Qianwen/Xunfei/DeepSeek
- Special Features: Role presets, conversation history, Markdown export, long document summarization

### Module 2: Multimedia AI Workstation
- AI Image Generation: Text-to-image/Image-to-image/Outpainting/Background removal
- Audio/Video: Speech-to-text, AI voiceover, video subtitle generation, audio denoising
- OCR: Text recognition from images/PDF/screenshots, formula/table extraction

### Module 3: Document & Office Tools
- PDF Toolkit: Split/Merge/Encrypt/Decrypt/Format conversion/AI summarization
- Word/Excel: AI batch processing, document proofreading, batch copywriting rewriting
- Exam/Notes: AI exam paper analysis, mind map generation

### Module 4: Developer Assistant
- Code Generation/Debugging/Commenting: Multi-language support (C/C++/Python/Java/JS)
- Project Scaffolding: Auto-generate frontend/backend templates from requirements
- API Testing: Lightweight Postman alternative

### Module 5: Plugin Ecosystem
- Open plugin SDK supporting third-party plugin integration
- Built-in plugin marketplace with one-click installation

## Quick Start

### Windows

```bash
# Double-click to run
Start.exe

# Or use command line
python main.py
```

### Linux/macOS

```bash
# Clone repository
git clone https://github.com/xxx/OpenAll-In-AI.git
cd OpenAll-In-AI

# Install dependencies
pip install -r requirements.txt

# Start
python main.py
```

### Docker Deployment (Linux)

```bash
docker build -t openall-in-ai .
docker run -p 8000:8000 openall-in-ai
```

Access `http://localhost:8000` to use the application.

## Technical Architecture

| Layer | Technology |
|-------|------------|
| Frontend | Vue3 + Element Plus |
| Backend | Python FastAPI |
| Model Inference | llama.cpp |
| Database | SQLite |
| Packaging | PyInstaller |

## Project Structure

```
OpenAll-In-AI/
├── backend/              # FastAPI Backend
│   ├── api/              # API Routes
│   ├── core/             # Core Configuration
│   ├── model_manager/    # Model Management
│   ├── services/         # Business Logic
│   └── plugins/          # Plugin System
├── frontend/             # Vue3 Frontend
│   └── src/
│       ├── api/          # API Calls
│       ├── views/        # Page Components
│       ├── stores/       # State Management
│       └── router/       # Router Configuration
├── plugins/              # Built-in Plugins
├── tests/               # Test Files
├── docs/                # Documentation
├── main.py              # Entry Point
└── README.md
```

## API Configuration

Supports multiple cloud-based LLM APIs, configurable in settings:

- **OpenAI**: GPT-3.5/GPT-4
- **Alibaba Tongyi Qianwen**: Qwen-Turbo/Qwen-Max
- **iFLYTEK Spark**: Spark Max
- **DeepSeek**: DeepSeek Chat

## System Requirements

### Minimum Requirements
- CPU: 4 cores
- Memory: 8GB RAM
- Storage: 10GB available space

### Recommended Requirements
- CPU: 8+ cores
- Memory: 16GB+ RAM
- GPU: NVIDIA 4GB+ (for local AI image generation)

## Development

### Environment Setup

```bash
# Clone repository
git clone https://github.com/xxx/OpenAll-In-AI.git
cd OpenAll-In-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Start Development Server

```bash
# Backend
cd OpenAll-In-AI
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html
```

## License

MIT License - Free for commercial use, open for secondary development

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xxx/OpenAll-In-AI&type=Date)](https://star-history.com/#xxx/OpenAll-In-AI&Date)

## Contributing

Welcome to submit Issues and PRs!

1. Fork this repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## Contact

- GitHub Issues: [https://github.com/luo1chen/OpenAll-In-AI/issues](https://github.com/luo1chen/OpenAll-In-AI/issues)
- Email:703879709@qq.com