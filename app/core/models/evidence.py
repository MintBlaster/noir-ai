from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Any, Annotated
from pydantic import BaseModel, Field


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
    target_value: str = Field(
        ...,
        description="Canonical target value this evidence is about (e.g., example.com).",
    )
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured/parsing result extracted from the raw response.",
    )
    risk_indicators: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Signals or flags (indicator name + metadata) implying risk.",
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
        ..., description="Confidence in this piece of evidence (0.0–1.0)."
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When the evidence was captured."
    )
    cost_tier: str = Field(
        "free",
        description="Acquisition cost tier for this evidence: free, basic, premium.",
    )
    raw_response: str = Field(
        "",
        description="Unprocessed raw output from the source (kept for debugging/audit).",
    )

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "source": "news_search",
                "target_value": "example.com",
                "data": {
                    "title": "Complaint filed against example.com",
                    "snippet": "User reports X...",
                },
                "risk_indicators": [{"indicator": "complaint", "weight": 0.4}],
                "confidence": 0.85,
                "timestamp": "2025-01-15T10:32:00Z",
                "cost_tier": "free",
                "raw_response": '{"articles":[{"title":"Complaint..."}]}',
            }
        }

    def __str__(self) -> str:
        return f"<Evidence {self.source} for {self.target_value} (confidence={self.confidence:.2f})>"

    def __repr__(self) -> str:
        return f"Evidence(source={self.source!r}, target_value={self.target_value!r}, confidence={self.confidence!r})"
