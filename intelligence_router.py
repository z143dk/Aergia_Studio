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
# Dynamic loading:
# 1. Check AERGIA_ENV_PATH (if set)
# 2. Check current directory
# 3. Check hardcoded path (legacy fallback only)
current_dir = os.path.dirname(os.path.abspath(__file__))
potential_paths = [
    os.path.join(current_dir, ".env"),
    os.path.join(os.path.dirname(current_dir), ".env"), # Parent dir
    os.path.join(current_dir, "Project Midas", ".env.local"), # Midas Local
    os.path.join(current_dir, "Project Midas", ".env"), # Midas Shared
    os.path.join(current_dir, "Project Chimera", ".env"), # Chimera Shared
    os.path.join(current_dir, "Project Chemera", ".env"), # Chimera Shared
]

loaded = False
for p in potential_paths:
    if os.path.exists(p):
        load_dotenv(p)
        loaded = True
        break

if not loaded:
    # Fallback to default
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
    VIDEO_GEN = "video_gen"
    SWARM = "swarm"  # Hive Mind

from router.hive_mind import HiveMind

# -----------------------------------------------------------------------------
# Orchestrator Router
# -----------------------------------------------------------------------------
class IntelligenceRouter:
    """
    Central orchestration and routing engine for Aergia Studio.
    
    Coordinates multiple upstream LLM providers, task execution layers, policy 
    verification, and multi-agent plan execution. Includes fallback routing logic 
    to ensure system resilience and execution safety constraints.
    
    Attributes:
        registry (ProviderRegistry): Registry containing active deep learning API providers.
        policy (PolicyEngine): Gating engine enforcing safety, steerability, and system prompt constraints.
        executor (ExecutionEngine): Execution engine that processes TaskRequests.
        planner (Planner): Agentic reasoning engine for multi-step goals.
    """

    def __init__(self):
        """
        Initializes the IntelligenceRouter and registers all available backends.
        """
        self.registry = ProviderRegistry()
        self.policy = PolicyEngine(self.registry)
        self.executor = ExecutionEngine(self.registry, self.policy)
        self.planner = Planner(self.executor)

        logging.info("🧠 Intelligence Router initialized (Orchestrator Mode)")
        logging.info(f"Registered providers: {self.registry.list_ids()}")

    def generate(self, prompt, task_type=TaskType.CODING, system_prompt="", **kwargs):
        """
        Generates content for a given task using the optimal provider routed by policy.
        
        Backward compatible interface that automatically routes requests based on task 
        type, system prompts, and configuration parameters. Enforces fallback pathing 
        on failure.

        Args:
            prompt (str): The primary instructions or query to be processed by the model.
            task_type (TaskType or str, optional): The classification of the task 
                (e.g., TaskType.CODING, TaskType.CREATIVE). Defaults to TaskType.CODING.
            system_prompt (str, optional): System instructions specifying agent constraints. 
                Defaults to "".
            **kwargs: Dynamic arguments passed to the underlying execution provider.

        Returns:
            str: The raw text response content or resource URL (e.g. image link) from the backend.

        Raises:
            ValueError: If the task type is unsupported or policy gating blocks the payload.
            RuntimeError: If execution fails across primary and fallback endpoints.
        """
        # normalize task_type to string
        if isinstance(task_type, Enum):
            task_type_value = task_type.value
        else:
            task_type_value = str(task_type)

        if task_type_value == TaskType.SWARM.value:
            # Hive Mind Execution
            hive = HiveMind(self.registry)
            # Run async loop for the swarm
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            return loop.run_until_complete(hive.swarm(prompt))

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
        Orchestrates execution of a structured TaskRequest.
        
        Validates, policy-checks, and runs the request, returning a comprehensive 
        execution result object with telemetry metadata.

        Args:
            req (TaskRequest): Structured data container representing the task requirements.

        Returns:
            ExecutionResult: Contains response payload, selected provider metadata, and timing metrics.
        """
        return self.executor.execute(req)

    def plan_and_execute(self, goal: str):
        """
        High-level agentic entrypoint for complex multi-step reasoning.
        
        First creates a multi-step execution plan using reasoning models, then 
        orchestrates execution steps sequentially while maintaining state tracking.

        Args:
            goal (str): High-level task description or objective.

        Returns:
            List[ExecutionResult]: Sequence of results from executing plan steps.
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
