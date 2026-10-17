# AERGIA STUDIO PROPRIETARY CODEBASE (V2 Intelligence)
Generated on Aergia_Studio

## File: aergia_dashboard.py
```python
import customtkinter as ctk
import subprocess
import os
import threading
import sys
import webbrowser
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AergiaDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Aergia OS - Command Center")
        self.geometry("1000x800")
        
        # Set Window Icon (Taskbar)
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "aergia_icon.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon load error: {e}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Content Frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self.label = ctk.CTkLabel(self.main_frame, text="THE AERGIA PANTHEON", font=("Roboto Medium", 32))
        self.label.pack(pady=20)
        
        self.label.pack(pady=20)

        # Brain Bar (The Intelects)
        self.brain_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.brain_frame.pack(fill="x", pady=(0, 20))
        self.brain_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # 1. ChatLLM -> Project Athena (Strategy)
        self.btn_chatllm = ctk.CTkButton(self.brain_frame, text="🧠 Project Athena\n(ChatLLM Strategy)", 
                                         fg_color="#2E2B5F", hover_color="#1A1840",
                                         height=60, command=self.open_chatllm)
        self.btn_chatllm.grid(row=0, column=0, padx=5, sticky="ew")

        # 2. Gemini -> Project Prometheus (Forethought)
        self.btn_gemini = ctk.CTkButton(self.brain_frame, text="🔥 Project Prometheus\n(Gemini Thinking)", 
                                        fg_color="#1A73E8", hover_color="#1557B0",
                                        height=60, command=self.open_gemini)
        self.btn_gemini.grid(row=0, column=1, padx=5, sticky="ew")

        # 3. Antigravity -> Project Hephaestus (The Forge)
        self.btn_gravity = ctk.CTkButton(self.brain_frame, text="⚒️ Project Hephaestus\n(Antigravity Forge)", 
                                         fg_color="#0F9D58", hover_color="#0B8043",
                                         height=60, command=self.open_antigravity)
        self.btn_gravity.grid(row=0, column=2, padx=5, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.main_frame, text="System Online", font=("Roboto", 14), text_color="gray")
        self.status_label.pack(pady=(0, 20))

        # Buttons Grid Frame
        self.grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure Grid (3x3)
        self.grid_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_frame.grid_rowconfigure((0, 1, 2), weight=1)

        # --- ROW 0: ACTIVE PROJECTS ---
        self.create_button(0, 0, "Project Midas\n(Trading Engine)", "#D4AF37", "#B5952F", self.launch_midas)
        self.create_button(0, 1, "Project Chimera\n(Video Engine)", "#800080", "#600060", self.launch_chimera)
        self.create_button(0, 2, "Project Hyperion\n(AI Director)", "#008080", "#006060", self.launch_hyperion)

        # --- ROW 1: PLANNED PROJECTS ---
        self.create_button(1, 0, "Project Aura\n(Edge AI / Jetson)", "#4682B4", "#36648B", lambda: self.placeholder("Aura"))
        self.create_button(1, 1, "Project Hestia\n(Home & Health)", "#E9967A", "#CD853F", lambda: self.placeholder("Hestia"))
        self.create_button(1, 2, "Project Hermes\n(Messenger / Comms)", "#CDCD00", "#8B8B00", lambda: self.placeholder("Hermes"))

        # --- ROW 2: FUTURE / LEGACY ---
        self.create_button(2, 0, "Project Kairos\n(Scheduling)", "#708090", "#607080", lambda: self.placeholder("Kairos"))
        self.create_button(2, 1, "Project Morai\n(Predictive AI)", "#9370DB", "#7B68EE", lambda: self.placeholder("Morai"))
        self.create_button(2, 2, "Project Plutus\n(Legacy Archive)", "#A9A9A9", "#696969", lambda: self.placeholder("Plutus"))
        
        # Footer
        self.footer = ctk.CTkLabel(self.main_frame, text="v1.1 - Full Ecosystem Map", font=("Roboto", 10))
        self.footer.pack(side="bottom", pady=10)

    def create_button(self, row, col, text, color, hover, cmd):
        btn = ctk.CTkButton(self.grid_frame, text=text, command=cmd, 
                            font=("Roboto", 14), height=80,
                            fg_color=color, hover_color=hover)
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def run_script(self, cmd_list, cwd):
        try:
            subprocess.Popen(cmd_list, cwd=cwd, shell=True)
            self.status_label.configure(text=f"Launched: {cmd_list[0]}", text_color="#00FF00")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
            
    def placeholder(self, name):
        self.status_label.configure(text=f"Project {name} is currently Offline/Planned.", text_color="orange")

    def launch_midas(self):
        midas_dir = os.path.join(os.getcwd(), "Project Midas")
        target = "midas_home.py"
        if not os.path.exists(os.path.join(midas_dir, target)):
             self.status_label.configure(text="Midas Home not found!", text_color="red")
             return
        self.status_label.configure(text="Launching Midas...", text_color="yellow")
        # Use sys.executable to ensure we use the same python interpreter
        self.run_script(f'"{sys.executable}" "{target}"', midas_dir)

    def launch_chimera(self):
        # Launches the Full Studio (Backend + Worker + GUI)
        studio_bat = os.path.abspath("launch_studio.bat")
        if os.path.exists(studio_bat):
            self.status_label.configure(text="Launching Aergia Studio...", text_color="yellow")
            self.status_label.configure(text="Launching Aergia Studio...", text_color="yellow")
            try:
                os.startfile(studio_bat)
            except Exception as e:
                self.status_label.configure(text=f"Launch Error: {e}", text_color="red")
        else:
            self.status_label.configure(text="launch_studio.bat not found!", text_color="red")

    def launch_hyperion(self):
        # Hyperion is part of the Studio now
        self.launch_chimera()

    def open_chatllm(self):
        webbrowser.open("https://apps.abacus.ai/chatllm/?appId=15f718eedc")
        self.status_label.configure(text="Opening ChatLLM Strategy Brain...", text_color="#00FF00")

    def open_gemini(self):
        webbrowser.open("https://gemini.google.com/app")
        self.status_label.configure(text="Opening Gemini...", text_color="#1A73E8")

    def open_antigravity(self):
        # Antigravity "yourself" -> Opens the local project folder
        try:
            os.startfile(os.getcwd())
            self.status_label.configure(text="Opening Project Files...", text_color="#0F9D58")
        except Exception as e:
            self.status_label.configure(text=f"Error opening folder: {e}", text_color="red")

if __name__ == "__main__":
    app = AergiaDashboard()
    app.mainloop()

```

