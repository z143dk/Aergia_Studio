import requests
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class OllamaProvider:
    """
    Local Ollama provider for offline / free model execution.
    Connects to the local Ollama instance running at base_url.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma2:2b"):
        self.base_url = base_url.rstrip('/')
        self.model = model
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"Ollama Local ({self.model})",
            capabilities=[
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.CODE_GENERATION,
                ProviderCapability.REASONING,
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=8192,
            cost_per_1k_tokens=0.0,  # 100% Free / Local!
            avg_latency_ms=800,
            supports_streaming=True,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Synchronous text generation via local Ollama API.
        """
        url = f"{self.base_url}/api/generate"
        
        # Format payload according to Ollama API specs
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        }
        
        # Optional config overrides
        if "temperature" in kwargs or "max_tokens" in kwargs:
            payload["options"] = {}
            if "temperature" in kwargs:
                payload["options"]["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                payload["options"]["num_predict"] = kwargs["max_tokens"]
        
        try:
            logger.info(f"Local Ollama request: url={url} model={self.model}")
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            content = data.get("response", "")
            
            return {
                "content": content,
                "model": self.model,
                "raw": data,
            }
        except Exception as e:
            logger.error(f"Local Ollama error: {e}")
            raise
            
    def submit_job(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("Ollama is a synchronous provider")
