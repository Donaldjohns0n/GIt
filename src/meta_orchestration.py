"""Unified recursive meta-orchestration framework implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Dict,
    Iterable,
    List,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
)


# ---------------------------------------------------------------------------
# Meta-prompt evolution tracking
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MetaPromptVersion:
    """Represents one iteration of the guiding meta-prompt."""

    version: str
    prompt: str
    rationale: str
    paradox_observation: str
    counter_intuitive_discovery: Optional[str] = None


@dataclass
class MetaPromptTracker:
    """Maintains a provenance-aware ledger of meta-prompt updates."""

    _versions: Dict[str, MetaPromptVersion] = field(default_factory=dict)
    _chronology: List[str] = field(default_factory=list)

    def register_version(
        self,
        *,
        version: str,
        prompt: str,
        rationale: str,
        paradox_observation: str,
        counter_intuitive_discovery: Optional[str] = None,
    ) -> MetaPromptVersion:
        """Record a new meta-prompt iteration with unique chronology."""

        if version in self._versions:
            raise ValueError(
                f"Meta-prompt version '{version}' already registered"
            )

        record = MetaPromptVersion(
            version=version,
            prompt=prompt,
            rationale=rationale,
            paradox_observation=paradox_observation,
            counter_intuitive_discovery=counter_intuitive_discovery,
        )
        self._versions[version] = record
        self._chronology.append(version)
        return record

    def latest(self) -> Optional[MetaPromptVersion]:
        """Return the most recent meta-prompt iteration."""

        if not self._chronology:
            return None
        return self._versions[self._chronology[-1]]

    def evolution_log(self) -> List[MetaPromptVersion]:
        """Return all meta-prompt iterations in chronological order."""

        return [self._versions[version] for version in self._chronology]


# ---------------------------------------------------------------------------
# Emergent tactic detection
# ---------------------------------------------------------------------------


@dataclass
class EmergentTacticDetector:
    """Flags tactics that emerge through repeated use across phases."""

    threshold: int = 2
    _occurrences: Dict[str, int] = field(default_factory=dict)
    _emergent: Dict[str, List[str]] = field(default_factory=dict)

    def record(self, *, phase: str, tactic: str) -> bool:
        """Register a tactic occurrence and flag if it becomes emergent."""

        if not tactic:
            return False

        count = self._occurrences.get(tactic, 0) + 1
        self._occurrences[tactic] = count

        if count >= self.threshold and tactic not in self._emergent:
            self._emergent[tactic] = [phase]
            return True

        if tactic in self._emergent:
            phases = self._emergent[tactic]
            if phase not in phases:
                phases.append(phase)
        return False

    def emergent_tactics(self) -> Dict[str, List[str]]:
        """Return emergent tactics with the phases that revealed them."""

        return {
            key: list(phases)
            for key, phases in self._emergent.items()
        }


# ---------------------------------------------------------------------------
# Paradox catalog with version provenance
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParadoxEntry:
    """Catalog entry linking paradox insights to their originating version."""

    name: str
    description: str
    severity: str
    version: str
    resolution_strategy: Optional[str] = None


@dataclass
class ParadoxCatalog:
    """Tracks paradox observations and cross-version implications."""

    _entries: List[ParadoxEntry] = field(default_factory=list)

    def register(self, entry: ParadoxEntry) -> None:
        self._entries.append(entry)

    def by_version(self, version: str) -> List[ParadoxEntry]:
        return [entry for entry in self._entries if entry.version == version]

    def all_entries(self) -> List[ParadoxEntry]:
        return list(self._entries)


# ---------------------------------------------------------------------------
# Audit log with provenance information
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AuditEntry:
    """Structured audit trail record."""

    phase: str
    action: str
    version: str
    source: Optional[str]
    notes: str


@dataclass
class AuditLog:
    """Maintains traceable records of key orchestration actions."""

    _entries: List[AuditEntry] = field(default_factory=list)

    def record(
        self,
        *,
        phase: str,
        action: str,
        version: str,
        source: Optional[str],
        notes: str,
    ) -> AuditEntry:
        entry = AuditEntry(
            phase=phase,
            action=action,
            version=version,
            source=source,
            notes=notes,
        )
        self._entries.append(entry)
        return entry

    def history(self) -> List[AuditEntry]:
        return list(self._entries)

    def by_phase(self, phase: str) -> List[AuditEntry]:
        return [entry for entry in self._entries if entry.phase == phase]


# ---------------------------------------------------------------------------
# Browser orchestration protocol
# ---------------------------------------------------------------------------


@dataclass
class BrowserTabState:
    """Describes a browser tab assigned to a specific platform."""

    tab_id: str
    platform: str
    context_summary: str


@dataclass(frozen=True)
class BrowserTransition:
    """Describes a context switch within the browser orchestration protocol."""

    tab_id: str
    platform: str
    action: str
    context_snapshot: str


@dataclass
class BrowserOrchestrationProtocol:
    """Coordinates multi-platform workspaces with state preservation."""

    _tabs: Dict[str, BrowserTabState] = field(default_factory=dict)
    _platform_index: Dict[str, str] = field(default_factory=dict)
    _history: List[BrowserTransition] = field(default_factory=list)
    _next_id: int = 1

    def _generate_tab_id(self) -> str:
        tab_id = f"tab-{self._next_id}"
        self._next_id += 1
        return tab_id

    def open_tab(
        self,
        *,
        platform: str,
        context_summary: str,
    ) -> BrowserTabState:
        tab_id = self._generate_tab_id()
        state = BrowserTabState(
            tab_id=tab_id,
            platform=platform,
            context_summary=context_summary,
        )
        self._tabs[tab_id] = state
        self._platform_index[platform] = tab_id
        self._history.append(
            BrowserTransition(
                tab_id=tab_id,
                platform=platform,
                action="open",
                context_snapshot=context_summary,
            )
        )
        return state

    def log_event(
        self,
        *,
        platform: str,
        action: str,
        context_snapshot: str,
    ) -> BrowserTransition:
        tab_id = self._platform_index.get(platform)
        if tab_id is None:
            state = self.open_tab(
                platform=platform,
                context_summary=context_snapshot,
            )

            # open_tab already logged the transition; return that entry
            return self._history[-1]

        state = self._tabs[tab_id]
        state.context_summary = context_snapshot
        transition = BrowserTransition(
            tab_id=tab_id,
            platform=platform,
            action=action,
            context_snapshot=context_snapshot,
        )
        self._history.append(transition)
        return transition

    def timeline(self) -> List[BrowserTransition]:
        return list(self._history)

    def context_matrix(self) -> Dict[str, str]:
        return {
            state.platform: state.context_summary
            for state in self._tabs.values()
        }


# ---------------------------------------------------------------------------
# Role & responsibility governance
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RoleDefinition:
    """Fully specified role with nuanced orchestration duties."""

    role: str
    perspective: str
    responsibilities: Tuple[str, ...]
    inputs: Tuple[str, ...]
    outputs: Tuple[str, ...]
    dependencies: Tuple[str, ...]
    context_boundaries: Tuple[str, ...]
    negotiation_protocols: Tuple[str, ...]
    escalation_paths: Tuple[str, ...]
    origin_versions: Tuple[str, ...]


@dataclass(frozen=True)
class RoleOverlap:
    """Capture overlaps and the reconciliation protocols between roles."""

    roles: Tuple[str, ...]
    nuance: str
    resolution_protocol: str
    triggers: Tuple[str, ...]
    origin_versions: Tuple[str, ...]


@dataclass(frozen=True)
class ContextShiftRecord:
    """Describe platform shifts, impacted roles, and mitigation protocols."""

    platform: str
    description: str
    ambiguity: str
    resolution_protocol: str
    affected_roles: Tuple[str, ...]
    origin_phase: str
    origin_version: str


@dataclass
class RoleResponsibilityLedger:
    """Reconcile role definitions, overlaps, and context-driven adjustments."""

    _roles: Dict[str, RoleDefinition] = field(default_factory=dict)
    _overlaps: List[RoleOverlap] = field(default_factory=list)
    _context_shifts: List[ContextShiftRecord] = field(default_factory=list)

    def register_role(self, definition: RoleDefinition) -> RoleDefinition:
        self._roles[definition.role] = definition
        return definition

    def role(self, role: str) -> RoleDefinition:
        return self._roles[role]

    def roles(self) -> List[RoleDefinition]:
        return list(self._roles.values())

    def register_overlap(self, overlap: RoleOverlap) -> RoleOverlap:
        self._overlaps.append(overlap)
        return overlap

    def overlaps(self) -> List[RoleOverlap]:
        return list(self._overlaps)

    def record_context_shift(
        self, context_shift: ContextShiftRecord
    ) -> ContextShiftRecord:
        self._context_shifts.append(context_shift)
        return context_shift

    def context_shifts(self) -> List[ContextShiftRecord]:
        return list(self._context_shifts)


# ---------------------------------------------------------------------------
# Strategic architecture, plan of work & testing strategy
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StrategicComponent:
    """Defines one architectural component used by the orchestration agent."""

    name: str
    responsibilities: Sequence[str]
    dependencies: Sequence[str] = ()
    outputs: Sequence[str] = ()


@dataclass
class StrategicArchitecture:
    """Maintains a registry of orchestration components and dependencies."""

    _components: Dict[str, StrategicComponent] = field(default_factory=dict)

    def add_component(self, component: StrategicComponent) -> None:
        if component.name in self._components:
            raise ValueError(
                f"Component '{component.name}' already registered"
            )
        self._components[component.name] = component

    def component(self, name: str) -> StrategicComponent:
        return self._components[name]

    def components(self) -> List[StrategicComponent]:
        return list(self._components.values())


@dataclass(frozen=True)
class PlanOfWorkEntry:
    """Defines responsibilities per phase and context."""

    phase: str
    context: str
    responsible_roles: Tuple[str, ...]
    tasks: Tuple[str, ...]
    data_inputs: Tuple[str, ...]
    outputs: Tuple[str, ...]
    handoffs: Tuple[str, ...]
    paradox_checks: Tuple[str, ...]
    escalation_paths: Tuple[str, ...]
    joint_actions: Tuple[str, ...]


@dataclass
class PlanOfWorkMatrix:
    """Maintains a consolidated plan of work across phases and contexts."""

    _entries: List[PlanOfWorkEntry] = field(default_factory=list)

    def add_entry(self, entry: PlanOfWorkEntry) -> PlanOfWorkEntry:
        self._entries.append(entry)
        return entry

    def entries(self) -> List[PlanOfWorkEntry]:
        return list(self._entries)

    def as_table(self) -> List[Dict[str, Sequence[str]]]:
        table: List[Dict[str, Sequence[str]]] = []
        for entry in self._entries:
            table.append(
                {
                    "phase": entry.phase,
                    "context": entry.context,
                    "responsible_roles": list(entry.responsible_roles),
                    "tasks": list(entry.tasks),
                    "data_inputs": list(entry.data_inputs),
                    "outputs": list(entry.outputs),
                    "handoffs": list(entry.handoffs),
                    "paradox_checks": list(entry.paradox_checks),
                    "escalation_paths": list(entry.escalation_paths),
                    "joint_actions": list(entry.joint_actions),
                }
            )
        return table


@dataclass(frozen=True)
class TestScenario:
    """Represents a planned test that validates orchestration outcomes."""

    name: str
    objective: str
    command: str
    coverage: Sequence[str] = ()
    __test__ = False  # Avoid pytest collection.


@dataclass
class TestingStrategy:
    """Connects planned validation routines with executed results."""

    _plans: Dict[str, List[TestScenario]] = field(default_factory=dict)
    _executions: Dict[str, Dict[str, str]] = field(default_factory=dict)
    __test__ = False

    def plan_phase_tests(
        self,
        phase: str,
        scenarios: Iterable[TestScenario],
    ) -> None:
        plans = self._plans.setdefault(phase, [])
        plans.extend(scenarios)

    def planned_tests(self, phase: str) -> List[TestScenario]:
        return list(self._plans.get(phase, []))

    def record_execution(
        self,
        phase: str,
        results: MutableMapping[str, str],
    ) -> None:
        self._executions[phase] = dict(results)

    def execution_results(self, phase: str) -> Dict[str, str]:
        return dict(self._executions.get(phase, {}))


# ---------------------------------------------------------------------------
# Research agent implementation
# ---------------------------------------------------------------------------


@dataclass
class PhaseRecord:
    """Historical record of a phase execution."""

    phase: str
    version: str
    outputs: Dict[str, str]
    paradoxes: List[ParadoxEntry]
    counter_intuitive_discoveries: List[str]
    emergent_tactics: List[str]
    audit_entries: List[AuditEntry]
    tests_executed: Dict[str, str]


@dataclass
class ResearchAgent:
    """Coordinates the end-to-end recursive meta-orchestration workflow."""

    name: str
    phases: Sequence[str]
    meta_prompt_tracker: MetaPromptTracker
    tactic_detector: EmergentTacticDetector
    paradox_catalog: ParadoxCatalog
    audit_log: AuditLog
    browser_protocol: BrowserOrchestrationProtocol
    architecture: StrategicArchitecture
    testing_strategy: TestingStrategy
    responsibility_ledger: RoleResponsibilityLedger
    plan_of_work: PlanOfWorkMatrix
    history: List[PhaseRecord] = field(default_factory=list)

    def register_role_definition(
        self,
        *,
        phase: str,
        version: str,
        role: str,
        perspective: str,
        responsibilities: Sequence[str],
        inputs: Sequence[str],
        outputs: Sequence[str],
        dependencies: Sequence[str],
        context_boundaries: Sequence[str],
        negotiation_protocols: Sequence[str],
        escalation_paths: Sequence[str],
        origin_versions: Optional[Sequence[str]] = None,
    ) -> RoleDefinition:
        """Register or update a role definition with full nuance."""

        definition = RoleDefinition(
            role=role,
            perspective=perspective,
            responsibilities=tuple(responsibilities),
            inputs=tuple(inputs),
            outputs=tuple(outputs),
            dependencies=tuple(dependencies),
            context_boundaries=tuple(context_boundaries),
            negotiation_protocols=tuple(negotiation_protocols),
            escalation_paths=tuple(escalation_paths),
            origin_versions=tuple(origin_versions or (version,)),
        )
        self.responsibility_ledger.register_role(definition)
        self.audit_log.record(
            phase=phase,
            action="role-definition",
            version=version,
            source=role,
            notes="Responsibilities reconciled across orchestration contexts.",
        )
        return definition

    def register_role_overlap(
        self,
        *,
        phase: str,
        version: str,
        roles: Sequence[str],
        nuance: str,
        resolution_protocol: str,
        triggers: Sequence[str],
        origin_versions: Optional[Sequence[str]] = None,
    ) -> RoleOverlap:
        """Document overlaps and how they are resolved."""

        overlap = RoleOverlap(
            roles=tuple(roles),
            nuance=nuance,
            resolution_protocol=resolution_protocol,
            triggers=tuple(triggers),
            origin_versions=tuple(origin_versions or (version,)),
        )
        self.responsibility_ledger.register_overlap(overlap)
        self.audit_log.record(
            phase=phase,
            action="role-overlap",
            version=version,
            source=",".join(roles),
            notes=resolution_protocol,
        )
        return overlap

    def register_context_shift(
        self,
        *,
        phase: str,
        version: str,
        platform: str,
        description: str,
        ambiguity: str,
        resolution_protocol: str,
        affected_roles: Sequence[str],
    ) -> ContextShiftRecord:
        """Capture context switch impacts and mitigation protocols."""

        record = ContextShiftRecord(
            platform=platform,
            description=description,
            ambiguity=ambiguity,
            resolution_protocol=resolution_protocol,
            affected_roles=tuple(affected_roles),
            origin_phase=phase,
            origin_version=version,
        )
        self.responsibility_ledger.record_context_shift(record)
        self.audit_log.record(
            phase=phase,
            action="context-shift",
            version=version,
            source=platform,
            notes=resolution_protocol,
        )
        return record

    def add_plan_of_work_entry(
        self,
        *,
        phase: str,
        version: str,
        context: str,
        responsible_roles: Sequence[str],
        tasks: Sequence[str],
        data_inputs: Sequence[str],
        outputs: Sequence[str],
        handoffs: Sequence[str],
        paradox_checks: Sequence[str],
        escalation_paths: Sequence[str],
        joint_actions: Sequence[str],
    ) -> PlanOfWorkEntry:
        """Create a plan-of-work entry for the given context."""

        entry = PlanOfWorkEntry(
            phase=phase,
            context=context,
            responsible_roles=tuple(responsible_roles),
            tasks=tuple(tasks),
            data_inputs=tuple(data_inputs),
            outputs=tuple(outputs),
            handoffs=tuple(handoffs),
            paradox_checks=tuple(paradox_checks),
            escalation_paths=tuple(escalation_paths),
            joint_actions=tuple(joint_actions),
        )
        self.plan_of_work.add_entry(entry)
        context_note = f"Context: {context}"
        self.audit_log.record(
            phase=phase,
            action="plan-of-work",
            version=version,
            source=",".join(responsible_roles),
            notes=context_note,
        )
        return entry

    def execute_phase(
        self,
        phase: str,
        *,
        version: str,
        meta_prompt: str,
        rationale: str,
        paradox_observation: str,
        counter_intuitive_discovery: Optional[str] = None,
        outputs: Optional[Dict[str, str]] = None,
        paradox_entries: Optional[Iterable[ParadoxEntry]] = None,
        tactics: Optional[Iterable[str]] = None,
        audit_notes: Optional[Sequence[str]] = None,
        browser_events: Optional[Sequence[Tuple[str, str, str]]] = None,
        test_results: Optional[MutableMapping[str, str]] = None,
    ) -> PhaseRecord:
        """Execute a phase and update all governance records."""

        if phase not in self.phases:
            raise ValueError(
                f"Unknown phase '{phase}' for agent '{self.name}'"
            )

        # Register the meta-prompt version if new.
        try:
            self.meta_prompt_tracker.register_version(
                version=version,
                prompt=meta_prompt,
                rationale=rationale,
                paradox_observation=paradox_observation,
                counter_intuitive_discovery=counter_intuitive_discovery,
            )
        except ValueError:
            # Version already registered – acceptable for iterative execution.
            pass

        record_audit_entries: List[AuditEntry] = []
        latest_prompt = self.meta_prompt_tracker.latest()
        for note in audit_notes or ("Phase execution initiated",):
            record_audit_entries.append(
                self.audit_log.record(
                    phase=phase,
                    action="phase-update",
                    version=version,
                    source=(
                        latest_prompt.version if latest_prompt else None
                    ),
                    notes=note,
                )
            )

        emergent_tactics: List[str] = []
        for tactic in tactics or ():
            if self.tactic_detector.record(phase=phase, tactic=tactic):
                emergent_tactics.append(tactic)

        registered_paradoxes: List[ParadoxEntry] = []
        for paradox in paradox_entries or ():
            self.paradox_catalog.register(paradox)
            registered_paradoxes.append(paradox)

        executed_tests: Dict[str, str] = {}
        if test_results:
            executed_tests.update(test_results)
            self.testing_strategy.record_execution(phase, test_results)

        for platform, action, context_snapshot in browser_events or ():
            transition = self.browser_protocol.log_event(
                platform=platform,
                action=action,
                context_snapshot=context_snapshot,
            )
            record_audit_entries.append(
                self.audit_log.record(
                    phase=phase,
                    action=f"browser:{action}",
                    version=version,
                    source=transition.platform,
                    notes=context_snapshot,
                )
            )

        phase_record = PhaseRecord(
            phase=phase,
            version=version,
            outputs=dict(outputs or {}),
            paradoxes=registered_paradoxes,
            counter_intuitive_discoveries=[
                discovery
                for discovery in (counter_intuitive_discovery,) if discovery
            ],
            emergent_tactics=emergent_tactics,
            audit_entries=record_audit_entries,
            tests_executed=executed_tests,
        )
        self.history.append(phase_record)
        return phase_record


# ---------------------------------------------------------------------------
# Framework container
# ---------------------------------------------------------------------------


@dataclass
class MetaOrchestrationFramework:
    """Aggregates all orchestration subsystems and reporting helpers."""

    agent: ResearchAgent

    def audit_trail(self) -> List[AuditEntry]:
        return self.agent.audit_log.history()

    def paradox_catalog(self) -> List[ParadoxEntry]:
        return self.agent.paradox_catalog.all_entries()

    def meta_prompt_log(self) -> List[MetaPromptVersion]:
        return self.agent.meta_prompt_tracker.evolution_log()

    def role_definitions(self) -> List[RoleDefinition]:
        return self.agent.responsibility_ledger.roles()

    def plan_of_work_matrix(self) -> List[PlanOfWorkEntry]:
        return self.agent.plan_of_work.entries()

    def actionable_roadmap(self) -> List[str]:
        """Generate actionable next steps derived from recorded history."""

        roadmap: List[str] = []
        for record in self.agent.history:
            for paradox in record.paradoxes:
                roadmap.append(
                    (
                        f"Resolve paradox '{paradox.name}' "
                        f"(severity: {paradox.severity}) "
                        f"in version {paradox.version}."
                    )
                )
            for discovery in record.counter_intuitive_discoveries:
                roadmap.append(
                    (
                        "Operationalize counter-intuitive discovery: "
                        f"{discovery} (phase {record.phase})."
                    )
                )
            for tactic in record.emergent_tactics:
                roadmap.append(
                    (
                        f"Codify emergent tactic '{tactic}' into "
                        "standard operating procedures."
                    )
                )
        if not roadmap:
            roadmap.append(
                "Review latest meta-prompt iteration "
                "for potential enhancements."
            )
        return roadmap

    def documentation_summary(self) -> Dict[str, Sequence[str]]:
        """Summarize documentation evidence across subsystems."""

        executed_items = self.agent.testing_strategy._executions.items()
        return {
            "phases": [record.phase for record in self.agent.history],
            "components": [
                component.name
                for component in self.agent.architecture.components()
            ],
            "roles": [
                f"{role.role} ({role.perspective})"
                for role in self.agent.responsibility_ledger.roles()
            ],
            "tests": [
                f"{phase}:{name}"
                for phase, results in executed_items
                for name in results
            ],
            "plan_of_work": [
                f"{entry.phase}:{entry.context}"
                for entry in self.agent.plan_of_work.entries()
            ],
        }
