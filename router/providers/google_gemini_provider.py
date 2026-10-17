import requests
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class GoogleGeminiProvider:
    """
    Google Gemini provider using REST API.
    Supports Gemini 1.5 Flash and Pro models.
    """
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash-001"):
        self.api_key = api_key
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"Google Gemini ({self.model})",
            capabilities=[
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.CODE_GENERATION,
                ProviderCapability.REASONING,
                ProviderCapability.MULTIMODAL,
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=1000000 if "flash" in self.model else 128000,
            cost_per_1k_tokens=0.075,
            avg_latency_ms=1500,
            supports_streaming=True,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Synchronous text generation via Gemini REST API.
        """
        # Combine system prompt and user prompt
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ]
        }
        
        # Optional parameters
        if "temperature" in kwargs or "max_tokens" in kwargs:
            payload["generationConfig"] = {}
            if "temperature" in kwargs:
                payload["generationConfig"]["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                payload["generationConfig"]["maxOutputTokens"] = kwargs["max_tokens"]
        
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            logger.info(f"Gemini request: model={self.model}")
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            
            return {
                "content": content,
                "model": self.model,
                "raw": data,
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
    
    def submit_job(self, prompt: str, **kwargs) -> str:
        """
        Not applicable for sync LLM providers.
        """
        raise NotImplementedError("Gemini is a synchronous provider")
