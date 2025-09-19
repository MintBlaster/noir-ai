from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from .enums import TargetType


class Target(BaseModel):
    """
    Canonical representation of an investigation target.

    Normalizes user input so planners, orchestrators and primitives operate
    on a consistent value set (use `normalized_value` downstream).
    """

    value: str = Field(
        ..., description="Original input provided by the user (unmodified)."
    )
    type: TargetType = Field(
        ..., description="Category of the target, e.g. domain, IP, URL, company."
    )
    normalized_value: str = Field(
        ...,
        description="Cleaned, normalized representation used for lookups (e.g. 'example.com').",
    )
    created_at: datetime = Field(
        default_factory=(lambda: datetime.now(timezone.utc)),
        description="When this Target object was created.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional context (extracted fields, source, notes).",
    )

    model_config = ConfigDict(
        from_attributes = True,
        use_enum_values = True,
        json_schema_extra = {
            "example": {
                "value": "suspicious-deals.com",
                "type": "domain",
                "normalized_value": "suspicious-deals.com",
                "created_at": "2025-01-15T10:00:00Z",
                "metadata": {
                    "original_input": "suspicious-deals.com",
                    "user_agent": "NoirAI/1.0",
                },
            }
        }
    )

    def __str__(self) -> str:
        return f"<Target {self.type.value}: {self.normalized_value}>"

    def __repr__(self) -> str:
        return f"Target(value={self.value!r}, type={self.type!r}, normalized_value={self.normalized_value!r})"