## File: intelligence_router.py
```python
import os
import logging
from enum import Enum
from dotenv import load_dotenv

from router.schemas import TaskRequest
from router.registry import ProviderRegistry
from router.policy import PolicyEngine
from router.executor import ExecutionEngine
from router.planner import Planner

# -----------------------------------------------------------------------------
# Env loading
# -----------------------------------------------------------------------------
# Keep your current behavior, but make it safer:
# 1) If AERGIA_ENV_PATH is set, load that
# 2) Else try your existing hardcoded path
# 3) Else try a local .env in the current working directory
ENV_OVERRIDE = os.getenv("AERGIA_ENV_PATH")

if ENV_OVERRIDE and os.path.exists(ENV_OVERRIDE):
    load_dotenv(ENV_OVERRIDE)
else:
    # Your previous hardcoded location (works for your current machine)
    hardcoded_env = r"c:\Users\z143d\OneDrive\Desktop\Project Aergia\.env"
    if os.path.exists(hardcoded_env):
        load_dotenv(hardcoded_env)
    else:
        # fallback: local .env (MagHub-friendly later)
        load_dotenv()

logging.basicConfig(level=logging.INFO)

# -----------------------------------------------------------------------------
# Backward compatible TaskType
# -----------------------------------------------------------------------------
class TaskType(Enum):
    CODING = "coding"
    CONTEXT = "context"
    SPEED = "speed"
    CREATIVE = "creative"
    REASONING = "reasoning"
    IMAGE_GEN = "image_gen"


# -----------------------------------------------------------------------------
# Orchestrator Router
# -----------------------------------------------------------------------------
class IntelligenceRouter:
    """
    Orchestrator-backed router.
    Backward compatible with your existing calls:

        router.generate(prompt, task_type=TaskType.CREATIVE, system_prompt="...")

    New capabilities:
      - task_type=TaskType.IMAGE_GEN -> routes to FAL image gen provider
      - policy-based fallback routing
    """

    def __init__(self):
        self.registry = ProviderRegistry()
        self.policy = PolicyEngine(self.registry)
        self.executor = ExecutionEngine(self.registry, self.policy)
        self.planner = Planner(self.executor)

        logging.info("🧠 Intelligence Router initialized (Orchestrator Mode)")
        logging.info(f"Registered providers: {self.registry.list_ids()}")

    def generate(self, prompt, task_type=TaskType.CODING, system_prompt="", **kwargs):
        """
        Legacy interface.
        Returns the primary 'content' string (text or URL depending on task).
        """
        # normalize task_type to string
        if isinstance(task_type, Enum):
            task_type_value = task_type.value
        else:
            task_type_value = str(task_type)

        req = TaskRequest(
            prompt=prompt,
            task_type=task_type_value,
            system_prompt=system_prompt or "",
            payload=kwargs or {},
        )

        result = self.executor.execute(req)

        # Optional logging for observability
        try:
            logging.info(
                f"[Router] task={task_type_value} provider={result.provider_id} "
                f"model={result.model} fallback={result.used_fallback} elapsed_ms={result.elapsed_ms} "
                f"reasons={result.routing.reasons}"
            )
        except Exception:
            pass

        return result.content

    def orchestrate(self, req: TaskRequest):
        """
        New interface: returns rich ExecutionResult (content + metadata).
        """
        return self.executor.execute(req)

    def plan_and_execute(self, goal: str):
        """
        High-level orchestrator entrypoint:
        Plan (reasoning) -> execute steps -> return structured results.
        """
        plan = self.planner.create_plan(goal)
        return self.planner.execute_plan(plan)


# Singleton instance (matches your current import pattern)
router = IntelligenceRouter()


# -----------------------------------------------------------------------------
# Optional: quick CLI test
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(router.generate("Say hello in one sentence.", task_type=TaskType.SPEED))

```

## File: router/core.py
```python
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

```

## File: router/registry.py
```python
import os
from dataclasses import dataclass
from typing import Dict, Optional, List

from router.providers.openrouter_provider import OpenRouterProvider
from router.providers.google_gemini_provider import GoogleGeminiProvider
from router.providers.fal_provider import FALProvider


@dataclass(frozen=True)
class ProviderIDs:
    # LLMs (sync)
    OPENROUTER_DEEPSEEK_V3: str = "openrouter_deepseek_v3"
    OPENROUTER_DEEPSEEK_R1: str = "openrouter_deepseek_r1"
    GOOGLE_GEMINI_FLASH: str = "google_gemini_flash"

    # Media (sync wrapper for now)
    FAL_FLUX_SCHNELL: str = "fal_flux_schnell"


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
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-001")
        fal_model = os.getenv("FAL_IMAGE_MODEL", "fal-ai/flux/schnell")

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

        # Google Gemini provider (REST)
        if google_key:
            self.providers[ProviderIDs.GOOGLE_GEMINI_FLASH] = GoogleGeminiProvider(
                api_key=google_key,
                model=gemini_model,
            )

        # FAL provider (uses env FAL_KEY internally)
        # If no FAL_KEY exists, calling it will fail at runtime (as expected).
        self.providers[ProviderIDs.FAL_FLUX_SCHNELL] = FALProvider(model=fal_model)

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

```

## File: router/policy.py
```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from router.schemas import ProviderCapability
from router.registry import ProviderRegistry, ProviderIDs


@dataclass
class RoutingDecision:
    primary: str
    fallbacks: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)


class PolicyEngine:
    """
    Rule-based policy (MVP).
    Later we can make this truly agentic by letting a model propose a plan
    BUT keep the final selection constrained by capabilities + allowlist.
    """

    def __init__(self, registry: ProviderRegistry):
        self.registry = registry

    def decide(
        self,
        task_type: str,
        payload: Optional[Dict[str, Any]] = None,
        prefer: Optional[str] = None,
    ) -> RoutingDecision:
        payload = payload or {}
        t = (task_type or "").lower().strip()

        # Explicit override (useful for debugging)
        if prefer:
            if self.registry.has(prefer):
                return RoutingDecision(primary=prefer, reasons=[f"prefer override={prefer}"])
            return RoutingDecision(primary=prefer, reasons=[f"prefer override requested but not registered: {prefer}"])

        # --- MEDIA TASKS ---
        if t in ("image_gen", "image", "image_generation"):
            return RoutingDecision(
                primary=ProviderIDs.FAL_FLUX_SCHNELL,
                fallbacks=[],
                reasons=["task=image_gen -> fal flux schnell"],
            )

        # --- REASONING TASKS ---
        if t in ("reasoning", "debate", "analysis"):
            if self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_R1):
                return RoutingDecision(
                    primary=ProviderIDs.OPENROUTER_DEEPSEEK_R1,
                    fallbacks=[
                        ProviderIDs.GOOGLE_GEMINI_FLASH,
                        ProviderIDs.OPENROUTER_DEEPSEEK_V3,
                    ],
                    reasons=["task=reasoning -> deepseek r1 primary"],
                )
            # If no OpenRouter, go Gemini
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                fallbacks=[],
                reasons=["task=reasoning but no openrouter -> gemini"],
            )

        # --- CONTEXT / SIMULATION TASKS (Prometheus lane) ---
        if t in ("context", "simulation", "thinking", "prometheus"):
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                fallbacks=[
                    ProviderIDs.OPENROUTER_DEEPSEEK_V3,
                ],
                reasons=["task=context/simulation -> gemini primary"],
            )

        # --- CODING TASKS (Hephaestus lane, but via LLMs) ---
        if t in ("coding", "code", "refactor", "debug"):
            if self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_V3):
                return RoutingDecision(
                    primary=ProviderIDs.OPENROUTER_DEEPSEEK_V3,
                    fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH],
                    reasons=["task=coding -> deepseek v3 primary"],
                )
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                fallbacks=[],
                reasons=["task=coding but no openrouter -> gemini"],
            )

        # --- CREATIVE (Hyperion director mode) ---
        if t in ("creative", "script", "story", "hyperion"):
            if self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_V3):
                return RoutingDecision(
                    primary=ProviderIDs.OPENROUTER_DEEPSEEK_V3,
                    fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH],
                    reasons=["task=creative -> deepseek v3 primary"],
                )
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                fallbacks=[],
                reasons=["task=creative but no openrouter -> gemini"],
            )

        # --- SPEED / DEFAULT CHAT ---
        if self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_V3):
            return RoutingDecision(
                primary=ProviderIDs.OPENROUTER_DEEPSEEK_V3,
                fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH],
                reasons=["default -> deepseek v3"],
            )

        return RoutingDecision(
            primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
            fallbacks=[],
            reasons=["default -> gemini (openrouter unavailable)"],
        )

```

