from typing import Any, Dict, List, Optional

from app.core.models.enums import CostTier, TargetType
from app.core.models.step import Step
from app.core.models.target import Target
from app.core.models.evidence import Evidence
from app.core.planning.base import BasePlanner, PlannerError


class MockPlanner(BasePlanner):
    """
    Produces a deterministic sequence of Steps for a given target.
    """

    def __init__(self):
        super().__init__(name="mock")
        self._supported_types = {TargetType.DOMAIN, TargetType.URL, TargetType.IP}

    async def create_plan(
        self, target: Target, context: Optional[Dict[str, Any]] = None
    ) -> List[Step]:
        """Create a deterministic investigation plan."""

        # Validate target type
        if target.type not in self._supported_types:
            raise PlannerError(
                f"MockPlanner doesn't support target type: {target.type}. "
                f"Supported types: {', '.join(t.value for t in self._supported_types)}"
            )

        context = context or {}
        demo_mode = context.get("demo", False)
        step_counter = 1

        steps: List[Step] = []

        # Always start with WHOIS for domains/IPs
        if target.type in {TargetType.DOMAIN, TargetType.URL}:
            steps.append(
                Step(
                    id=f"step_{target.type}_{step_counter:03d}",
                    primitive="whois",
                    params={"domain": target.normalized_value},
                    label="WHOIS Domain Lookup",
                    cost_tier=CostTier.FREE,
                    timeout_s=30,
                    parallel=False,
                )
            )
            step_counter += 1

        # Web search for general information
        steps.append(
            Step(
                id=f"step_{target.type}_{step_counter:03d}",
                primitive="web_search",
                params={
                    "query": target.normalized_value,
                    "max_results": 5 if demo_mode else 3,
                },
                label="Web Search",
                cost_tier=CostTier.FREE,
                timeout_s=15,
                parallel=True,  # Can run in parallel with reputation
            )
        )
        step_counter += 1

        # Reputation check (can run parallel with web search)
        steps.append(
            Step(
                id=f"step_{target.type}_{step_counter:03d}",
                primitive="reputation",
                params={
                    "target": target.normalized_value,
                    "engines": ["virustotal", "safebrowsing"],
                },
                label="Reputation Check",
                cost_tier=CostTier.FREE,
                timeout_s=20,
                parallel=True,
            )
        )
        step_counter += 1

        # Add news search in demo mode or if specifically requested
        if demo_mode or context.get("include_news", False):
            steps.append(
                Step(
                    id=f"step_{target.type}_{step_counter:03d}",
                    primitive="news_search",
                    params={
                        "query": f"{target.normalized_value} scam OR complaints OR fraud",
                        "days_back": 30,
                    },
                    label="News & Complaint Search",
                    cost_tier=CostTier.BASIC,
                    timeout_s=25,
                    parallel=False,
                )
            )
            step_counter += 1

        # Always end with risk scoring (depends on all previous steps)
        steps.append(
            Step(
                id=f"step_{target.type}_{step_counter:03d}",
                primitive="risk_score",
                params={
                    "aggregation_method": "weighted_average",
                    "confidence_threshold": 0.7,
                },
                label="Risk Assessment",
                cost_tier=CostTier.FREE,
                timeout_s=5,
                parallel=False,
            )
        )

        return steps

    async def adapt_plan(
        self, current_plan: List[Step], evidence: List[Evidence]
    ) -> List[Step]:
        """
        Adapt plan based on evidence (simple heuristics for mock).

        In a real implementation, this would analyze evidence and potentially:
        - Add more expensive checks if initial evidence is suspicious
        - Skip remaining steps if confidence is very high/low
        - Add specialized primitives based on findings
        """

        if not evidence:
            return current_plan

        # Simple adaptation: if we find high-risk indicators, add deeper investigation
        high_risk_found = any(
            any(indicator.get("severity") == "high" for indicator in ev.risk_indicators)
            for ev in evidence
        )

        if high_risk_found:
            # Check if we already have news search
            has_news_search = any(
                step.primitive == "news_search" for step in current_plan
            )

            if not has_news_search:
                # Insert news search before the final risk_score step
                risk_score_idx = next(
                    i
                    for i, step in enumerate(current_plan)
                    if step.primitive == "risk_score"
                )

                news_step = Step(
                    id=f"step_adaptive_{len(current_plan):03d}",
                    primitive="news_search",
                    params={
                        "query": f"{evidence[0].target_value} scam OR complaints OR fraud",
                        "days_back": 90,  # Longer search for high-risk cases
                    },
                    label="Deep News Search (High Risk Detected)",
                    cost_tier=CostTier.BASIC,
                    timeout_s=30,
                    parallel=False,
                )

                adapted_plan = current_plan.copy()
                adapted_plan.insert(risk_score_idx, news_step)
                return adapted_plan

        return current_plan
