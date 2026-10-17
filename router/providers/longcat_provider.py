import os
import logging
import requests
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class LongCatProvider:
    """
    LongCat Chat Provider (LLM/Text).
    Compatible with OpenAI Chat Completions API.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("LONGCAT_API_KEY")
        self.base_url = "https://api.longcat.chat/v1" 
        self.model = "gpt-3.5-turbo" # Default fallback, user can override
        
        if not self.api_key:
            logger.warning("LONGCAT_API_KEY not found.")
            
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name="LongCat Chat",
            capabilities=[
                ProviderCapability.CODING,
                ProviderCapability.CREATIVE,
                ProviderCapability.REASONING
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=4096,
            cost_per_1k_tokens=0.0,
            avg_latency_ms=1000,
            supports_streaming=False,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Text generation via LongCat Chat.
        """
        if not self.api_key:
            raise RuntimeError("LONGCAT_API_KEY not configured")
            
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Try generic OpenAI payload
        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        try:
            logger.info(f"LongCat Text request: {prompt[:50]}...")
            # We try the standard chat completion endpoint
            res = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=30)
            
            if res.status_code != 200:
                 raise ValueError(f"LongCat API Error ({res.status_code}): {res.text}")
                
            data = res.json()
            content = data["choices"][0]["message"]["content"]
            
            return {
                "content": content,
                "model": data.get("model", "longcat"),
                "raw": data
            }
            
        except Exception as e:
            logger.error(f"LongCat text error: {e}")
            raise