## File: router/executor.py
```python
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional

from router.schemas import TaskRequest
from router.registry import ProviderRegistry
from router.policy import PolicyEngine, RoutingDecision
from router.utils import clean_markdown_fences


@dataclass
class ExecutionResult:
    content: str
    provider_id: str
    model: str
    raw: Any
    routing: RoutingDecision
    used_fallback: bool
    elapsed_ms: int


class ExecutionEngine:
    def __init__(self, registry: ProviderRegistry, policy: PolicyEngine):
        self.registry = registry
        self.policy = policy

    def execute(self, req: TaskRequest) -> ExecutionResult:
        decision = self.policy.decide(
            task_type=req.task_type,
            payload=req.payload,
            prefer=req.payload.get("prefer_provider") if req.payload else None,
        )

        # Try primary then fallbacks
        provider_order = [decision.primary] + list(decision.fallbacks)

        last_err: Optional[Exception] = None
        start = time.time()

        for idx, provider_id in enumerate(provider_order):
            used_fallback = idx > 0
            try:
                provider = self.registry.get(provider_id)
                resp: Dict[str, Any] = provider.generate(
                    prompt=req.prompt,
                    system_prompt=req.system_prompt,
                    **(req.payload or {})
                )

                content = resp.get("content", "")
                # Keep legacy behavior: strip markdown fences
                content = clean_markdown_fences(content)

                elapsed_ms = int((time.time() - start) * 1000)
                return ExecutionResult(
                    content=content,
                    provider_id=provider_id,
                    model=str(resp.get("model", "")),
                    raw=resp.get("raw"),
                    routing=decision,
                    used_fallback=used_fallback,
                    elapsed_ms=elapsed_ms,
                )

            except Exception as e:
                last_err = e
                continue

        elapsed_ms = int((time.time() - start) * 1000)
        raise RuntimeError(
            f"All providers failed for task_type={req.task_type}. "
            f"Tried={provider_order}. Elapsed={elapsed_ms}ms. LastError={last_err}"
        )

```

## File: router/schemas.py
```python
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

class ProviderCapability(Enum):
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    REASONING = "reasoning"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    MULTIMODAL = "multimodal"

class ExecutionMode(Enum):
    SYNC = "sync"
    ASYNC = "async"

@dataclass
class ProviderMetadata:
    name: str
    capabilities: List[ProviderCapability]
    execution_mode: ExecutionMode
    max_context: int
    cost_per_1k_tokens: float
    avg_latency_ms: int
    supports_streaming: bool

@dataclass
class TaskRequest:
    prompt: str
    task_type: str
    priority: str = "normal"
    latency_budget_ms: int = 10000
    cost_sensitivity: str = "medium"
    system_prompt: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PlanStep:
    step_id: int
    task_type: str
    prompt: str
    depends_on: List[int] = field(default_factory=list)
    output_key: str = "" # Where to store the result for future steps

@dataclass
class OrchestrationPlan:
    goal: str
    steps: List[PlanStep]
    metadata: Dict[str, Any] = field(default_factory=dict)

```

## File: router/base_provider.py
```python
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

```

## File: router/providers/openrouter_provider.py
```python
import requests
from typing import Dict, Any, Optional

from router.base_provider import BaseProvider
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode


class OpenRouterProvider(BaseProvider):
    """
    Pure REST wrapper around OpenRouter chat.completions.
    Good for DeepSeek V3/R1 through OpenRouter.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_s: int = 60,
        http_referer: str = "https://project-aergia.local",
        x_title: str = "Project Aergia OS",
    ):
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s
        self.http_referer = http_referer
        self.x_title = x_title

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_metadata(self) -> ProviderMetadata:
        # Heuristic capabilities based on model name
        caps = [ProviderCapability.TEXT_GENERATION, ProviderCapability.CODE_GENERATION]
        if "r1" in self.model.lower():
            caps.append(ProviderCapability.REASONING)

        return ProviderMetadata(
            name=f"openrouter:{self.model}",
            capabilities=caps,
            execution_mode=ExecutionMode.SYNC,
            max_context=64000,          # conservative placeholder; tune later
            cost_per_1k_tokens=0.0,     # fill if you want cost-aware routing
            avg_latency_ms=2000,        # tune later
            supports_streaming=True,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY missing for OpenRouterProvider")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.http_referer,
            "X-Title": self.x_title,
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        resp = requests.post(self.base_url, headers=headers, json=payload, timeout=self.timeout_s)
        if resp.status_code != 200:
            raise RuntimeError(f"OpenRouter error ({resp.status_code}): {resp.text}")

        data = resp.json()
        content = data["choices"][0]["message"]["content"]

        return {
            "content": content,
            "raw": data,
            "provider": "openrouter",
            "model": self.model,
        }

    def submit_job(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("OpenRouterProvider is sync-only (use generate).")

```

## File: router/providers/google_gemini_provider.py
```python
import requests
from typing import Dict, Any, Optional

from router.base_provider import BaseProvider
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode


class GoogleGeminiProvider(BaseProvider):
    """
    Pure REST wrapper around Google Generative Language API (AI Studio).
    Uses API key query param.
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash-001", timeout_s: int = 60):
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s

    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"google:{self.model}",
            capabilities=[
                ProviderCapability.TEXT_GENERATION,
                ProviderCapability.REASONING,   # Gemini is solid for thinking/simulation
            ],
            execution_mode=ExecutionMode.SYNC,
            max_context=1000000,     # placeholder; adjust per model
            cost_per_1k_tokens=0.0,  # optional
            avg_latency_ms=1800,     # optional
            supports_streaming=False,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY missing for GoogleGeminiProvider")

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

        full_prompt = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt.strip()

        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": full_prompt}]}],
        }

        # Optional generation config
        gen_cfg: Dict[str, Any] = {}
        if temperature is not None:
            gen_cfg["temperature"] = temperature
        if max_output_tokens is not None:
            gen_cfg["maxOutputTokens"] = max_output_tokens
        if gen_cfg:
            payload["generationConfig"] = gen_cfg

        resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=self.timeout_s)
        if resp.status_code != 200:
            raise RuntimeError(f"Gemini error ({resp.status_code}): {resp.text}")

        data = resp.json()
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            raise RuntimeError(f"Gemini response parse error: {data}")

        return {
            "content": text,
            "raw": data,
            "provider": "google",
            "model": self.model,
        }

    def submit_job(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("GoogleGeminiProvider is sync-only (use generate).")

```

