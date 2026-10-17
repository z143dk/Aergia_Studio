import requests
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class OpenRouterProvider:
    """
    OpenRouter provider for LLM inference.
    Supports DeepSeek V3, DeepSeek R1, and other models via OpenRouter API.
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"OpenRouter ({self.model})",
            capabilities=[
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.CODE_GENERATION,
                ProviderCapability.REASONING,
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=64000 if "deepseek" in self.model.lower() else 8000,
            cost_per_1k_tokens=0.14 if "deepseek-chat" in self.model else 0.55,
            avg_latency_ms=2000,
            supports_streaming=True,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Synchronous text generation via OpenRouter.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        # Optional parameters
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            logger.info(f"OpenRouter request: model={self.model}")
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            return {
                "content": content,
                "model": self.model,
                "raw": data,
            }
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            raise
    
    def submit_job(self, prompt: str, **kwargs) -> str:
        """
        Not applicable for sync LLM providers.
        """
        raise NotImplementedError("OpenRouter is a synchronous provider")

    def check_credits(self) -> Dict[str, Any]:
        """
        Check API key credits/usage.
        """
        try:
            url = "https://openrouter.ai/api/v1/auth/key"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                # Data format: {'data': {'limit': X, 'usage': Y, 'rate_limit': ...}}
                # 'limit' might be null for infinite, or a number.
                # 'usage' is total usage.
                # OpenRouter doesn't always show "balance directly" via this, but showing usage/limit is helpful.
                # Actually OpenRouter UI shows credits, but API mostly shows usage/limit.
                return data.get("data", {})
            return {"error": f"Status {resp.status_code}"}
        except Exception as e:
            logger.error(f"OpenRouter credit check failed: {e}")
            return {"error": str(e)}
