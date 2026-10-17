import os
from dataclasses import dataclass
from typing import Dict, Optional, List

from router.providers.openrouter_provider import OpenRouterProvider
from router.providers.google_gemini_provider import GoogleGeminiProvider
from router.providers.fal_provider import FALProvider
from router.providers.coinbase_provider import CoinbaseProvider
from router.providers.schwab_provider import SchwabProvider
from router.providers.schwab_provider import SchwabProvider
from router.providers.longcat_provider import LongCatProvider
from router.providers.fal_video_provider import FALVideoProvider
from router.providers.ollama_provider import OllamaProvider



@dataclass(frozen=True)
class ProviderIDs:
    # LLMs (sync)
    OPENROUTER_DEEPSEEK_V3: str = "openrouter_deepseek_v3"
    OPENROUTER_DEEPSEEK_R1: str = "openrouter_deepseek_r1"
    OPENROUTER_KIMI: str = "openrouter_kimi"
    GOOGLE_GEMINI_FLASH: str = "google_gemini_flash"
    GOOGLE_GEMINI_PRO: str = "google_gemini_pro"

    # Media (sync wrapper for now)
    FAL_FLUX_SCHNELL: str = "fal_flux_schnell"
    FAL_VIDEO_MINIMAX: str = "fal_video_minimax"
    
    # Financial
    COINBASE: str = "coinbase"
    SCHWAB: str = "schwab"
    
    # Avatars
    LONGCAT: str = "longcat_avatar"

    # Local Offline / Edge
    OLLAMA_LOCAL: str = "ollama_local"



class ProviderRegistry:
    """
    Central place to initialize and retrieve providers.
    - Reads env keys
    - Builds provider instances
    - Keeps them ready for policy/executor selection
    """

    def __init__(self):
        self.providers: Dict[str, object] = {}
        self._init_providers()

    def _init_providers(self) -> None:
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")

        # Optional override knobs
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        gemini_pro_model = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-flash") # [FIX] Fallback to Flash to avoid 404s
        fal_model = os.getenv("FAL_IMAGE_MODEL", "fal-ai/flux/schnell")
        fal_video_model = os.getenv("FAL_VIDEO_MODEL", "fal-ai/minimax-video")
        
        # Financial Keys
        coinbase_key = os.getenv("COINBASE_API_KEY")
        coinbase_secret = os.getenv("COINBASE_API_SECRET")

        # OpenRouter providers
        if openrouter_key:
            self.providers[ProviderIDs.OPENROUTER_DEEPSEEK_V3] = OpenRouterProvider(
                api_key=openrouter_key,
                model=os.getenv("OPENROUTER_MODEL_V3", "deepseek/deepseek-chat"),
            )
            self.providers[ProviderIDs.OPENROUTER_DEEPSEEK_R1] = OpenRouterProvider(
                api_key=openrouter_key,
                model=os.getenv("OPENROUTER_MODEL_R1", "deepseek/deepseek-r1"),
            )
            # [NEW] Kimi (Moonshot) for Research
            self.providers[ProviderIDs.OPENROUTER_KIMI] = OpenRouterProvider(
                api_key=openrouter_key,
                model=os.getenv("OPENROUTER_MODEL_KIMI", "moonshotai/moonshot-v1-8k"),
            )

        # Google Gemini provider (REST)
        if google_key:
            self.providers[ProviderIDs.GOOGLE_GEMINI_FLASH] = GoogleGeminiProvider(
                api_key=google_key,
                model=gemini_model,
            )
            self.providers[ProviderIDs.GOOGLE_GEMINI_PRO] = GoogleGeminiProvider(
                api_key=google_key,
                model=gemini_pro_model,
            )

        # FAL provider (uses env FAL_KEY internally)
        # If no FAL_KEY exists, calling it will fail at runtime (as expected).
        self.providers[ProviderIDs.FAL_FLUX_SCHNELL] = FALProvider(model=fal_model)
        self.providers[ProviderIDs.FAL_VIDEO_MINIMAX] = FALVideoProvider(model=fal_video_model)

        # Financial Providers
        if coinbase_key and coinbase_secret:
             self.providers[ProviderIDs.COINBASE] = CoinbaseProvider(api_key=coinbase_key, api_secret=coinbase_secret)
        
        # Schwab (always init, handles own auth/path check)
        self.providers[ProviderIDs.SCHWAB] = SchwabProvider()

        # Long Cat AI
        longcat_key = os.getenv("LONGCAT_API_KEY")
        if longcat_key:
            self.providers[ProviderIDs.LONGCAT] = LongCatProvider(api_key=longcat_key)

        # Local Ollama AI
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "gemma2:2b")
        self.providers[ProviderIDs.OLLAMA_LOCAL] = OllamaProvider(
            base_url=ollama_url,
            model=ollama_model
        )


    def has(self, provider_id: str) -> bool:
        return provider_id in self.providers

    def get(self, provider_id: str):
        p = self.providers.get(provider_id)
        if not p:
            raise KeyError(f"Provider not registered: {provider_id}")
        return p

    def list_ids(self) -> List[str]:
        return list(self.providers.keys())

    def list_providers(self):
        return list(self.providers.values())
