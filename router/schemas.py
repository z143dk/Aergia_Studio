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
    FINANCIAL_ANALYSIS = "financial_analysis"
    TRADING = "trading"

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
