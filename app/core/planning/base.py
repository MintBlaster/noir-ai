from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.core.models.step import Step
from app.core.models.target import Target
from app.core.models.evidence import Evidence


class PlannerError(Exception):
    """Raised when planner fails to produce or adapt a plan."""

    pass


class BasePlanner(ABC):
    """
    Base interface for all investigation planners.

    Planners decide what steps to take during an investigation.
    - MockPlanner: returns a fixed deterministic plan (for dev/demo).
    - BedrockPlanner: queries an LLM to reason about targets and evidence.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def create_plan(
        self, target: Target, context: Optional[Dict[str, Any]] = None
    ) -> List[Step]:
        """
        Create an investigation plan for the given target.

        Args:
            target: The target under investigation.
            context: Optional extra context (prior evidence, preferences).

        Returns:
            List of Step objects to execute.

        Raises:
            PlannerError: If planning fails or target is unsupported.
        """
        raise NotImplementedError

    @abstractmethod
    async def adapt_plan(
        self, current_plan: List[Step], evidence: List[Evidence]
    ) -> List[Step]:
        """
        Adapt an existing plan given new evidence.

        Args:
            current_plan: Steps generated earlier.
            evidence: Evidence collected so far.

        Returns:
            Updated plan (may add/remove/modify steps).

        Raises:
            PlannerError: If adaptation fails.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}>"