## File: router/providers/fal_provider.py
```python
import os
from typing import Dict, Any, Optional

import requests
import fal_client

from router.base_provider import BaseProvider
from router.schemas import ProviderMetadata, ProviderCapability, ExecutionMode


class FALProvider(BaseProvider):
    """
    FAL provider wrapper (uses fal_client).
    For MVP: blocking "submit -> get()" flow, returns an image URL (or list).
    """

    def __init__(
        self,
        model: str = "fal-ai/flux/schnell",
        timeout_s: int = 180,
        fal_key: Optional[str] = None
    ):
        self.model = model
        self.timeout_s = timeout_s

        # fal_client reads FAL_KEY from env, but allow passing explicitly
        if fal_key:
            os.environ["FAL_KEY"] = fal_key

    def get_metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=f"fal:{self.model}",
            capabilities=[ProviderCapability.IMAGE_GENERATION],
            execution_mode=ExecutionMode.SYNC,  # blocking wrapper for MVP
            max_context=0,
            cost_per_1k_tokens=0.0,
            avg_latency_ms=8000,
            supports_streaming=False,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        image_size: str = "landscape_16_9",
        num_inference_steps: int = 4,
        seed: Optional[int] = 42,
        **kwargs
    ) -> Dict[str, Any]:
        # FAL doesn't use system_prompt; if provided, we just prepend
        full_prompt = f"{system_prompt}\n\n{prompt}".strip() if system_prompt else prompt.strip()

        handler = fal_client.submit(
            self.model,
            arguments={
                "prompt": full_prompt,
                "image_size": image_size,
                "num_inference_steps": num_inference_steps,
                "seed": seed,
            },
        )

        result = handler.get()  # blocks

        # Normalize to a single URL when possible
        image_url = None
        if isinstance(result, dict) and "images" in result and result["images"]:
            image_url = result["images"][0].get("url")

        if not image_url:
            raise RuntimeError(f"FAL returned no image URL: {result}")

        return {
            "content": image_url,
            "raw": result,
            "provider": "fal",
            "model": self.model,
        }

    def submit_job(self, prompt: str, **kwargs) -> str:
        # If you want true async later, we can store request_id and poll.
        handler = fal_client.submit(self.model, arguments={"prompt": prompt, **kwargs})
        # handler.request_id exists in many versions; fallback to string repr
        return getattr(handler, "request_id", None) or str(handler)

```

## File: Project Chimera\source\worker.py
```python
import os
import sys
import logging
import sqlite3
import time
from datetime import datetime
from dotenv import load_dotenv
# from google.cloud import texttospeech
# import vertexai
# from vertexai.preview.generative_models import GenerativeModel
import fal_client
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
import requests

# Add Aergia Studio Root to Path
current_dir = os.path.dirname(os.path.abspath(__file__))
aergia_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if aergia_root not in sys.path:
    sys.path.append(aergia_root)

from intelligence_router import router, TaskType

# --- App Initialization ---
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
    handlers=[
        logging.FileHandler("chimera_worker.log"),
        logging.StreamHandler()
    ]
)

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chimera.db")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Clients
tts_client = None

def initialize_worker():
    """Initializes AI clients."""
    global tts_client
    if tts_client:
        return

    logging.info("Initializing Worker service...")
    try:
        # if not PROJECT_ID:
        #    logging.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI features (Image Generation) will be unavailable.")
        # else:
        #    # Init clients
        #    pass
        
        logging.info("Worker config: Using EdgeTTS (Audio) and Pollinations.ai (Video). No Google Cloud Billing required.")
            
        # Initialize SQLite DB if needed
        init_db()

        logging.info("Worker clients and database initialized successfully.")

    except Exception as e:
        logging.error(f"Worker Initialization Warning: {e}")
        # raise # Don't crash, allow limited functionality

def init_db():
    """Creates the SQLite table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storyboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT DEFAULT 'pending',
            video_path TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            storyboard_id INTEGER,
            scene_number INTEGER,
            script TEXT,
            prompt TEXT,
            FOREIGN KEY(storyboard_id) REFERENCES storyboards(id)
        )
    ''')
    conn.commit()
    conn.close()

    conn.commit()
    conn.close()

def Image_Generation_via_router(prompt, image_size="landscape_16_9"):
    """
    Replaces direct fal_client calls. 
    Uses the Aergia Orchestrator to handle generation and fallbacks.
    """
    logging.info(f"🎨 Orchestrating image generation for: {prompt[:50]}...")
    
    try:
        # The router now handles the FAL logic, API keys, and error catching
        image_url = router.generate(
            prompt=prompt,
            task_type=TaskType.IMAGE_GEN,
            image_size=image_size # Passed into the FAL provider via kwargs
        )
        return image_url
    except Exception as e:
        logging.error(f"❌ Router Image Gen Failed: {e}")
        # Fallback to a placeholder or a secondary method if desired
        return None

def process_task(storyboard_id):
    """Processes a video generation task for a given storyboard ID."""
    logging.info(f"Job {storyboard_id}: Processing started.")
    
    final_video_filename = f"storyboard_{storyboard_id}.mp4"
    final_video_path = os.path.join(OUTPUT_DIR, final_video_filename)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    temp_files = []

    try:
        # Update status
        cursor.execute("UPDATE storyboards SET status = 'processing' WHERE id = ?", (storyboard_id,))
        conn.commit()

        # Fetch ALL scenes
        cursor.execute("SELECT scene_number, script, prompt FROM scenes WHERE storyboard_id = ? ORDER BY scene_number", (storyboard_id,))
        scenes = cursor.fetchall()
        
        if not scenes:
            raise Exception(f"No scenes found for storyboard_id {storyboard_id}")
        
        logging.info(f"Job {storyboard_id}: Found {len(scenes)} scenes.")
        
        video_clips = []

        for scene in scenes:
            scene_num, script_text, video_prompt = scene
            logging.info(f"Job {storyboard_id}: Processing Scene {scene_num}...")

            scene_audio_path = f"temp_{storyboard_id}_scene_{scene_num}.mp3"
            scene_image_path = f"temp_{storyboard_id}_scene_{scene_num}.png"
            temp_files.extend([scene_audio_path, scene_image_path])

            # 2. Text Substitution (Time/Date)
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%B %d, %Y")
            script_text = script_text.replace("{{TIME}}", current_time).replace("{{DATE}}", current_date)
            logging.info(f"  - Final Script: {script_text}")

            # 3. Generate Audio (Edge TTS - Free)
            logging.info(f"  - Generating audio (Edge TTS)...")
            
            # Escape text for CLI (basic)
            safe_text = script_text.replace('"', '\\"').replace('\n', ' ')
            voice_name = "en-US-ChristopherNeural" # High quality male voice
            
            # Run edge-tts via CLI to avoid async compatibility headeraches in this sync worker
            # Command: edge-tts --text "Hello" --write-media output.mp3 --voice en-US-ChristopherNeural
            cmd = f'edge-tts --text "{safe_text}" --write-media "{scene_audio_path}" --voice {voice_name}'
            
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Edge TTS failed: {result.stderr}")
            
            if not os.path.exists(scene_audio_path):
                 raise Exception("Edge TTS did not produce an audio file.")

            
            # 4. Generate Video (Fal.ai - Wan 2.5)
            if video_prompt.startswith("RESOURCE:"):
                # ... resource handling remains same ...
                resource_filename = video_prompt.split("RESOURCE:")[1].strip()
                resource_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", resource_filename)
                logging.info(f"  - Using local resource: {resource_path}")
                if not os.path.exists(resource_path):
                     raise FileNotFoundError(f"Resource file not found: {resource_path}")
                final_image_source = resource_path
                is_video = resource_path.lower().endswith(".mp4")
            else:
                logging.info(f"  - Generating VIDEO with prompt: '{video_prompt}'")
                
                # Check for Key
                if not os.getenv("FAL_KEY"):
                    raise Exception("FAL_KEY not found in .env! Cannot generate video.")

                # Router Image Generation (Flux via Intelligence Router) using Helper
                image_url = Image_Generation_via_router(video_prompt)
                
                if not image_url:
                     raise Exception("Failed to generate image via Router.")

                logging.info(f"    - Image Generated: {image_url}")
                
                # Download Image (reuse scene_image_path which is .png)
                # Note: scene_image_path was already added to temp_files for cleanup
                response = requests.get(image_url)
                with open(scene_image_path, "wb") as f:
                    f.write(response.content)
                    
                final_image_source = scene_image_path
                is_video = False # Static Image

            # 5. Create Clip
            logging.info(f"  - Creating clip...")
            audioclip = AudioFileClip(scene_audio_path)
            
            if is_video:
                # Load Video 
                video_clip_raw = VideoFileClip(final_image_source)
                
                # Loop or trim video to match audio length
                if video_clip_raw.duration < audioclip.duration:
                    # Loop if too short
                    n_loops = int(audioclip.duration / video_clip_raw.duration) + 1
                    video_clip = video_clip_raw.loop(n=n_loops)
                else:
                    video_clip = video_clip_raw
                    
                # Set duration explicitly to audio length
                video_clip = video_clip.with_duration(audioclip.duration)
                
                # If generated video has no audio, add TTS. 
                # If it has audio, we usually replace it with our narrative TTS.
                video_clip = video_clip.with_audio(audioclip)
                
            else:
                # Fallback for Static Images (Resources)
                from moviepy import ImageClip
                image_clip = ImageClip(final_image_source, duration=audioclip.duration)
                video_clip = image_clip.with_audio(audioclip)
                
            video_clips.append(video_clip)

        # 4. Concatenate All Clips
        logging.info(f"Job {storyboard_id}: Concatenating {len(video_clips)} clips...")
        final_clip = concatenate_videoclips(video_clips, method="compose")
        
        final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=24, logger=None)

        # Update status to complete
        cursor.execute("UPDATE storyboards SET status = 'complete', video_url = ? WHERE id = ?", (final_video_path, storyboard_id))
        conn.commit()

        logging.info(f"SUCCESS: Job {storyboard_id} finished. Video saved to: {final_video_path}")

    except Exception as e:
        logging.error(f"FAILURE: Error processing job {storyboard_id}: {e}", exc_info=True)
        cursor.execute("UPDATE storyboards SET status = 'failed', error_message = ? WHERE id = ?", (str(e), storyboard_id))
        conn.commit()

    finally:
        conn.close()
        # Cleanup temp files
        time.sleep(2) # Give OS time to release file handles (Fix WinError 32)
        for f in temp_files:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError as e:
                    logging.warning(f"Job {storyboard_id}: Could not remove temp file {f}: {e}")

def main():
    initialize_worker()
    
    # Simple polling loop for demonstration
    logging.info("Worker started. Polling for pending jobs...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM storyboards WHERE status = 'pending' LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                process_task(row[0])
            else:
                time.sleep(5) # Wait before checking again
        except KeyboardInterrupt:
            logging.info("Worker stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in polling loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
```

