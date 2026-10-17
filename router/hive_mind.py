import asyncio
import json
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

from router.schemas import TaskRequest
from router.registry import ProviderRegistry, ProviderIDs
from router.policy import PolicyEngine

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HiveMind")

@dataclass
class SubTask:
    id: int
    instruction: str
    role: str # 'researcher', 'analyst', 'coder'

class HiveMind:
    """
    The Swarm Orchestrator.
    Manages parallel execution of specialized sub-agents.
    """
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self.policy = PolicyEngine(registry) # [NEW] Use Policy Engine for routing
        # Default to a fast model for workers
        self.worker_model_id =ProviderIDs.GOOGLE_GEMINI_FLASH 
        # Default to a smart model for the manager
        self.manager_model_id = ProviderIDs.GOOGLE_GEMINI_PRO

    async def swarm(self, goal: str) -> str:
        """
        Main entry point.
        1. Breaks goal into subtasks (Manager).
        2. Executes subtasks in parallel (Workers).
        3. Synthesizes results (Manager).
        """
        logger.info(f"🐝 HiveMind Activated. Goal: {goal}")

        # 1. Plan
        subtasks = await self._plan_tasks(goal)
        if not subtasks:
            return "Failed to generate a plan."
        
        logger.info(f"📋 Plan generated: {len(subtasks)} tasks.")

        # 2. Execute (Parallel)
        tasks = [self._execute_worker(t) for t in subtasks]
        results = await asyncio.gather(*tasks)
        
        # 3. Synthesize
        final_output = await self._synthesize(goal, results)
        return final_output

    async def _plan_tasks(self, goal: str) -> List[SubTask]:
        """Manager Agent: Breaks down the goal."""
        system_prompt = """
        You are the Hive Manager. 
        Break the user's goal into 2-5 distinct, parallelizable subtasks.
        
        CRITICAL RULES:
        1.  **Stop Loss:** Every trade plan MUST include a precise Stop Loss level.
        2.  **Ratchet:** For winning trades, define how to move the stop loss up (Trailing Stop) to lock in max profit.
        3.  **Weekend Analysis:** If asked for "Next Week", ensure researchers look for upcoming catalysts/earnings.
        
        Return JSON format:
        {
            "tasks": [
                {"id": 1, "role": "researcher", "instruction": "..."},
                {"id": 2, "role": "analyst", "instruction": "..."}
            ]
        }
        Roles: 
        - 'researcher' (News/Docs -> Kimi/Gemini), 
        - 'analyst' (Logic/Math -> DeepSeek R1), 
        - 'strategist' (Synthesis -> Gemini/V3).
        """
        
        provider = self.registry.get(self.manager_model_id) or self.registry.get_any()
        if not provider:
            raise ValueError("No providers available for HiveMind.")

        # Sync call wrapped in async (until providers are async)
        # In a real async system, provider.generate would be awaitable.
        # For now, we assume fast execution or wrap if needed.
        response = provider.generate(goal, system_prompt=system_prompt)
        
        try:
            # Clean markdown (response is a dict)
            content = response.get("content", "") if isinstance(response, dict) else response.content
            text = content.replace("```json", "").replace("```", "").strip()
            # Handle potential preamble
            if "{" in text: text = text[text.find("{"):text.rfind("}")+1]
            
            data = json.loads(text)
            return [SubTask(**t) for t in data.get("tasks", [])]
        except Exception as e:
            logger.error(f"Planning Error: {e}")
            return []

    async def _execute_worker(self, task: SubTask) -> str:
        """Worker Agent: Executes a single subtask."""
        logger.info(f"🐜 Worker {task.id} ({task.role}) starting: {task.instruction[:30]}...")
        
        system_prompt = f"""
        You are a generic {task.role} agent.
        <thinking>
        First, think step-by-step about how to solve the task.
        </thinking>
        Then provide the final output.
        """
        
        # Simulate async work for now since underlying calls are sync requests
        # In production this allows non-blocking HTTP
        await asyncio.sleep(0.1) 
        
        # Intelligent Routing via Policy Engine
        # Map Hive role to Policy task type
        policy_task_type = f"hive_{task.role}"
        decision = self.policy.decide(policy_task_type)
        provider_id = decision.primary
        
        provider = self.registry.get(provider_id)
        logger.info(f"🐜 Worker {task.id} using Provider: {provider_id} (Reason: {decision.reasons[0]})")
        
        try:
            response = provider.generate(task.instruction, system_prompt=system_prompt)
            content = response.get("content", "") if isinstance(response, dict) else response.content
            logger.info(f"✅ Worker {task.id} finished.")
            return f"--- Task {task.id} ({task.role} / {provider_id}) Result ---\n{content}\n"
        except Exception as e:
             logger.error(f"Worker {task.id} Failed: {e}")
             # Try fallback if available?
             if decision.fallbacks:
                 fallback_id = decision.fallbacks[0]
                 logger.info(f"⚠️ Worker {task.id} retrying with fallback: {fallback_id}")
                 try:
                     fb_provider = self.registry.get(fallback_id)
                     resp = fb_provider.generate(task.instruction, system_prompt=system_prompt)
                     content = resp.get("content", "") if isinstance(resp, dict) else resp.content
                     return f"--- Task {task.id} ({task.role} / {fallback_id} [FALLBACK]) Result ---\n{content}\n"
                 except Exception as e2:
                     return f"Error in Task {task.id} (Primary & Fallback): {e2}"
             return f"Error in Task {task.id}: {e}"

    async def _synthesize(self, goal: str, worker_results: List[str]) -> str:
        """Manager Agent: Combines work."""
        combined_data = "\n".join(worker_results)
        
        prompt = f"""
        original_goal: {goal}
        
        worker_outputs:
        {combined_data}
        
        Synthesize these findings into a cohesive final report.
        """
        
        provider = self.registry.get(self.manager_model_id) or self.registry.get_any()
        response = provider.generate(prompt, system_prompt="You are the Hive Manager. Synthesize the team's work.")
        
        content = response.get("content", "") if isinstance(response, dict) else response.content
        return content
