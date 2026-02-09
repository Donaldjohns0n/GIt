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
    assert detector.emergent_tactics()["context-triangulation"] == [
        "Phase 2",
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


def test_log_event_records_intended_action_for_new_platform():
    """Verify log_event uses the caller's action, not just 'open', when a tab
    must be created for a previously-unseen platform."""

    protocol = BrowserOrchestrationProtocol()

    transition = protocol.log_event(
        platform="ChatGPT",
        action="synthesize",
        context_snapshot="First interaction",
    )

    # The returned transition must carry the intended action.
    assert transition.action == "synthesize"

    # The timeline should contain two entries: the implicit "open" and then
    # the intended "synthesize" action.
    timeline = protocol.timeline()
    assert len(timeline) == 2
    assert timeline[0].action == "open"
    assert timeline[0].platform == "ChatGPT"
    assert timeline[1].action == "synthesize"
    assert timeline[1].platform == "ChatGPT"
    assert timeline[1].tab_id == timeline[0].tab_id


def test_log_event_uses_action_on_existing_tab():
    """Ensure log_event still works correctly for platforms with existing
    tabs (the non-buggy path)."""

    protocol = BrowserOrchestrationProtocol()
    protocol.open_tab(platform="Claude", context_summary="Initial context")

    transition = protocol.log_event(
        platform="Claude",
        action="validate",
        context_snapshot="Cross-check findings",
    )

    assert transition.action == "validate"
    timeline = protocol.timeline()
    # One "open" from open_tab, one "validate" from log_event.
    assert len(timeline) == 2
    assert timeline[0].action == "open"
    assert timeline[1].action == "validate"


def test_execute_phase_browser_timeline_matches_audit_log():
    """The browser protocol timeline and audit log should agree on actions
    recorded via browser_events in execute_phase."""

    agent = build_agent()
    agent.execute_phase(
        "Phase 1",
        version="v1",
        meta_prompt="Evaluate findings",
        rationale="Bootstrap",
        paradox_observation="None",
        browser_events=[
            ("ChatGPT", "synthesize", "Compiled debate summary"),
            ("Claude", "validate", "Cross-check paradox rationale"),
        ],
    )

    timeline = agent.browser_protocol.timeline()
    audit_browser = [
        entry
        for entry in agent.audit_log.history()
        if entry.action.startswith("browser:")
    ]

    # Each browser_event should produce an audit entry with the intended action.
    assert len(audit_browser) == 2
    assert audit_browser[0].action == "browser:synthesize"
    assert audit_browser[1].action == "browser:validate"

    # The timeline should contain the intended actions (not just "open").
    timeline_actions = [t.action for t in timeline]
    assert "synthesize" in timeline_actions
    assert "validate" in timeline_actions
