from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Dict, Any, Annotated
from pydantic import BaseModel, Field, ConfigDict
from .enums import RiskLevel


class RiskReport(BaseModel):
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
    level: RiskLevel = Field(
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
        default_factory=(lambda : datetime.now(timezone.utc)), description="When this report was generated."
    )
    investigation_id: str = Field(
        ..., description="ID of the investigation that produced this report."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata (model used, prompt hash, version info).",
    )

    model_config = ConfigDict(
        from_attributes = True,
        use_enum_values = True,
        json_schema_extra = {
            "example": {
                "target_value": "suspicious-deals.com",
                "score": 75,
                "level": "high",
                "confidence": 0.87,
                "explanation": "High risk domain: newly registered with privacy protection and suspicious naming pattern",
                "evidence_summary": [
                    "Domain registered only 5 days ago",
                    "WHOIS privacy protection enabled",
                    "Domain name contains suspicious keywords",
                ],
                "recommended_actions": [
                    "Exercise extreme caution before visiting",
                    "Verify legitimacy through alternative channels",
                    "Consider blocking domain in security tools",
                ],
                "generated_at": "2025-01-15T10:08:45Z",
                "investigation_id": "inv_20250115_001",
                "metadata": {
                    "scoring_model": "noir_ai_v1.0",
                    "evidence_count": 2,
                    "processing_time_ms": 525,
                },
            }
        }
    )

    def __str__(self) -> str:
        return f"<RiskReport target={self.target_value} score={self.score} level={self.level.value}>"

    def __repr__(self) -> str:
        return f"RiskReport(target_value={self.target_value!r}, score={self.score}, level={self.level!r})"