## File: Project Hyperion\hyperion_director.py
```python

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

# --- Configuration ---
# Load API Key from Project Midas (Shared Key)
MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env.local")
load_dotenv(MIDAS_ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Check .env (Fallback)
if not API_KEY:
    MIDAS_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Project Midas", ".env")
    load_dotenv(MIDAS_ENV_PATH)
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    # 3. Last Resort: local .env
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

class HyperionDirector:
    def __init__(self):
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in Project Midas/.env.local or environment.")
        
        self.client = genai.Client(api_key=API_KEY)
        self.model_name = "gemini-2.0-flash-exp"
        print(f"🎬 Hyperion Director initialized with {self.model_name} (New SDK)")

    def direct_movie(self, user_concept):
        """
        Takes a user concept and returns a list of scenes (dict with script/prompt).
        """
        system_prompt = self._load_system_prompt()
        full_prompt = f"{system_prompt}\n\nUSER REQUEST: {user_concept}\n\nOUTPUT:"
        
        try:
            # We need to add the parent directory to sys.path to import intelligence_router
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from intelligence_router import router, TaskType
            
            print("🎬 Director: Delegating generation to Intelligence Router...")
            
            # The router handles retries, fallbacks (OpenRouter -> Google), and model selection
            response_text = router.generate(
                prompt=full_prompt,
                task_type=TaskType.CREATIVE,
                system_prompt=system_prompt
            )
            
            if "Error" in response_text and len(response_text) < 100:
                print(f"❌ Director Failed: {response_text}")
                return []
                
            return self._parse_response(response_text)

        except Exception as e:
            print(f"Router Error: {e}")
            import traceback
            traceback.print_exc()
            return []


    def _load_system_prompt(self):
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "hyperion_public_prompt.txt")
            with open(prompt_path, "r") as f:
                return f.read()
        except:
            return "You are an AI Movie Director. Create a 3 scene script."

    def _parse_response(self, text):
        """
        Parses the text output into a structured list.
        Expected format lines: 'Scene X: [Visual] | [Audio]'
        """
        scenes = []
        lines = text.split('\n')
        scene_count = 1
        
        import re
        for line in lines:
            print(f"DEBUG: Raw Response Length: {len(text)}")
            if len(text) < 500:
                print(f"DEBUG: Raw Response: {text}")

            # Match "Scene X", "**Scene X**", "Simple Header: Scene X", etc.
            # Removed ^ start anchor to handle markdown bullets or reasoning text
            match = re.search(r"\**Scene\s+(\d+)", line.strip(), re.IGNORECASE)
            
            if match:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    content = parts[1].strip()
                    # Remove trailing ** if present (from **Scene 1**: format)
                    content = content.replace("**", "") 
                    
                    # Split Visual | Audio
                    if '|' in content:
                        visual, audio = content.split('|', 1)
                        # We use Visual as Prompt, and Audio (or combined) as Script
                        # Actually worker.py expects: Script | Prompt
                        # Let's make the Script be the Audio/Voiceover description and Prompt be the Visual
                        script = audio.strip()
                        prompt = visual.strip()
                    else:
                        script = content
                        prompt = content
                    
                    scenes.append({
                        "scene_number": int(match.group(1)),
                        "script": script,
                        "prompt": prompt
                    })
        return scenes

if __name__ == "__main__":
    # Test
    print("🎬 Hyperion Director: Initializing...")
    try:
        director = HyperionDirector()
        print("🎬 Action! Directing 'A cyberpunk detective in the rain'...")
        scenes = director.direct_movie("A cyberpunk detective in the rain")
        
        for scene in scenes:
            print(f"Scene {scene['scene_number']}:")
            print(f"  Prompt: {scene['prompt']}")
            print(f"  Script: {scene['script']}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error: {e}")

```

