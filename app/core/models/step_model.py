from __future__ import annotations
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class Step(BaseModel):
    """
    Planner -> Orchestrator step contract.

    Defines the atomic unit of work in an investigation plan.
    Produced by the planner and consumed by the orchestrator.
    """

    id: str = Field(..., description="Unique step id (planner assigned).")
    primitive: str = Field(
        ..., description="Name of the primitive/task to execute (e.g., 'whois')."
    )
    params: Dict[str, Any] = Field(
        default_factory=dict, description="Structured parameters for the primitive."
    )
    parallel: bool = Field(
        default=False, description="If true, this step can be executed concurrently."
    )
    label: Optional[str] = Field(
        None, description="Optional human-friendly label for UI display."
    )
    timeout_s: Optional[int] = Field(
        None, description="Optional per-step timeout in seconds."
    )
    cost_tier: str = Field(
        "free",
        description="Expected acquisition cost tier for this step: free, basic, premium.",
    )

    class Config:
        from_attributes = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "id": "s1",
                "primitive": "whois",
                "params": {"domain": "example.com"},
                "parallel": False,
                "label": "WHOIS lookup",
                "timeout_s": 10,
                "cost_tier": "free",
            }
        }

    def __str__(self) -> str:
        return f"<Step {self.id}: {self.primitive} (parallel={self.parallel})>"

    def __repr__(self) -> str:
        return f"Step(id={self.id!r}, primitive={self.primitive!r}, parallel={self.parallel}, cost_tier={self.cost_tier!r})"
