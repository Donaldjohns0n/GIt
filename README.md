
# Cursor CLI & Recursive Meta-Orchestration Framework

Cursor CLI lets you interact with AI agents directly from your terminal to write, review, and modify code. Whether you prefer an interactive terminal interface or want print-style automation for scripts and CI pipelines, the CLI provides powerful coding assistance right where you work.

This repository extends Cursor CLI with a **Unified Recursive Meta-Orchestration Framework** — a Python library and documentation suite for running multi-agent research experiments with full auditability, paradox tracking, and browser-context orchestration.

---

## Getting Started with Cursor CLI

### Install
```bash
curl https://cursor.com/install -fsS | bash
```

### Run an Interactive Session
```bash
cursor-agent
```

Cursor CLI is currently in beta—we'd love your feedback on it!

### Interactive Mode

Start a conversational session with the agent to describe your goals, review proposed changes, and approve commands:

```bash
# Start interactive session
cursor-agent

# Start with initial prompt
cursor-agent "refactor the auth module to use JWT tokens"
```

### Non-Interactive Mode

Use print mode for non-interactive scenarios like scripts, CI pipelines, or automation:

```bash
# Run with specific prompt and model
cursor-agent -p "find and fix performance issues" --model "gpt-5"

# Use with git changes included for review
cursor-agent -p "review these changes for security issues" --output-format text
```

### Sessions

Resume previous conversations to maintain context across multiple interactions:

```bash
# List all previous chats
cursor-agent ls

# Resume latest conversation
cursor-agent resume

# Resume specific conversation
cursor-agent --resume="chat-id-here"
```

---

## Meta-Orchestration Framework

The root modules `meta_orchestration.py` and `summarizer.py` provide a deployable orchestration system that consolidates four experiment iterations:

- **V1 — Research Agent Implementation:** Phase-aware execution engine with detailed governance hooks.
- **V2 — Strategic Architecture:** Component model aligning context extraction, workflow synthesis, audit review, and prompt stewardship.
- **V3 — Testing Strategy:** Sample-and-test loops and validation triggers mapped to each orchestration phase.
- **V4 — Planning Dossier:** Operational cadence, paradox anticipation, and documentation commitments.

### Key Components

| Component | Class | Purpose |
| --- | --- | --- |
| Research Agent | `ResearchAgent` | Executes phases; drives audit, paradox, meta-prompt, and browser protocols in lockstep |
| Meta-Prompt Tracker | `MetaPromptTracker` | Records every prompt iteration with rationale, paradox observations, and counter-intuitive discoveries |
| Emergent Tactic Detector | `EmergentTacticDetector` | Flags tactics crossing a configurable usage threshold across phases |
| Paradox Catalog | `ParadoxCatalog` | Captures paradox entries with severity, resolution strategies, and version provenance |
| Audit Log | `AuditLog` | Records every orchestration decision with phase, action, version, and source |
| Browser Protocol | `BrowserOrchestrationProtocol` | Maintains per-platform tabs, context snapshots, and transition history |
| Role Ledger | `RoleResponsibilityLedger` | Reconciles agent roles, overlaps, escalation paths, and context-shift impacts |
| Plan-of-Work Matrix | `PlanOfWorkMatrix` | Phase-level responsibility assignments with handoffs, paradox checks, and escalation paths |
| Testing Strategy | `TestingStrategy` | Links planned test scenarios to executed results for each phase |
| Framework Container | `MetaOrchestrationFramework` | Aggregates all subsystems and exposes reporting helpers |

### Quick Start

```python
from src import (
    ResearchAgent, MetaOrchestrationFramework, MetaPromptTracker,
    EmergentTacticDetector, ParadoxCatalog, AuditLog,
    BrowserOrchestrationProtocol, StrategicArchitecture, StrategicComponent,
    TestingStrategy, RoleResponsibilityLedger, PlanOfWorkMatrix,
)

agent = ResearchAgent(
    name="research_orchestrator",
    phases=("Phase 1", "Phase 2", "Phase 3", "Phase 4"),
    meta_prompt_tracker=MetaPromptTracker(),
    tactic_detector=EmergentTacticDetector(threshold=2),
    paradox_catalog=ParadoxCatalog(),
    audit_log=AuditLog(),
    browser_protocol=BrowserOrchestrationProtocol(),
    architecture=StrategicArchitecture(),
    testing_strategy=TestingStrategy(),
    responsibility_ledger=RoleResponsibilityLedger(),
    plan_of_work=PlanOfWorkMatrix(),
)

record = agent.execute_phase(
    "Phase 1",
    version="v1",
    meta_prompt="Self-evaluate and refine",
    rationale="Bootstrap orchestration",
    paradox_observation="Recursive dependency identified",
    browser_events=[("ChatGPT", "synthesize", "Compiled debate summary")],
)

framework = MetaOrchestrationFramework(agent=agent)
print(framework.actionable_roadmap())
```

