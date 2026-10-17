import os
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class FALProvider:
    """
    FAL.ai provider for image/video generation.
    Uses fal_client SDK for async job submission.
    """
    
    def __init__(self, model: str = "fal-ai/flux/schnell"):
        self.model = model
        self.fal_key = os.getenv("FAL_KEY")
        
        if not self.fal_key:
            logger.warning("FAL_KEY not found in environment. FAL provider will fail at runtime.")
        
        # Lazy import to avoid dependency issues if fal_client not installed
        try:
            import fal_client
            self.fal_client = fal_client
            # Set the key for the fal_client library if it exists
            if self.fal_key:
                os.environ["FAL_KEY"] = self.fal_key
        except ImportError:
            logger.error("fal_client not installed. Run: pip install fal-client")
            self.fal_client = None
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"FAL ({self.model})",
            capabilities=[
                ProviderCapability.IMAGE_GENERATION,
                ProviderCapability.VIDEO_GENERATION,
            ],
            execution_mode=ExecutionMode.ASYNC,
            max_context=0,  # Not applicable
            cost_per_1k_tokens=0.0,  # Priced per image/video
            avg_latency_ms=5000,
            supports_streaming=False,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Synchronous wrapper for FAL image generation.
        Submits job and waits for result.
        """
        if not self.fal_client:
            raise RuntimeError("fal_client not available")
        
        arguments = {
            "prompt": prompt,
            "image_size": kwargs.get("image_size", "landscape_4_3"),
            "num_inference_steps": kwargs.get("num_inference_steps", 4),
            "num_images": kwargs.get("num_images", 1),
        }
        
        try:
            logger.info(f"FAL request: model={self.model}, prompt={prompt[:50]}...")
            
            # Submit and wait (synchronous)
            result = self.fal_client.subscribe(
                self.model,
                arguments=arguments,
                with_logs=False,
            )
            
            # Extract image URL
            images = result.get("images", [])
            if not images:
                raise ValueError("No images returned from FAL")
            
            image_url = images[0]["url"]
            
            return {
                "content": image_url,  # Return URL as content
                "model": self.model,
                "raw": result,
            }
        except Exception as e:
            logger.error(f"FAL error: {e}")
            raise
    
    def submit_job(self, prompt: str, **kwargs) -> str:
        """
        Async job submission (returns job_id).
        Use this for true async workflows.
        """
        if not self.fal_client:
            raise RuntimeError("fal_client not available")
        
        arguments = {
            "prompt": prompt,
            "image_size": kwargs.get("image_size", "landscape_4_3"),
            "num_inference_steps": kwargs.get("num_inference_steps", 4),
            "num_images": kwargs.get("num_images", 1),
        }
        
        try:
            handler = self.fal_client.submit(self.model, arguments=arguments)
            return handler.request_id
        except Exception as e:
            logger.error(f"FAL submit error: {e}")
            raise
            
    def check_balance(self) -> Dict[str, Any]:
        """
        Check FAL balance.
        """
        if not self.fal_client:
             return {"error": "fal_client not installed"}
             
        # FAL SDK doesn't always expose balance directly in a stable way.
        # We will try a known endpoint via direct request if SDK method is missing.
        import requests
        try:
            # We must use the key directly
            if not self.fal_key:
                return {"error": "No FAL_KEY"}
                
            # Unofficial/Stable route for user balance?
            # Or just return a link to the dashboard if API is private.
            # Let's try to list queue/usage if possible, or leave as placeholder.
            # Official docs don't document a balance endpoint for keys.
            return {"note": "Balance check not supported via API key. Visit fal.ai/dashboard"}
            
        except Exception as e:
            return {"error": str(e)}
