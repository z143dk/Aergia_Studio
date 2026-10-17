import json
import logging
from typing import Dict, Any

from router.schemas import TaskRequest, OrchestrationPlan, PlanStep
from router.utils import clean_markdown_fences


class Planner:
    """
    Model-assisted planner:
      - Ask a reasoning model to output a JSON plan
      - Validate/parse
      - Execute steps through the ExecutionEngine
    """

    def __init__(self, executor):
        self.executor = executor
        self.logger = logging.getLogger("Planner")

    def create_plan(self, user_goal: str) -> OrchestrationPlan:
        planning_prompt = f"""
You are the Aergia Orchestrator Planner.

Break the user's goal into a small sequence of atomic steps that can be executed one-by-one.

Allowed task_type values:
- coding
- creative
- reasoning
- context
- image_gen

Rules:
- step_id starts at 1 and increments by 1
- Use depends_on to reference earlier step_ids when needed
- Use output_key to store outputs for later substitution with {{output_key}}

Return ONLY valid JSON in this exact structure:
{{
  "goal": "string",
  "steps": [
    {{
      "step_id": 1,
      "task_type": "creative",
      "prompt": "…",
      "depends_on": [],
      "output_key": "script"
    }}
  ]
}}

User Goal:
{user_goal}
""".strip()

        plan_req = TaskRequest(prompt=planning_prompt, task_type="reasoning")
        plan_res = self.executor.execute(plan_req)

        raw = clean_markdown_fences(plan_res.content)
        try:
            plan_data = json.loads(raw)
            steps = [PlanStep(**s) for s in plan_data["steps"]]
            return OrchestrationPlan(goal=plan_data["goal"], steps=steps)
        except Exception as e:
            self.logger.error(f"Planner JSON parse failed: {e}. Raw={raw[:500]}")
            # Safe fallback: single-step creative response
            return OrchestrationPlan(
                goal=user_goal,
                steps=[PlanStep(step_id=1, task_type="creative", prompt=user_goal, output_key="result")],
                metadata={"planner_error": str(e)},
            )

    def execute_plan(self, plan: OrchestrationPlan) -> Dict[str, Any]:
        context: Dict[str, Any] = {}
        results: Dict[str, Any] = {
            "goal": plan.goal,
            "steps": [],
        }

        # naive: execute in given order (MVP). We'll enforce depends_on later if needed.
        for step in plan.steps:
            final_prompt = step.prompt
            # substitute {{key}} with prior outputs
            for key, val in context.items():
                final_prompt = final_prompt.replace(f"{{{{{key}}}}}", str(val))

            self.logger.info(f"Executing step {step.step_id} ({step.task_type})")

            req = TaskRequest(
                prompt=final_prompt,
                task_type=step.task_type,
                system_prompt="",
                payload={},  # can be extended per-step later
            )
            res = self.executor.execute(req)

            step_record = {
                "step_id": step.step_id,
                "task_type": step.task_type,
                "prompt": final_prompt,
                "output_key": step.output_key,
                "provider_id": res.provider_id,
                "model": res.model,
                "used_fallback": res.used_fallback,
                "elapsed_ms": res.elapsed_ms,
                "content": res.content,
            }
            results["steps"].append(step_record)

            if step.output_key:
                context[step.output_key] = res.content

        results["context"] = context
        return results
