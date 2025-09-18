from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field


class TargetType(str, Enum):
    """Supported investigation target categories."""

    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    COMPANY = "company"


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
        default_factory=datetime.now, description="When this Target object was created."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional context (extracted fields, source, notes).",
    )

    class Config:
        from_attributes = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "value": "https://www.Example.COM/page",
                "type": "domain",
                "normalized_value": "example.com",
                "created_at": "2025-01-15T10:30:00Z",
                "metadata": {
                    "original_input": "https://www.Example.COM/page",
                    "extracted_domain": "example.com",
                },
            }
        }

    def __str__(self) -> str:
        return f"<Target {self.type}: {self.normalized_value}>"

    def __repr__(self) -> str:
        return f"Target(value={self.value!r}, type={self.type!r}, normalized_value={self.normalized_value!r})"
