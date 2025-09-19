import pytest

from app.core.models.enums import TargetType
from app.core.models.step import Step
from app.core.models.target import Target
from app.core.models.evidence import Evidence
from app.core.planning.base import PlannerError
from app.core.planning.mock_planner import MockPlanner


@pytest.mark.asyncio
async def test_create_plan_demo_mode():
    planner = MockPlanner()
    target = Target(
        value="https://Example.COM/page",
        type=TargetType.DOMAIN,
        normalized_value="example.com",
    )

    plan = await planner.create_plan(target, context={"demo": True})

    # Check types and structure
    assert isinstance(plan, list)
    assert all(isinstance(s, Step) for s in plan)
    assert len(plan) >= 4  # At least whois, web_search, news_search, risk_score

    # Plan should include all expected primitives in demo mode
    primitive_names = [s.primitive for s in plan]
    assert "whois" in primitive_names
    assert "web_search" in primitive_names
    assert "news_search" in primitive_names
    assert "risk_score" in primitive_names

    # IDs should be unique and well-formatted
    ids = [s.id for s in plan]
    assert len(ids) == len(set(ids)), "Step IDs must be unique"
    assert all(s.id.startswith("step_domain_") for s in plan)

    # Risk score should always be last
    assert plan[-1].primitive == "risk_score"


@pytest.mark.asyncio
async def test_create_plan_non_demo_mode():
    planner = MockPlanner()
    target = Target(
        value="example.com",
        type=TargetType.DOMAIN,
        normalized_value="example.com",
    )

    plan = await planner.create_plan(target, context={"demo": False})
    primitives = [s.primitive for s in plan]

    # Should not include news search by default
    assert "news_search" not in primitives
    assert "risk_score" in primitives

    # Should still have core primitives
    assert "whois" in primitives
    assert "web_search" in primitives
    assert "reputation" in primitives


@pytest.mark.asyncio
async def test_create_plan_unsupported_target_type():
    planner = MockPlanner()
    target = Target(
        value="Acme Corporation",
        type=TargetType.COMPANY,
        normalized_value="acme corporation",
    )

    with pytest.raises(PlannerError) as exc_info:
        await planner.create_plan(target)

    assert "doesn't support target type: company" in str(exc_info.value)


@pytest.mark.asyncio
async def test_adapt_plan_with_high_risk_evidence():
    planner = MockPlanner()
    target = Target(
        value="suspicious.com",
        type=TargetType.DOMAIN,
        normalized_value="suspicious.com",
    )

    # Create initial plan (no demo mode, so no news search)
    initial_plan = await planner.create_plan(target, context={"demo": False})
    initial_primitives = [s.primitive for s in initial_plan]
    assert "news_search" not in initial_primitives

    # Create high-risk evidence
    high_risk_evidence = [
        Evidence(
            source="whois",
            target_value="suspicious.com",
            data={"creation_date": "2025-01-14"},
            risk_indicators=[
                {
                    "type": "new_domain",
                    "severity": "high",
                    "detail": "Created yesterday",
                }
            ],
            confidence=0.95,
            step_id="step_whois_001",
            raw_response="Domain Name: SUSPICIOUS-DEALS.COM\\nCreation Date: 2025-01-14...",
        )
    ]

    # Adapt plan based on evidence
    adapted_plan = await planner.adapt_plan(initial_plan, high_risk_evidence)
    adapted_primitives = [s.primitive for s in adapted_plan]

    # Should now include news search
    assert "news_search" in adapted_primitives
    assert len(adapted_plan) > len(initial_plan)

    # Risk score should still be last
    assert adapted_plan[-1].primitive == "risk_score"


@pytest.mark.asyncio
async def test_adapt_plan_no_evidence():
    planner = MockPlanner()
    target = Target(
        value="example.com",
        type=TargetType.DOMAIN,
        normalized_value="example.com",
    )

    initial_plan = await planner.create_plan(target)
    adapted_plan = await planner.adapt_plan(initial_plan, evidence=[])

    # Should be unchanged
    assert adapted_plan == initial_plan


@pytest.mark.asyncio
async def test_step_id_generation():
    planner = MockPlanner()
    target = Target(
        value="test.com",
        type=TargetType.DOMAIN,
        normalized_value="test.com",
    )

    plan = await planner.create_plan(target)

    # Check ID format and uniqueness
    for i, step in enumerate(plan, 1):
        assert step.id == f"step_domain_{i:03d}"
