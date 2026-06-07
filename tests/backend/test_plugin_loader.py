"""
Tests for plugin loader
"""
import pytest
from backend.plugins.loader import PluginLoader


def test_list_plugins():
    """Test listing plugins"""
    loader = PluginLoader()
    plugins = loader.list_plugins()

    assert len(plugins) >= 2  # Built-in plugins
    assert any(p["id"] == "builtin-translation" for p in plugins)


def test_get_plugin():
    """Test getting plugin details"""
    loader = PluginLoader()

    plugin = loader.get_plugin("builtin-translation")
    assert plugin is not None
    assert plugin["name"] == "AI Translation"


def test_get_nonexistent_plugin():
    """Test getting non-existent plugin"""
    loader = PluginLoader()

    plugin = loader.get_plugin("nonexistent-plugin")
    assert plugin is None


def test_enable_plugin():
    """Test enabling a plugin"""
    loader = PluginLoader()

    result = loader.enable_plugin("builtin-translation")
    assert result is True

    plugin = loader.get_plugin("builtin-translation")
    assert plugin["enabled"] is True


def test_disable_plugin():
    """Test disabling a plugin"""
    loader = PluginLoader()

    result = loader.disable_plugin("builtin-translation")
    assert result is True

    plugin = loader.get_plugin("builtin-translation")
    assert plugin["enabled"] is False


@pytest.mark.asyncio
async def test_install_plugin():
    """Test installing a plugin"""
    loader = PluginLoader()

    result = await loader.install_plugin("test-plugin", "1.0.0")
    assert result["status"] == "installed"


@pytest.mark.asyncio
async def test_install_existing_plugin():
    """Test installing already installed plugin"""
    loader = PluginLoader()

    result = await loader.install_plugin("builtin-translation")
    assert result["status"] == "already_installed"


@pytest.mark.asyncio
async def test_uninstall_plugin():
    """Test uninstalling a plugin"""
    loader = PluginLoader()

    # First install a plugin
    await loader.install_plugin("test-plugin-uninstall")

    # Then uninstall it
    result = await loader.uninstall_plugin("test-plugin-uninstall")
    assert result is True


@pytest.mark.asyncio
async def test_cannot_uninstall_builtin_plugin():
    """Test that built-in plugins cannot be uninstalled"""
    loader = PluginLoader()

    result = await loader.uninstall_plugin("builtin-translation")
    assert result is False


def test_list_market_plugins():
    """Test listing market plugins"""
    loader = PluginLoader()
    plugins = loader.list_market_plugins()

    assert "plugins" in plugins
    assert isinstance(plugins["plugins"], list)
