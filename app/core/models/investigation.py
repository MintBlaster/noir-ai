from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Annotated

from pydantic import BaseModel, Field

from app.core.models.target import Target


class InvestigationStatus(str, Enum):
    """Enumeration of current investigation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    FAILED = "failed"


class Investigation(BaseModel):
    """
    Canonical model for an investigation run.

    Notes
    - `plan` should represent planner output (list of step ids or human-readable step names).
      Use the Step model (when available) for stronger typing.
    - `evidence_collected` stores references (paths/keys/ids) to artifacts; storage backend
      resolves them to URLs when needed.
    """

    id: str = Field(..., description="Unique identifier for the investigation.")
    target: Target = Field(
        ..., description="Canonical target object for this investigation."
    )
    status: InvestigationStatus = Field(
        ..., description="Current lifecycle status of the investigation."
    )
    plan: List[str] = Field(
        default_factory=list,
        description="Ordered list of planned step identifiers or labels.",
    )
    evidence_collected: List[str] = Field(
        default_factory=list,
        description="List of artifact references collected during the run.",
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

    class Config:
        from_attributes = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "id": "inv_1234567890",
                "target": {
                    "value": "https://www.Example.COM/page",
                    "type": "domain",
                    "normalized_value": "example.com",
                    "created_at": "2025-01-15T10:30:00Z",
                    "metadata": {
                        "original_input": "https://www.Example.COM/page",
                        "extracted_domain": "example.com",
                    },
                },
                "status": "pending",
                "plan": ["s1_whois", "s2_web_search"],
                "evidence_collected": ["artifacts/inv_123/whois.txt"],
                "started_at": "2025-01-15T10:30:00Z",
                "completed_at": None,
                "demo_mode": False,
                "settings": {"max_runtime_s": 120},
            }
        }

    def __str__(self) -> str:
        return f"<Investigation {self.id} status={self.status}>"

    def __repr__(self) -> str:
        return (
            f"Investigation(id={self.id!r}, target={self.target!r}, status={self.status!r}, "
            f"plan={self.plan!r}, evidence_count={len(self.evidence_collected)}, started_at={self.started_at!r})"
        )
