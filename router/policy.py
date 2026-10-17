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

        # --- FINANCIAL TASKS ---
        if t in ("financial_analysis", "finance", "trading", "stock", "crypto", "market"):
            # Determine asset class from prompt
            prompt_content = (payload.get("prompt") or "").upper()
            
            # Crypto keywords -> Coinbase
            if any(k in prompt_content for k in ["BTC", "ETH", "SOL", "DOGE", "COINBASE", "CRYPTO"]):
                if self.registry.has(ProviderIDs.COINBASE):
                    return RoutingDecision(
                        primary=ProviderIDs.COINBASE,
                        fallbacks=[],
                        reasons=["task=finance+crypto -> coinbase"],
                    )
            
            # Default/Stocks -> Schwab
            if self.registry.has(ProviderIDs.SCHWAB):
                return RoutingDecision(
                    primary=ProviderIDs.SCHWAB,
                    fallbacks=[], # Could fallback to Coinbase for generic balance check if implemented
                    reasons=["task=finance -> schwab"],
                )
            
            # Fallback if specific finance provider missing
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                reasons=["finance task but no finance provider -> gemini (analysis only)"]
            )

        # --- MEDIA TASKS ---
        if t in ("image_gen", "image", "image_generation"):
            return RoutingDecision(
                primary=ProviderIDs.FAL_FLUX_SCHNELL,
                fallbacks=[],
                reasons=["task=image_gen -> fal flux schnell"],
            )

        if t in ("video_gen", "video", "minimax"):
            return RoutingDecision(
                primary=ProviderIDs.FAL_VIDEO_MINIMAX,
                fallbacks=[],
                reasons=["task=video_gen -> fal video minimax"],
            )

        # --- AVATAR / VIDEO TASKS ---
        if t in ("avatar", "longcat", "talking_head"):
            if self.registry.has(ProviderIDs.LONGCAT):
                return RoutingDecision(
                    primary=ProviderIDs.LONGCAT,
                    fallbacks=[], 
                    reasons=["task=avatar -> longcat"],
                )
            return RoutingDecision(
                primary=ProviderIDs.GOOGLE_GEMINI_FLASH,
                fallbacks=[],
                reasons=["task=avatar but no longcat -> gemini (fallback)"],
            )

        # --- HIVE SWARM ROLES (Dynamic Orchestration) ---
        if t == "hive_analyst":
            # DeepSeek R1 (Reasoning) > DeepSeek V3 > Gemini Pro
            if self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_R1):
                return RoutingDecision(primary=ProviderIDs.OPENROUTER_DEEPSEEK_R1, fallbacks=[ProviderIDs.GOOGLE_GEMINI_PRO], reasons=["role=analyst -> deepseek r1"])
            return RoutingDecision(primary=ProviderIDs.GOOGLE_GEMINI_PRO, fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH], reasons=["role=analyst -> gemini pro"])

        if t == "hive_researcher":
            # Kimi (Long Context) > Gemini Pro > DeepSeek V3
            if self.registry.has(ProviderIDs.OPENROUTER_KIMI):
                return RoutingDecision(primary=ProviderIDs.OPENROUTER_KIMI, fallbacks=[ProviderIDs.GOOGLE_GEMINI_PRO], reasons=["role=researcher -> kimi"])
            return RoutingDecision(primary=ProviderIDs.GOOGLE_GEMINI_PRO, fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH], reasons=["role=researcher -> gemini pro"])

        if t == "hive_strategist":
            # Gemini Pro (Synthesis) > DeepSeek V3
            if self.registry.has(ProviderIDs.GOOGLE_GEMINI_PRO):
                return RoutingDecision(primary=ProviderIDs.GOOGLE_GEMINI_PRO, fallbacks=[ProviderIDs.OPENROUTER_DEEPSEEK_V3], reasons=["role=strategist -> gemini pro"])
            return RoutingDecision(primary=ProviderIDs.GOOGLE_GEMINI_FLASH, fallbacks=[], reasons=["role=strategist -> gemini flash"])

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
            # Prefer Longcat for long-form scripts if available
            if self.registry.has(ProviderIDs.LONGCAT):
                 return RoutingDecision(
                    primary=ProviderIDs.LONGCAT,
                    fallbacks=[ProviderIDs.OPENROUTER_DEEPSEEK_V3, ProviderIDs.GOOGLE_GEMINI_FLASH],
                    reasons=["task=creative -> longcat (long context support)"],
                )
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

        # --- EDGE / LOCAL OFFLINE ---
        if t in ("edge", "local", "offline"):
            if self.registry.has(ProviderIDs.OLLAMA_LOCAL):
                return RoutingDecision(
                    primary=ProviderIDs.OLLAMA_LOCAL,
                    fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH],
                    reasons=["task=edge/local -> ollama local"],
                )

        # --- SPEED / DEFAULT CHAT ---
        if self.registry.has(ProviderIDs.OLLAMA_LOCAL):
            # Prefer free local AI for default chat if running
            return RoutingDecision(
                primary=ProviderIDs.OLLAMA_LOCAL,
                fallbacks=[ProviderIDs.GOOGLE_GEMINI_FLASH],
                reasons=["default -> ollama local (free)"],
            )
        elif self.registry.has(ProviderIDs.OPENROUTER_DEEPSEEK_V3):
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
