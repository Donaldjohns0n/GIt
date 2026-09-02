"""Tests for the unified meta-orchestration framework."""

from __future__ import annotations

import pytest

from src import (
    AuditLog,
    BrowserOrchestrationProtocol,
    EmergentTacticDetector,
    MetaOrchestrationFramework,
    MetaPromptTracker,
    ParadoxCatalog,
    ParadoxEntry,
    PlanOfWorkMatrix,
    ResearchAgent,
    RoleResponsibilityLedger,
    StrategicArchitecture,
    StrategicComponent,
    TestScenario,
    TestingStrategy,
)


def build_agent() -> ResearchAgent:
    tracker = MetaPromptTracker()
    detector = EmergentTacticDetector(threshold=2)
    paradox_catalog = ParadoxCatalog()
    audit_log = AuditLog()
    browser_protocol = BrowserOrchestrationProtocol()
    architecture = StrategicArchitecture()
    architecture.add_component(
        StrategicComponent(
            name="context_extractor",
            responsibilities=(
                "capture session context",
                "synchronize prompts",
            ),
            outputs=("context ledger",),
        )
    )
    ledger = RoleResponsibilityLedger()
    plan = PlanOfWorkMatrix()
    testing = TestingStrategy()
    testing.plan_phase_tests(
        "Phase 1",
        [
            TestScenario(
                name="pytest",
                objective="validate unit coverage",
                command="pytest -q",
                coverage=("summarizer", "meta_orchestration"),
            )
        ],
    )
    agent = ResearchAgent(
        name="research_orchestrator",
        phases=("Phase 1", "Phase 2", "Phase 3", "Phase 4"),
        meta_prompt_tracker=tracker,
        tactic_detector=detector,
        paradox_catalog=paradox_catalog,
        audit_log=audit_log,
        browser_protocol=browser_protocol,
        architecture=architecture,
        testing_strategy=testing,
        responsibility_ledger=ledger,
        plan_of_work=plan,
    )
    return agent


def test_meta_prompt_tracker_prevents_duplicates():
    tracker = MetaPromptTracker()
    tracker.register_version(
        version="v1",
        prompt="Analyze prior instruction",
        rationale="Baseline orchestration",
        paradox_observation="Self-reference loop detected",
    )
    with pytest.raises(ValueError):
        tracker.register_version(
            version="v1",
            prompt="Refined prompt",
            rationale="Duplicate",
            paradox_observation="n/a",
        )


def test_emergent_tactic_detector_flags_new_tactic():
    detector = EmergentTacticDetector(threshold=2)
    assert detector.record(
        phase="Phase 1",
        tactic="context-triangulation",
    ) is False
    assert detector.record(
        phase="Phase 2",
        tactic="context-triangulation",
    ) is True
    assert detector.record(
        phase="Phase 3",
        tactic="context-triangulation",
    ) is False
    assert detector.record(
        phase="Phase 3",
        tactic="context-triangulation",
    ) is False
    assert detector.emergent_tactics()["context-triangulation"] == [
        "Phase 2",
        "Phase 3",
    ]


