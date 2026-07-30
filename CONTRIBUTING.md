# 🤝 Contributing to OpenAll-In-AI

First off, thank you for considering contributing to OpenAll-In-AI! It's people like you that make this toolbox amazing.

## 🌟 Ways to Contribute

### 1. Bug Reports
- Use the GitHub issue tracker to report bugs
- Please include: OS version, Python version, steps to reproduce, expected vs actual behavior
- Check if similar issues already exist before creating a new one

### 2. Feature Requests
- Suggest new features or improvements
- Describe the use case and how it would benefit users
- Check the roadmap first to avoid duplicates

### 3. Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/OpenAll-In-AI.git
cd OpenAll-In-AI

# Add the original repository as upstream
git remote add upstream https://github.com/luo1chen/OpenAll-In-AI.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# Run tests
pytest tests/ -v
```

## 📋 Pull Request Process

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/amazing-feature main
   ```

2. **Make your changes** and ensure they follow existing code style

3. **Write tests** for new functionality:
   ```bash
   pytest tests/ -v
   ```

4. **Update documentation** if you're changing behavior or adding features

5. **Push your branch** and submit a PR

6. **Wait for review** - We'll review your PR within 48 hours

### PR Checklist

- [ ] My code follows the project's style guidelines
- [ ] I've written tests for new functionality
- [ ] All existing tests pass
- [ ] I've updated the documentation if necessary
- [ ] My changes don't break existing functionality
- [ ] I've described what and why in my PR description

## 🎨 Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

### Vue/TypeScript (Frontend)
- Follow Vue 3 Composition API style
- Use `<script setup>` syntax
- Use TypeScript with proper typing
- Keep components small and focused

## 🔄 Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/<name>` | `feature/pdf-merge` |
| Bugfix | `fix/<name>` | `fix/chat-timeout` |
| Hotfix | `hotfix/<name>` | `hotfix/login-error` |
| Release | `release/v<version>` | `release/v1.1.0` |

## 📝 Commit Messages

Write clear, descriptive commit messages:

```
feat: Add PDF merge functionality
fix: Resolve chat timeout on slow connections
docs: Update API documentation
refactor: Clean up model inference code
test: Add tests for plugin loader
```

## 💬 Getting Help

If you have questions, feel free to:
- Open a GitHub Discussion
- Check existing issues and PRs
- Email: 703879709@qq.com

---

Thank you for contributing! 🎉