"""
Model inference engine
"""
from typing import Any, Dict, Optional

import httpx


class ModelInference:
    """Unified interface for model inference"""

    def __init__(self):
        self._local_models: Dict[str, Any] = {}

    async def generate(
        self,
        prompt: str,
        model: str = "qwen2.5-7b",
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate response from model"""
        # Check if it's a local model or API model
        if self._is_local_model(model):
            return await self._local_generate(prompt, model, system_prompt, **kwargs)
        else:
            return await self._api_generate(prompt, model, system_prompt, **kwargs)

    def _is_local_model(self, model: str) -> bool:
        """Check if model is a local model"""
        local_prefixes = ["qwen", "llama", "gemma", "phi", "mistral"]
        return any(model.lower().startswith(prefix) for prefix in local_prefixes)

    async def _local_generate(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate using local model"""
        # Placeholder - actual implementation would use llama.cpp
        return f"[Local Model {model}] Response to: {prompt[:50]}..."

    async def _api_generate(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate using API (OpenAI, Dashscope, etc.)"""
        # Determine which API to use based on model name
        if "gpt" in model.lower():
            return await self._call_openai(prompt, model, system_prompt, **kwargs)
        elif "qwen" in model.lower():
            return await self._call_dashscope(prompt, model, system_prompt, **kwargs)
        elif "deepseek" in model.lower():
            return await self._call_deepseek(prompt, model, system_prompt, **kwargs)
        else:
            return f"[API Model {model}] Response to: {prompt[:50]}..."

    async def _call_openai(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call OpenAI API"""
        from backend.core.config import settings

        if not settings.apis.openai.enabled:
            return "OpenAI API not enabled"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.apis.openai.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.apis.openai.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        **kwargs
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"OpenAI API error: {str(e)}"

    async def _call_dashscope(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call Alibaba Dashscope API"""
        from backend.core.config import settings

        if not settings.apis.dashscope.enabled:
            return "Dashscope API not enabled"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.apis.dashscope.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.apis.dashscope.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        **kwargs
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Dashscope API error: {str(e)}"

    async def _call_deepseek(
        self,
        prompt: str,
        model: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call DeepSeek API"""
        from backend.core.config import settings

        if not settings.apis.deepseek.enabled:
            return "DeepSeek API not enabled"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.apis.deepseek.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.apis.deepseek.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        **kwargs
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"DeepSeek API error: {str(e)}"
