import os
import sys
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Ensure root is in path for imports if running standalone
current_dir = os.path.dirname(os.path.abspath(__file__))
aergia_root = os.path.dirname(current_dir)
if aergia_root not in sys.path:
    sys.path.append(aergia_root)

# Import schemas, registry, and utils
from router.schemas import TaskRequest
from router.base_provider import BaseProvider
from router.registry import ProviderRegistry, ProviderIDs
from router.utils import clean_markdown_fences

load_dotenv()
logging.basicConfig(level=logging.INFO)

class Router:
    def __init__(self):
        # Auto-initialize via Registry
        self.registry = ProviderRegistry()

    def route(self, request: TaskRequest) -> Dict[str, Any]:
        """
        Executor:
        1. Selects best provider via Policy.
        2. Executes the request.
        """
        provider = self._select_provider(request)
        if not provider:
            error_msg = f"No suitable provider found for task type: {request.task_type}"
            logging.error(error_msg)
            return {"error": error_msg}

        logging.info(f"Router: Selected '{provider.get_metadata().name}' for task '{request.task_type}'")

        try:
            # Sync Execution
            response = provider.generate(
                prompt=request.prompt,
                system_prompt=request.system_prompt,
                **request.payload
            )
            
            # Clean text content if present (for code blocks etc)
            if "content" in response and isinstance(response["content"], str):
                 response["content"] = clean_markdown_fences(response["content"])
                 
            return response

        except Exception as e:
            logging.error(f"Router Execution Error: {e}")
            return {"error": str(e)}

    def _select_provider(self, request: TaskRequest) -> Optional[BaseProvider]:
        """
        Policy Engine:
        Delegates to Registry lookup based on task type rules.
        """
        t_type = request.task_type.lower()
        reg = self.registry
        ids = ProviderIDs

        # 1. IMAGE / VIDEO
        if "image" in t_type or "video" in t_type:
            return reg.get(ids.FAL_FLUX_SCHNELL) if reg.has(ids.FAL_FLUX_SCHNELL) else None

        # 2. REASONING (Deep Thinking)
        if t_type == "reasoning":
            if reg.has(ids.OPENROUTER_DEEPSEEK_R1):
                return reg.get(ids.OPENROUTER_DEEPSEEK_R1)
            # Fallback to V3
            return reg.get(ids.OPENROUTER_DEEPSEEK_V3) if reg.has(ids.OPENROUTER_DEEPSEEK_V3) else None

        # 3. CODING / LOGIC
        if t_type == "coding" or t_type == "code_generation":
            # Prefer V3 (Smart/Fast)
            if reg.has(ids.OPENROUTER_DEEPSEEK_V3):
                return reg.get(ids.OPENROUTER_DEEPSEEK_V3)
            # Fallback to Gemini
            return reg.get(ids.GOOGLE_GEMINI_FLASH) if reg.has(ids.GOOGLE_GEMINI_FLASH) else None

        # 4. CONTEXT (Large Documents)
        if t_type == "context":
            # Prefer Gemini Flash (Big Window)
            if reg.has(ids.GOOGLE_GEMINI_FLASH):
                return reg.get(ids.GOOGLE_GEMINI_FLASH)
            return reg.get(ids.OPENROUTER_DEEPSEEK_V3) if reg.has(ids.OPENROUTER_DEEPSEEK_V3) else None

        # 5. GENERAL DEFAULT
        # Prefer V3
        if reg.has(ids.OPENROUTER_DEEPSEEK_V3):
            return reg.get(ids.OPENROUTER_DEEPSEEK_V3)
        # Fallback to Gemini
        return reg.get(ids.GOOGLE_GEMINI_FLASH) if reg.has(ids.GOOGLE_GEMINI_FLASH) else None

# Singleton instance
global_router = Router()
