import os
import logging
from typing import Dict, Any
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode

logger = logging.getLogger(__name__)

class FALVideoProvider:
    """
    FAL.ai provider for AI VIDEO generation (Image-to-Video).
    Target Models: 
    - fal-ai/minimax-video (Default)
    - fal-ai/kling-video
    - fal-ai/luma-dream-machine
    """
    
    def __init__(self, model: str = "fal-ai/minimax-video"):
        self.model = model
        self.fal_key = os.getenv("FAL_KEY")
        
        if not self.fal_key:
            logger.warning("FAL_KEY not found in environment. FAL Video provider will fail at runtime.")
        
        try:
            import fal_client
            self.fal_client = fal_client
            if self.fal_key:
                os.environ["FAL_KEY"] = self.fal_key
        except ImportError:
            logger.error("fal_client not installed. Run: pip install fal-client")
            self.fal_client = None
    
    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"FAL Video ({self.model})",
            capabilities=[
                ProviderCapability.VIDEO_GENERATION,
                ProviderCapability.MULTIMODAL,
            ],
            execution_mode=ExecutionMode.ASYNC, # Video takes time
            max_context=0,
            cost_per_1k_tokens=0.0,
            avg_latency_ms=60000, # ~1 minute typically
            supports_streaming=False,
        )
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """
        Synchronous wrapper for FAL Video generation.
        Requires 'prompt' and optional 'image_url' for Image-to-Video.
        """
        if not self.fal_client:
            raise RuntimeError("fal_client not available")
        
        image_url = kwargs.get("image_url")
        if not image_url:
            # Text-to-Video mode (if supported by model)
            # Minimax supports text-to-video? Yes.
            pass

        arguments = {
            "prompt": prompt,
        }
        
        if image_url:
            arguments["image_url"] = image_url
            
        # Model specific tweaks
        # Kling uses 'image_url'
        # Minimax uses 'image_url'
        # Luma uses 'image_url'
        
        try:
            logger.info(f"FAL Video request: model={self.model}, prompt={prompt[:40]}..., image={image_url}")
            
            # Submit and wait
            result = self.fal_client.subscribe(
                self.model,
                arguments=arguments,
                with_logs=True,
            )
            
            # Extract Video URL
            # Minimax returns: {'video': {'url': '...', 'content_type': 'video/mp4'}}
            # Kling returns: {'video': {'url': '...'}}
            
            video_data = result.get("video")
            if not video_data:
                # Fallback check
                if "video_url" in result:
                     video_url = result["video_url"]
                else:
                    raise ValueError(f"No video returned from FAL: {result.keys()}")
            else:
                video_url = video_data.get("url")

            return {
                "content": video_url,
                "model": self.model,
                "raw": result,
            }
        except Exception as e:
            logger.error(f"FAL Video error: {e}")
            raise