## File: Project Midas\midas_home.py
```python
import customtkinter as ctk
from PIL import Image, ImageSequence
import threading
import os
import sys
import webbrowser
import subprocess
import glob

# Import Midas Modules
from midas_voice import speak
from midas_strategist import MidasStrategist
from squeeze_scanner import get_squeeze_candidates
from midas_notifier import send_alert # Alerts
from midas_notifier import send_alert # Alerts
import midas_agent # For visual scan
from midas_swing import MidasSwingTrader # Swing Logic
from agents.coach import TradingCoach # Trading Coach Logic
from agents.strategy_coordinator import StrategyCoordinator # Auto-Pilot Logic
from virtual_broker import VirtualBroker # Broker logic
from schwab_api.client import SchwabClient # Live Account

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True) # No title bar
        
        # Fixed size for splash
        w, h = 600, 400
        self.geometry(f"{w}x{h}")
        
        # Center on screen
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        try:
            self.gif_path = "assets/startup.gif"
            if not os.path.exists(self.gif_path):
                 raise FileNotFoundError("No gif found")
                 
            self.gif_image = Image.open(self.gif_path)
            self.frames = [frame.copy() for frame in ImageSequence.Iterator(self.gif_image)]
            self.frame_index = 0
            
            self.label = ctk.CTkLabel(self, text="")
            self.label.pack(expand=True, fill="both")
            
            self.animate()
            
            # Close after 3 seconds
            self.after(3000, self.finish)
        except Exception as e:
            print(f"Splash Error: {e}")
            self.finish()

    def animate(self):
        try:
            if not self.winfo_exists(): return
            
            frame = self.frames[self.frame_index]
            # Resize frame to fit window if needed, or keep original aspect
            # For simplicity, force fit
            ctk_img = ctk.CTkImage(light_image=frame, dark_image=frame, size=(600, 400))
            self.label.configure(image=ctk_img)
            
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(66, self.animate) # ~15fps
        except Exception:
            pass
            
    def finish(self):
        self.destroy()
        self.master.deiconify()

class MidasHome(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Midas - AI Trading Workspace")
        self.geometry("1100x700")

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) # Portfolio Panel (Fixed/Auto)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Avatar & Controls) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Push bottom spacer

        # Avatar
        self.avatar_label = ctk.CTkLabel(self.sidebar_frame, text="")
        self.avatar_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.load_avatar()

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MIDAS AI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        # Buttons
        self.btn_briefing = ctk.CTkButton(self.sidebar_frame, text="🌞 Morning Briefing", command=self.start_briefing_thread)
        self.btn_briefing.grid(row=2, column=0, padx=20, pady=10)

        self.btn_scanner = ctk.CTkButton(self.sidebar_frame, text="🚀 Squeeze Scanner", command=self.run_scanner_thread)
        self.btn_scanner.grid(row=3, column=0, padx=20, pady=10)

        self.btn_visual = ctk.CTkButton(self.sidebar_frame, text="👁️ Visual Scan (Screen)", command=self.run_visual_thread, fg_color="#552222", hover_color="#773333")
        self.btn_visual.grid(row=4, column=0, padx=20, pady=10)

        self.btn_swing = ctk.CTkButton(self.sidebar_frame, text="📈 Quant Swing Trader", command=self.run_swing_thread, fg_color="#225522", hover_color="#337733")
        self.btn_swing.grid(row=5, column=0, padx=20, pady=10)

        # New Tools
        self.btn_chart = ctk.CTkButton(self.sidebar_frame, text="📊 Open Latest Chart", command=self.open_latest_chart, fg_color="#333333", hover_color="#555555")
        self.btn_chart.grid(row=6, column=0, padx=20, pady=10)

        self.btn_launch = ctk.CTkButton(self.sidebar_frame, text="🚀 Launch Workspace", command=self.launch_workspace_thread, fg_color="#440044", hover_color="#660066")
        self.btn_launch.grid(row=7, column=0, padx=20, pady=(10, 20))

        self.btn_coach = ctk.CTkButton(self.sidebar_frame, text="🧠 Run Trading Coach", command=self.run_coach_thread, fg_color="#004444", hover_color="#006666")
        self.btn_coach.grid(row=8, column=0, padx=20, pady=10)

        self.btn_autopilot = ctk.CTkButton(self.sidebar_frame, text="♾️ Activate Auto-Pilot", command=self.toggle_autopilot, fg_color="#550000", hover_color="#770000")
        self.btn_autopilot.grid(row=9, column=0, padx=20, pady=10)

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Output Log (Briefing/Scan Results)
        self.textbox = ctk.CTkTextbox(self.main_frame, width=500, height=400, font=("Consolas", 14))
        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.textbox.insert("0.0", "Welcome back, Daniel.\nSystem Ready.\n")

        # --- Portfolio Panel (Right Side) ---
        self.portfolio_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.portfolio_frame.grid(row=0, column=2, sticky="nsew")
        
        self.pf_label = ctk.CTkLabel(self.portfolio_frame, text="PORTFOLIO MONITOR", font=ctk.CTkFont(size=16, weight="bold"))
        self.pf_label.pack(pady=20)

        self.pf_tabview = ctk.CTkTabview(self.portfolio_frame, width=220)
        self.pf_tabview.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.tab_paper = self.pf_tabview.add("Paper")
        self.tab_live = self.pf_tabview.add("Live")
        
        # Paper Widgets
        self.lbl_paper_eq = ctk.CTkLabel(self.tab_paper, text="Net Liq: $---", font=("Consolas", 16))
        self.lbl_paper_eq.pack(pady=10)
        self.lbl_paper_cash = ctk.CTkLabel(self.tab_paper, text="Cash: $---", font=("Consolas", 12))
        self.lbl_paper_cash.pack(pady=5)
        self.lbl_paper_pos = ctk.CTkLabel(self.tab_paper, text="Positions:\nNone", justify="left")
        self.lbl_paper_pos.pack(pady=20, anchor="w")
        self.btn_refresh_paper = ctk.CTkButton(self.tab_paper, text="Refresh Paper", command=self.update_paper_portfolio, height=30)
        self.btn_refresh_paper.pack(pady=10)

        # Live Widgets
        self.lbl_live_eq = ctk.CTkLabel(self.tab_live, text="Net Liq: $---", font=("Consolas", 16))
        self.lbl_live_eq.pack(pady=10)
        self.lbl_live_cash = ctk.CTkLabel(self.tab_live, text="Cash: $---", font=("Consolas", 12))
        self.lbl_live_cash.pack(pady=5)
        self.lbl_live_pos = ctk.CTkLabel(self.tab_live, text="Positions:\n(Hidden)", justify="left")
        self.lbl_live_pos.pack(pady=20, anchor="w")
        self.btn_refresh_live = ctk.CTkButton(self.tab_live, text="Fetch Live Data", command=self.update_live_portfolio, fg_color="#aa0000", hover_color="#cc0000")
        self.btn_refresh_live.pack(pady=10)

        # --- Income / Medicaid Monitor (Bottom of Portfolio Panel) ---
        self.monitor_frame = ctk.CTkFrame(self.portfolio_frame, fg_color="#333333")
        self.monitor_frame.pack(side="bottom", fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(self.monitor_frame, text="MEDICAID SAFETY MONITOR", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Default Values
        self.wages = 10400.00 # $200 * 52
        self.medicaid_limit = 20000.00 # Safe Est.
        
        self.lbl_income_proj = ctk.CTkLabel(self.monitor_frame, text=f"Proj. Income: ${self.wages:,.2f}", font=("Consolas", 12))
        self.lbl_income_proj.pack(pady=2)
        
        self.lbl_income_status = ctk.CTkLabel(self.monitor_frame, text="STATUS: SAFE (Tier 1)", text_color="green", font=("Arial", 10, "bold"))
        self.lbl_income_status.pack(pady=(0, 10))
        
        self.progress_income = ctk.CTkProgressBar(self.monitor_frame, height=10)
        self.progress_income.set(self.wages / self.medicaid_limit)
        self.progress_income.pack(padx=10, pady=(0, 10))

        # Chat Input
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Ask Midas Strategy Brain...")
        self.entry.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry.bind("<Return>", self.chat_with_midas)

        self.strategist = MidasStrategist()
        # Initialize Agent SDK just in case
        midas_agent.init_midas()

        # Auto-Refresh Paper on load
        self.update_paper_portfolio()
        
    def load_avatar(self):
        try:
            # Load 'assets/avatar.jpg' or fallback
            path = "assets/avatar.jpg"
            if not os.path.exists(path):
                # Placeholder logic if no file
                return 
            
            my_image = ctk.CTkImage(light_image=Image.open(path),
                                  dark_image=Image.open(path),
                                  size=(150, 150))
            self.avatar_label.configure(image=my_image)
        except Exception as e:
            print(f"Avatar load error: {e}")

    # --- Actions ---
    
    def update_paper_portfolio(self):
        def _update():
            try:
                broker = VirtualBroker()
                summary = broker.get_account_summary()
                
                # Update Labels safely
                self.lbl_paper_eq.configure(text=f"Net Liq: ${summary['liquidation_value']:.2f}")
                self.lbl_paper_cash.configure(text=f"Cash: ${summary['cash']:.2f}")
                
                pos_text = "Positions:\n"
                if not summary['positions']:
                    pos_text += "None"
                else:
                    for sym, data in summary['positions'].items():
                        pos_text += f"{sym}: {data['qty']} @ ${data['avg_price']:.2f}\n"
                
                self.lbl_paper_pos.configure(text=pos_text)
            except Exception as e:
                print(f"Paper Update Error: {e}")
                
        threading.Thread(target=_update, daemon=True).start()

    def update_live_portfolio(self):
        def _update():
            try:
                self.btn_refresh_live.configure(text="Fetching...", state="disabled")
                client = SchwabClient()
                
                # 1. Get Accounts
                accounts = client.get_account_numbers() 
                if not accounts: 
                    self.lbl_live_eq.configure(text="No Accounts Found")
                    return
                
                # Prepare display text
                display_text_eq = ""
                display_text_cash = ""
                display_text_pos = ""
                
                total_liq_val = 0.0
                
                for idx, acct in enumerate(accounts):
                    acct_hash = acct.get('hashValue')
                    acct_num = acct.get('accountNumber', 'xxxx')[-4:] # Last 4 digits
                    
                    # 2. Get Balance for each
                    balance_data = client.get_account_balance(acct_hash)
                    
                    sec_acct = balance_data.get('securitiesAccount', {})
                    curr_bal = sec_acct.get('currentBalances', {})
                    liq_val = curr_bal.get('liquidationValue', 0.0)
                    cash_bal = curr_bal.get('cashBalance', 0.0)
                    
                    total_liq_val += liq_val
                    
                    positions = sec_acct.get('positions', [])
                    
                    # Format Output
                    # Add separator if not first account
                    if idx > 0:
                        display_text_eq += "\n"
                        display_text_cash += "\n"
                        display_text_pos += "\n" + "-"*30 + "\n"

                    display_text_eq += f"#{idx+1} (..{acct_num}): ${liq_val:,.2f}"
                    display_text_cash += f"#{idx+1}: ${cash_bal:,.2f}"
                    
                    display_text_pos += f"--- Account #{idx+1} (..{acct_num}) ---\n"
                    if not positions:
                        display_text_pos += "None\n"
                    else:
                        for p in positions: 
                            sym = p.get('instrument', {}).get('symbol', 'UNK')
                            qty = p.get('longQuantity', 0)
                            display_text_pos += f"{sym}: {qty}\n"

                self.lbl_live_eq.configure(text=display_text_eq.strip())
                self.lbl_live_cash.configure(text=display_text_cash.strip())
                self.lbl_live_pos.configure(text=display_text_pos)
                
                # --- Update Income Monitor ---
                # Use TOTAL Likidation Value for safety calculation
                
                est_gains = 0.0
                # Conservative estimate: Gains = Total Net Liq - (25k * num_accounts)? 
                # Or just assume Total Net Liq - 25000 base. 
                # Let's stick to the previous simple logic but on the Total.
                if total_liq_val > 25000:
                    est_gains = total_liq_val - 25000
                
                total_income = self.wages + est_gains
                fill_ratio = total_income / self.medicaid_limit
                if fill_ratio > 1.0: fill_ratio = 1.0
                
                self.lbl_income_proj.configure(text=f"Proj. Income: ${total_income:,.2f}")
                self.progress_income.set(fill_ratio)
                
                if total_income > self.medicaid_limit:
                    self.lbl_income_status.configure(text="STATUS: DANGER (Limit Exceeded)", text_color="red")
                    self.progress_income.configure(progress_color="red")
                elif total_income > (self.medicaid_limit * 0.9):
                    self.lbl_income_status.configure(text="STATUS: WARNING (Approaching)", text_color="orange")
                    self.progress_income.configure(progress_color="orange")
                else:
                    self.lbl_income_status.configure(text="STATUS: SAFE (Tier 1)", text_color="green")
                    self.progress_income.configure(progress_color="green")
                
            except Exception as e:
                self.lbl_live_eq.configure(text="Error Fetching")
                print(f"Live Update Error: {e}")
            finally:
                self.btn_refresh_live.configure(text="Fetch Live Data", state="normal")
                
        threading.Thread(target=_update, daemon=True).start()

    def log(self, text):
        self.after(0, lambda: self.textbox.insert("end", text + "\n"))
        self.after(0, lambda: self.textbox.see("end"))

    def start_briefing_thread(self):
        self.log("\n--- STARTING MORNING BRIEFING ---")
        threading.Thread(target=self.run_briefing_process, daemon=True).start()

    def run_briefing_process(self):
        # 1. Run Logic & Get Text
        full_text = run_briefing(output_callback=lambda x: None) # Suppress print, we use full text
        self.log(full_text)
        
        # 2. Voice (Multi-Talk)
        intro = "Good morning. Here is your daily briefing."
        clean_text = full_text.replace("*", "").replace("#", "")
        speak(intro)
        speak(clean_text)
        
        # 3. Mobile Alert (Voice & Text)
        self.log("\n📱 Sending Mobile Voice Alert...")
        
        # Generate Audio File for MMS
        audio_file = "briefing_audio.mp3"
        from midas_voice import save_to_file
        save_to_file(clean_text[:1000], audio_file) # Limit length for MMS size limits
        
        success = send_alert("Midas Morning Brief", full_text, attachment_path=audio_file)
        
        if success:
            self.log(">> Voice Briefing sent to Phone & Email.")
        else:
            self.log(">> Alert Failed. **Check EMAIL_SENDER in .env**")
            
        # Cleanup
        if os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except:
                pass

    def run_scanner_thread(self):
        self.log("\n--- RUNNING SQUEEZE SCANNER ---")
        threading.Thread(target=self.run_scanner_process, daemon=True).start()

    def run_scanner_process(self):
        candidates = get_squeeze_candidates()
        if not candidates:
            self.log("No hits found.")
            speak("I did not find any squeeze candidates for you today.")
        else:
            for c in candidates:
                self.log(f"🚨 {c['symbol']} | SI: {c['short_float']}%")
            speak(f"I found {len(candidates)} potential plays. Check the dashboard.")

    def run_visual_thread(self):
        self.log("\n--- VISUAL SCAN INITIATED ---")
        self.log("Hide this window if it blocks your chart. Capturing in 3 seconds...")
        threading.Thread(target=self.run_visual_process, daemon=True).start()

    def run_visual_process(self):
        import time
        time.sleep(3) # Time to switch windows
        speak("Capturing screen.")
        try:
            path = midas_agent.capture_screen(mask_privacy=True)
            self.log(f"Snapshot taken: {path}")
            
            response = midas_agent.analyze_market(path, "Analyze this chart/chain and suggest a trade.")
            self.log(f"\nMIDAS VISION:\n{response}")
            speak("Analysis complete. Check the log.")
            
            # Privacy cleanup
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            self.log(f"Visual Error: {e}")

    def run_swing_thread(self):
        self.log("\n--- STARTING QUANT SWING TRADER ---")
        threading.Thread(target=self.run_swing_process, daemon=True).start()

    def run_swing_process(self):
        try:
            speak("Initializing Swing Trader Protocol.")
            trader = MidasSwingTrader()
            broker = VirtualBroker()
            
            watchlist = ['SPY', 'QQQ', 'IWM', 'DIA', 'AAPL', 'NVDA', 'AMD', 'TSLA']
            self.log(f"Scanning Watchlist: {watchlist}")
            self.log(f"Paper Balance: ${broker.account['cash']:.2f}")

            hits = 0
            for symbol in watchlist:
                try:
                    analysis = trader.analyze_ticker(symbol)
                    if not analysis or analysis.get('signal') == 'ERROR':
                        continue
                        
                    signal = analysis['signal']
                    # Log result
                    self.log(f"{symbol}: {signal} | Last: {analysis['price']:.2f}")
                    
                    if "BUY" in signal:
                        hits += 1
                        self.log(f"   >>> ACTION REQUIRED: {signal}")
                        self.log(f"   >>> Reason: {analysis['reason']}")
                        if 'chart' in analysis:
                            chart_abs = os.path.abspath(analysis['chart'])
                            self.log(f"   >>> Chart Generated: {chart_abs}")
                            # Could auto-open: os.startfile(chart_abs) if desired

                except Exception as e:
                    self.log(f"Error {symbol}: {e}")
            
            if hits > 0:
                speak(f"Scan complete. I found {hits} trade opportunities.")
            else:
                speak("Scan complete. No significant signals found right now.")
                
        except Exception as e:
            self.log(f"Swing Trader Error: {e}")
            speak("Error running swing trader.")

    def run_coach_thread(self):
        self.log("\n--- STARTING TRADING COACH ---")
        threading.Thread(target=self.run_coach_process, daemon=True).start()

    def run_coach_process(self):
        try:
            speak("Reviewing your performance.")
            coach = TradingCoach()
            # Redirect stdout to capture coach output (simple hack) or just trust logs
            # For now, just run it, coach.py prints to stdout which goes to console, not GUI textbox unless redirected.
            # I will modify coach to return string or just read the 'lessons_learned.md' tail?
            # Let's just run it and read the last lesson.
            
            coach.run_analysis()
            
            # Read last lesson from file
            if os.path.exists(coach.lessons_path):
                with open(coach.lessons_path, 'r') as f:
                    lines = f.readlines()
                    # simplistic tail
                    last_lesson = "".join(lines[-10:]) 
                self.log(f"\n[COACH FEEDBACK]\n{last_lesson}")
                speak("I have updated your lessons learned file.")
            else:
                self.log("Coach finished (No history found).")
                speak("No new trade history to review.")
                
        except Exception as e:
            self.log(f"Coach Error: {e}")
            speak("The Coach encountered an error.")

    def toggle_autopilot(self):
        if hasattr(self, 'autopilot_running') and self.autopilot_running:
            self.autopilot_running = False
            self.btn_autopilot.configure(text="♾️ Activate Auto-Pilot", fg_color="#550000")
            self.log("Auto-Pilot Stopping...")
            speak("Auto Pilot Deactivated.")
        else:
            self.autopilot_running = True
            self.btn_autopilot.configure(text="🛑 Stop Auto-Pilot", fg_color="#005500")
            self.log("Auto-Pilot Activated. Running cycles every 60s.")
            speak("Auto Pilot Engaged. Monitoring markets.")
            threading.Thread(target=self.run_autopilot_loop, daemon=True).start()

    def run_autopilot_loop(self):
        coord = StrategyCoordinator()
        
        while getattr(self, 'autopilot_running', False):
             try:
                 self.log("\n[AUTO-PILOT] Starting Market Cycle...")
                 # We invoke the cycle. Currently it prints to stdout.
                 # Ideally we capture it, but for MVP we log start/finish.
                 coord.run_daily_cycle()
                 self.log("[AUTO-PILOT] Cycle Complete. Sleeping 60s.")
             except Exception as e:
                 self.log(f"[AUTO-PILOT] Error: {e}")
            
             # Sleep in chunks to allow faster stop
             for _ in range(60): 
                 if not getattr(self, 'autopilot_running', False): break
                 threading.Event().wait(1)

    def chat_with_midas(self, event=None):
        prompt = self.entry.get()
        if not prompt: return
        
        self.log(f"\nYOU: {prompt}")
        self.entry.delete(0, "end")
        
        def run_chat():
            response = self.strategist.ask(prompt)
            self.log(f"MIDAS: {response}")
            
        threading.Thread(target=run_chat, daemon=True).start()

    def launch_workspace_thread(self):
        threading.Thread(target=self.launch_workspace, daemon=True).start()

    def launch_workspace(self):
        self.log("\n--- LAUNCHING WORKSPACE ---")
        tos_path = r"C:\Users\z143d\AppData\Local\thinkorswim\thinkorswim.exe"
        coinbase_url = "https://www.coinbase.com/home"
        
        # 1. Launch TOS
        if os.path.exists(tos_path):
            self.log("Launching ThinkOrSwim...")
            try:
                subprocess.Popen(tos_path)
                speak("Launching Think-Or-Swim.")
            except Exception as e:
                self.log(f"Error launching TOS: {e}")
        else:
            self.log(f"TOS not found at: {tos_path}")
            
        # 2. Launch Coinbase
        self.log("Opening Coinbase...")
        webbrowser.open(coinbase_url)
        speak("Opening Coinbase.")

    def open_latest_chart(self):
        self.log("\nSearching for latest chart...")
        try:
            # Find all html files in charts folder
            chart_dir = os.path.join(os.path.dirname(__file__), "charts")
            list_of_files = glob.glob(os.path.join(chart_dir, "*.html"))
            
            if not list_of_files:
                self.log("No charts found.")
                speak("I don't see any generated charts yet.")
                return

            latest_file = max(list_of_files, key=os.path.getctime)
            self.log(f"Opening: {os.path.basename(latest_file)}")
            webbrowser.open(f"file://{os.path.abspath(latest_file)}")
            speak("Opening chart.")
        except Exception as e:
            self.log(f"Error opening chart: {e}")

if __name__ == "__main__":
    # 1. Init App but hide it
    app = MidasHome()
    app.withdraw() # Hide until splash is done
    
    # 2. Show Splash
    splash = SplashScreen(app)
    
    # 3. Process events until splash destroys itself
    # app.mainloop.mainloop() handles the splash because it is a Toplevel of app
    app.mainloop()

```

