from abc import ABC, abstractmethod
from typing import Dict, Any
from .schemas import ProviderMetadata

class BaseProvider(ABC):
    @abstractmethod
    def get_metadata(self) -> ProviderMetadata:
        """Returns the capabilities and stats of this provider."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> Dict[str, Any]:
        """Synchronous execution (for LLMs)."""
        pass
    
    @abstractmethod
    def submit_job(self, prompt: str, **kwargs) -> str:
        """Asynchronous submission (for Video/Images)."""
        pass
