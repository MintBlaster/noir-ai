from enum import Enum


class CostTier(str, Enum):
    """Cost tiers for operations and evidence acquisition"""

    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class InvestigationStatus(str, Enum):
    """Enumeration of current investigation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    FAILED = "failed"


class RiskLevel(str, Enum):
    """Severity buckets for aggregated risk."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TargetType(str, Enum):
    """Supported investigation target categories."""

    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    COMPANY = "company"
