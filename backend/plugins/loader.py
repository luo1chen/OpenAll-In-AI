"""
Plugin loader for managing plugins
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class PluginManifest:
    """Plugin manifest information"""
    id: str
    name: str
    version: str
    description: str
    author: str
    main: str
    dependencies: List[str]


@dataclass
class Plugin:
    """Loaded plugin instance"""
    manifest: PluginManifest
    module: Any
    enabled: bool


class PluginLoader:
    """Loader for managing plugins"""

    def __init__(self):
        self.plugins_dir = Path("./plugins")
        self.plugins_dir.mkdir(exist_ok=True)
        self._plugins: Dict[str, Plugin] = {}
        self._load_builtin_plugins()

    def _load_builtin_plugins(self):
        """Load built-in plugins"""
        # Built-in translation plugin
        self._plugins["builtin-translation"] = Plugin(
            manifest=PluginManifest(
                id="builtin-translation",
                name="AI Translation",
                version="1.0.0",
                description="AI-powered translation plugin",
                author="OpenAll-In-AI",
                main="translation",
                dependencies=[]
            ),
            module=None,
            enabled=True
        )

        # Built-in web scraping plugin
        self._plugins["builtin-scraper"] = Plugin(
            manifest=PluginManifest(
                id="builtin-scraper",
                name="Web Scraper",
                version="1.0.0",
                description="Simple web scraping tool",
                author="OpenAll-In-AI",
                main="scraper",
                dependencies=["requests"]
            ),
            module=None,
            enabled=True
        )

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins"""
        return [
            {
                "id": p.manifest.id,
                "name": p.manifest.name,
                "version": p.manifest.version,
                "description": p.manifest.description,
                "author": p.manifest.author,
                "enabled": p.enabled
            }
            for p in self._plugins.values()
        ]

    def list_market_plugins(self) -> List[Dict[str, Any]]:
        """List plugins available in the market"""
        # Simulated market plugins
        return [
            {
                "id": "market-translator-pro",
                "name": "Translator Pro",
                "version": "2.0.0",
                "description": "Professional translation with more languages",
                "author": "Community"
            },
            {
                "id": "market-cloud-storage",
                "name": "Cloud Storage",
                "version": "1.5.0",
                "description": "Connect to cloud storage services",
                "author": "Community"
            }
        ]

    def get_plugin(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get plugin details"""
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return None

        return {
            "id": plugin.manifest.id,
            "name": plugin.manifest.name,
            "version": plugin.manifest.version,
            "description": plugin.manifest.description,
            "author": plugin.manifest.author,
            "enabled": plugin.enabled,
            "main": plugin.manifest.main
        }

    async def install_plugin(self, plugin_id: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Install a plugin"""
        # Check if already installed
        if plugin_id in self._plugins:
            return {
                "status": "already_installed",
                "message": f"Plugin {plugin_id} is already installed"
            }

        # Create a placeholder plugin
        self._plugins[plugin_id] = Plugin(
            manifest=PluginManifest(
                id=plugin_id,
                name=f"Plugin {plugin_id}",
                version=version or "1.0.0",
                description="Installed plugin",
                author="Unknown",
                main="main",
                dependencies=[]
            ),
            module=None,
            enabled=True
        )

        return {
            "status": "installed",
            "message": f"Plugin {plugin_id} installed successfully"
        }

    async def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin"""
        if plugin_id not in self._plugins:
            return False

        # Don't allow uninstalling built-in plugins
        if plugin_id.startswith("builtin-"):
            return False

        del self._plugins[plugin_id]
        return True

    def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin"""
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return False

        plugin.enabled = True
        return True

    def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin"""
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return False

        plugin.enabled = False
        return True
