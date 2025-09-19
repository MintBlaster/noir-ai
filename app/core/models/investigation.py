from __future__ import annotations
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from .target import Target
from .step import Step
from .evidence import Evidence
from .enums import InvestigationStatus


class Investigation(BaseModel):
    """
    Canonical model for an investigation run.

    Orchestrates the execution of a plan (Steps) and collects results (Evidence).
    """

    id: str = Field(..., description="Unique identifier for the investigation.")
    target: Target = Field(
        ..., description="Canonical target object for this investigation."
    )
    status: InvestigationStatus = Field(
        default=InvestigationStatus.PENDING,
        description="Current lifecycle status of the investigation.",
    )
    plan: List[Step] = Field(
        default_factory=list,
        description="Ordered list of steps to execute (from planner).",
    )
    evidence_collected: List[Evidence] = Field(
        default_factory=list,
        description="Evidence gathered during execution.",
    )
    started_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the investigation started."
    )
    completed_at: Optional[datetime] = Field(
        None, description="When the investigation completed (populated on finish)."
    )
    demo_mode: bool = Field(
        default=False, description="Whether the investigation was run in demo mode."
    )
    settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional runtime settings for the investigation (non-sensitive).",
    )

    model_config = ConfigDict(
        from_attributes = True,
        use_enum_values = True,
        json_schema_extra = {
            "example": {
                "id": "inv_20250115_001",
                "target": {
                    "value": "suspicious-deals.com",
                    "type": "domain",
                    "normalized_value": "suspicious-deals.com",
                    "created_at": "2025-01-15T10:00:00Z",
                    "metadata": {"original_input": "suspicious-deals.com"},
                },
                "status": "completed",
                "plan": [
                    {
                        "id": "step_whois_001",
                        "primitive": "whois",
                        "params": {"domain": "suspicious-deals.com"},
                        "label": "WHOIS Domain Lookup",
                        "cost_tier": "free",
                    }
                ],
                "evidence_collected": [
                    {
                        "source": "whois",
                        "step_id": "step_whois_001",
                        "target_value": "suspicious-deals.com",
                        "confidence": 0.95,
                        "cost_tier": "free",
                    }
                ],
                "started_at": "2025-01-15T10:00:00Z",
                "completed_at": "2025-01-15T10:08:45Z",
                "demo_mode": False,
                "settings": {"max_cost_tier": "basic", "timeout_total_s": 300},
            }
        }
    )

    def __str__(self) -> str:
        return f"<Investigation {self.id} status={self.status.value}>"

    def __repr__(self) -> str:
        return (
            f"Investigation(id={self.id!r}, target={self.target.normalized_value!r}, "
            f"status={self.status!r}, evidence_count={len(self.evidence_collected)})"
        )
