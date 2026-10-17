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