### Browser Transition Fix

`BrowserOrchestrationProtocol.log_event` correctly records **both** the implicit `open` action and the intended action when a tab is created for a new platform. This ensures the browser timeline stays consistent with the audit log:

```python
protocol = BrowserOrchestrationProtocol()
transition = protocol.log_event(
    platform="ChatGPT",
    action="synthesize",
    context_snapshot="First interaction",
)
# timeline: [BrowserTransition(action="open"), BrowserTransition(action="synthesize")]
assert transition.action == "synthesize"
```

---

## Agent Roles

The framework codifies eleven agent personas used across experiment phases:

| Role | Perspective | Key Responsibility |
| --- | --- | --- |
| Orchestrator | Systems synthesis overseer | Sequences phases and mediates debate protocol |
| Mediator | Alignment negotiator | Captures disagreements and translates agent biases |
| Audit Critic | Quality gatekeeper | Validates evidence and ensures paradox documentation |
| Workflow Synthesizer | Systems architect | Integrates multi-agent outputs and aligns plan-of-work entries |
| Prompt Librarian | Knowledge steward | Maintains prompts, templates, and meta-prompt lineage |
| Context Extractor | Situational analyst | Mines conversation history and updates context snapshots |
| Shell Exec | Execution gate | Runs tests and scaffolds scripts with guardrails |
| Slack Webhook | Transparency pulse | Sends READY/delegation/failure notifications |
| ChatGPT | Exploration-first agent | Generates orchestration hypotheses and paradox scenarios |
| Claude | Risk-framing agent | Stress-tests strategies and surfaces governance gaps |
| Gemini | Systems optimization agent | Optimizes sequencing and highlights automation opportunities |

---

## Experiment Phases

| Phase | Focus | Paradox Anticipation |
| --- | --- | --- |
| Phase 1 – Bootstrap Paradox | Draft initial meta-prompt and specify observation metrics | Self-reference loops where instruction evaluation triggers rewrites |
| Phase 2 – Multi-Agent Coordination | Define agent personas and run debate protocol | Divergent priors converging on conflicting orchestration metrics |
| Phase 3 – Browser-Based Orchestration | Map tab states and capture context-shift impact records | Simultaneous context threads causing state fragmentation |
| Phase 4 – Recursive Improvement | Design evaluation rubric and plan redesign loop | Recursive redesign destabilizing baseline assumptions |

---

## Documentation

| File | Description |
| --- | --- |
| [`meta_orchestration_framework.md`](meta_orchestration_framework.md) | Comprehensive unified framework reference including role table, plan-of-work matrix, paradox catalog, and audit trail expectations |
| [`meta_orchestration_plan.md`](meta_orchestration_plan.md) | Experiment planning dossier with phase-by-phase objectives, counter-intuitive discovery targets, and audit commitments |
| [`csos_case_study.md`](csos_case_study.md) | System engineering case study: Ontological Stabilization of the Cognitive Sovereignty Operating System (CSOS) — covers the four foundational axioms, audit remediation ledger, identity anchoring, Concept Ingestion Protocol, and Hydra multi-agent framework |
| [`notion_meta_perspectives.md`](notion_meta_perspectives.md) | Notion-ready perspective matrix for the four orchestration components, with prompts for Notion AI integration |
| [`task_catalog.md`](task_catalog.md) | Thematic catalog of orchestration initiatives, knowledge extraction workstreams, and open coordination questions |

---

## Running Tests

```bash
pytest -v
```

The root-level `test_*.py` modules cover the meta-orchestration framework end-to-end, including the `BrowserOrchestrationProtocol.log_event` behavior, role responsibility unification, and the research summarizer.

---

Need help? Use **Copy page** to share the instructions or **Share feedback** to tell us how the Cursor CLI can improve.
