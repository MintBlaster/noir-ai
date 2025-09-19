# backend/app/core/models/evidence.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict

from .enums import CostTier


class Evidence(BaseModel):
    """
    Single piece of evidence gathered during an investigation.

    - `data` should be structured (parsed) output.
    - `raw_response` is preserved for debugging/audit and should not be used
      directly for scoring without parsing.
    """

    source: str = Field(
        ...,
        description="Primitive or tool that produced this evidence (e.g., whois, web_search).",
    )
    step_id: Optional[str] = Field(
        None,
        description="ID of the step that produced this evidence (links to Step.id).",
    )
    target_value: str = Field(
        ...,
        description="Canonical target value this evidence is about (e.g., example.com).",
    )
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured/parsed result extracted from the raw response.",
    )
    risk_indicators: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Signals or flags (indicator name + metadata) implying risk.",
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
        ..., description="Confidence in this piece of evidence (0.0–1.0)."
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the evidence was captured (UTC, timezone-aware).",
    )
    cost_tier: CostTier = Field(
        default=CostTier.FREE,
        description="Acquisition cost tier for this evidence.",
    )
    raw_response: str = Field(
        "",
        description="Unprocessed raw output from the source (kept for debugging/audit).",
    )

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "source": "whois",
                "step_id": "step_whois_001",
                "target_value": "suspicious-deals.com",
                "data": {
                    "domain": "suspicious-deals.com",
                    "creation_date": "2025-01-10T00:00:00Z",
                    "registrar": "Namecheap Inc.",
                    "privacy_protected": True,
                },
                "risk_indicators": [
                    {
                        "type": "new_domain",
                        "severity": "high",
                        "detail": "Domain registered 5 days ago",
                        "score_impact": 25,
                    }
                ],
                "confidence": 0.95,
                "timestamp": "2025-01-15T10:05:30Z",
                "cost_tier": "free",
                "raw_response": "Domain Name: SUSPICIOUS-DEALS.COM\\nCreation Date: 2025-01-10T00:00:00Z...",
            }
        },
    )

    def __str__(self) -> str:
        return f"<Evidence {self.source} for {self.target_value} (confidence={self.confidence:.2f})>"

    def __repr__(self) -> str:
        return f"Evidence(source={self.source!r}, step_id={self.step_id!r}, confidence={self.confidence!r})"
