# Tickets: Repository Flattening (GIt)

Rule in force: **no directory may exist in this repository without a full
ticket in this file.** Rationale: [failure-doctrine.md](failure-doctrine.md)
("butcher, don't box"). Edges for every move: [manifest.json](manifest.json).
Operation recorded in the ecosystem execution ledger
(`ai-agents-data-logs/ledger.jsonl`, session `exec-20260902-212320-e4188d`).

## Kept directories

### T-KEEP-01 — `.git/`
Version-control substrate holding the history graph, including the
pre-flattening hierarchy and the `git log --follow` trail across every move.
Removing it deletes relations, not a label. KEPT.

### T-KEEP-02 — `__pycache__/`, `.pytest_cache/` (ephemeral)
Interpreter/pytest caches; gitignored, self-recreating. Tolerated when they
appear; never committed.

## Removed directories

### T-01 — `docs/` (5 files)
- **Connected:** five markdown documents to the label "documentation."
- **Contents →** csos_case_study.md, meta_orchestration_framework.md,
  meta_orchestration_plan.md, notion_meta_perspectives.md, task_catalog.md
  at root.
- **Why no box:** nothing executable referenced the folder; README's document
  index carries the relation (what each doc covers), which a folder cannot.

### T-02 — `src/` (3 files)
- **Connected:** the Python package name `src` to the import statements in
  the tests — the one place in this repo where a directory carried real
  meaning (the dotted import path).
- **Contents →** meta_orchestration.py and summarizer.py at root;
  `src/__init__.py` DELETED (a root `__init__.py` breaks pytest collection
  and its relative imports cannot survive flat).
- **Decision recorded:** the `__init__` re-export surface (`__all__`, 25
  names) is gone. Its only consumers were this repo's tests, now importing
  the modules directly. The surface is recoverable verbatim from git history
  (last present at the pure-move commit).
- **Why no box:** the package existed to aggregate two modules for two test
  files; direct module imports carry the same relation without the tree.

### T-03 — `tests/` (2 files)
- **Connected:** test modules to the label "tests" — carried equally by the
  `test_` filename prefix, which is what pytest discovery actually uses.
- **Contents →** test_meta_orchestration.py, test_summarizer.py at root.
  `conftest.py` was already at root; its sys.path insert still applies.

## Standing rule

Adding a directory requires a keep-ticket here in the same commit, stating
what it connects that file content and manifest edges cannot.
