from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Annotated

from pydantic import BaseModel, Field, conint, confloat


class RiskReportLevel(str, Enum):
    """Severity buckets for aggregated risk."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskReportModel(BaseModel):
    """
    Aggregated risk assessment produced by an investigation.

    - `score` is an integer 0–100 representing the composite risk.
    - `confidence` is the model/evidence confidence for this assessment (0.0–1.0).
    - `evidence_summary` should be short, human-readable bullets pulled from evidence.
    - `recommended_actions` are prioritized suggestions for the user.
    """

    target_value: str = Field(
        ..., description="Canonical target value assessed (e.g., example.com)."
    )
    score: Annotated[int, Field(ge=0, le=100)] = Field(
        ..., description="Composite risk score, 0 (low) to 100 (high)."
    )
    level: RiskReportLevel = Field(
        ..., description="Categorical risk level derived from the score."
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
        ..., description="Confidence in this assessment (0.0–1.0)."
    )
    explanation: str = Field(
        ..., description="Short human-readable explanation for the assessment."
    )
    evidence_summary: List[str] = Field(
        default_factory=list,
        description="Key findings that materially influenced the score.",
    )
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Concrete next steps for the user (prioritized).",
    )
    generated_at: datetime = Field(
        default_factory=datetime.now, description="When this report was generated."
    )
    investigation_id: str = Field(
        ..., description="ID of the investigation that produced this report."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata (model used, prompt hash, version info).",
    )

    class Config:
        from_attributes = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "target_value": "sketchy-site.com",
                "score": 85,
                "level": "high",
                "confidence": 0.92,
                "explanation": "High risk: newly registered domain + multiple negative signals.",
                "evidence_summary": [
                    "Domain created 5 days ago",
                    "Multiple negative forum posts mentioning fraud",
                    "3 security engines flagged malware",
                ],
                "recommended_actions": [
                    "Do not visit this site",
                    "Block domain in perimeter controls",
                    "Escalate to security team",
                ],
                "generated_at": "2025-01-15T10:35:00Z",
                "investigation_id": "inv_abc123",
                "metadata": {
                    "model": "bedrock:anthropic.claude-2o",
                    "prompt_hash": "sha256:...",
                },
            }
        }

    def __str__(self) -> str:
        return f"<RiskReport target={self.target_value} score={self.score} level={self.level}>"

    def __repr__(self) -> str:
        return f"RiskReportModel(target_value={self.target_value!r}, score={self.score}, level={self.level!r})"
