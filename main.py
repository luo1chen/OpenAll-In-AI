"""
OpenAll-In-AI Main Entry Point
Unified startup script for the application
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn
    from backend.core.config import settings

    print(f"""
╔══════════════════════════════════════════════════════════╗
║                  OpenAll-In-AI v1.0.0                    ║
║              一站式本地部署AI聚合工具箱                    ║
╚══════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "backend.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload
    )