def test_research_agent_executes_phase_and_updates_framework():
    agent = build_agent()
    paradox = ParadoxEntry(
        name="instruction recursion",
        description="Meta prompts require meta-evaluation",
        severity="high",
        version="v1",
        resolution_strategy="Introduce meta-meta audit",
    )
    record = agent.execute_phase(
        "Phase 1",
        version="v1",
        meta_prompt="Self-evaluate and refine",
        rationale="Bootstrap",
        paradox_observation="Recursive dependency identified",
        counter_intuitive_discovery=(
            "Constrained autonomy increases paradox detection"
        ),
        outputs={"deliverable": "phase 1 dossier"},
        paradox_entries=[paradox],
        tactics=["context-triangulation", "context-triangulation"],
        audit_notes=("kickoff",),
        browser_events=[
            (
                "ChatGPT",
                "synthesize",
                "Compiled debate summary",
            ),
            (
                "Claude",
                "validate",
                "Cross-check paradox rationale",
            ),
        ],
        test_results={"pytest": "pass"},
    )

    assert record.phase == "Phase 1"
    assert record.version == "v1"
    assert record.paradoxes == [paradox]
    assert record.emergent_tactics == ["context-triangulation"]
    assert agent.meta_prompt_tracker.latest().version == "v1"
    assert agent.paradox_catalog.all_entries() == [paradox]
    assert agent.browser_protocol.context_matrix()[
        "Claude"
    ].startswith("Cross-check")
    assert agent.testing_strategy.execution_results("Phase 1") == {
        "pytest": "pass"
    }

    framework = MetaOrchestrationFramework(agent=agent)
    roadmap = framework.actionable_roadmap()
    assert any("instruction recursion" in item for item in roadmap)
    assert framework.meta_prompt_log()[0].version == "v1"
    assert framework.documentation_summary()["components"] == [
        "context_extractor"
    ]


def test_role_responsibility_unification_and_plan_of_work():
    agent = build_agent()

    definition = agent.register_role_definition(
        phase="Phase 1",
        version="v1",
        role="Orchestrator",
        perspective="Systems synthesis overseer",
        responsibilities=(
            "sequence phases",
            "mediate debate protocol",
            "enforce paradox catalog logging",
        ),
        inputs=("agent briefs", "audit trail"),
        outputs=("phase alignment report",),
        dependencies=("workflow_synthesizer", "audit_critic"),
        context_boundaries=("cross-platform orchestration",),
        negotiation_protocols=("debate protocol arbitration",),
        escalation_paths=(
            "notify audit_critic",
            "escalate to meta-review",
        ),
    )
    assert definition.role == "Orchestrator"
    assert agent.responsibility_ledger.role("Orchestrator").perspective == (
        "Systems synthesis overseer"
    )

    overlap = agent.register_role_overlap(
        phase="Phase 1",
        version="v1",
        roles=("Orchestrator", "Audit Critic"),
        nuance="Both evaluate debate outputs for traceability",
        resolution_protocol=(
            "Audit Critic validates evidence before Orchestrator finalizes"
        ),
        triggers=("phase-close", "context-switch ambiguity"),
    )
    assert overlap.roles == ("Orchestrator", "Audit Critic")

    context_shift = agent.register_context_shift(
        phase="Phase 2",
        version="v2",
        platform="Claude",
        description="Claude tab focuses on risk framing",
        ambiguity="Risk lens can override orchestration priorities",
        resolution_protocol=(
            "Mediator role captures deltas and revalidates with Orchestrator"
        ),
        affected_roles=("Mediator", "Orchestrator"),
    )
    assert context_shift.platform == "Claude"
    assert agent.responsibility_ledger.context_shifts()

    entry = agent.add_plan_of_work_entry(
        phase="Phase 2",
        version="v2",
        context="Debate escalation",
        responsible_roles=("Orchestrator", "Mediator", "Audit Critic"),
        tasks=(
            "collect arguments",
            "triage disagreements",
            "log paradox counterpoints",
        ),
        data_inputs=("debate transcript", "tab context matrix"),
        outputs=("synthesized resolution", "paradox annotations"),
        handoffs=("Mediator -> Orchestrator", "Orchestrator -> Audit Critic"),
        paradox_checks=("ensure paradox catalog updated",),
        escalation_paths=("invoke meta-review",),
        joint_actions=("Mediator and Audit Critic co-author risk note",),
    )
    assert entry.context == "Debate escalation"
    table = agent.plan_of_work.as_table()
    assert table[0]["responsible_roles"] == [
        "Orchestrator",
        "Mediator",
        "Audit Critic",
    ]

    audited_actions = {
        record.action
        for record in agent.audit_log.history()
        if "-" in record.action
    }
    assert {
        "role-definition",
        "role-overlap",
        "context-shift",
        "plan-of-work",
    } <= audited_actions
