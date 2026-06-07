"""
Plugins API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List

from backend.core.database import get_db
from backend.plugins.loader import PluginLoader

router = APIRouter()


class PluginInfo(BaseModel):
    id: str
    name: str
    version: str
    description: str
    author: str
    enabled: bool


class PluginManifest(BaseModel):
    id: str
    name: str
    version: str
    description: str
    author: str
    main: str
    dependencies: List[str] = []


def get_plugin_loader() -> PluginLoader:
    return PluginLoader()


@router.get("")
async def list_plugins(loader: PluginLoader = Depends(get_plugin_loader)):
    """List all installed plugins"""
    plugins = loader.list_plugins()
    return plugins


@router.get("/market")
async def list_market_plugins(loader: PluginLoader = Depends(get_plugin_loader)):
    """List plugins available in the market"""
    plugins = loader.list_market_plugins()
    return {"plugins": plugins}


@router.get("/{plugin_id}")
async def get_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader)
):
    """Get plugin details"""
    plugin = loader.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return plugin


@router.post("/install")
async def install_plugin(
    plugin_id: str,
    version: Optional[str] = None,
    loader: PluginLoader = Depends(get_plugin_loader)
):
    """Install a plugin"""
    result = await loader.install_plugin(plugin_id, version)
    return result


@router.post("/uninstall")
async def uninstall_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader)
):
    """Uninstall a plugin"""
    success = await loader.uninstall_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return {"status": "uninstalled"}


@router.post("/enable/{plugin_id}")
async def enable_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader)
):
    """Enable a plugin"""
    success = loader.enable_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return {"status": "enabled"}


@router.post("/disable/{plugin_id}")
async def disable_plugin(
    plugin_id: str,
    loader: PluginLoader = Depends(get_plugin_loader)
):
    """Disable a plugin"""
    success = loader.disable_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return {"status": "disabled"}
