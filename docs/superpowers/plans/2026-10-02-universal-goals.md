# Universal Goals Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Native execution is recommended; no subagents are required for this unit.

**Goal:** Deliver one validated cross-repository goals registry with reproducible evidence-aware graphs and request capture.

**Architecture:** Extend omn-kali-knowledge-graph-master, the existing coordination owner. Keep canonical goals separate from derived diagrams, inventory observations and private evidence. Link Grasshopper browser-provider independence as planned work without claiming implementation.

**Tech Stack:** Python 3.12, standard-library JSON/unittest/hashlib, existing PyYAML for migration, GitHub Actions. No new runtime dependency.

**Spec:** [browser and goals specification](../specs/2026-10-02-browser-and-goals.md), approved by the user's instruction to continue on 2026-10-02.

## Global Constraints

- Status vocabulary: PLANNED, IN_PROGRESS, BLOCKED, IMPLEMENTED, TEST_PROVEN, LIVE_PROVEN, REGRESSED, RETIRED.
- Evidence scope is separately UNIT, INTEGRATION, LIVE or RECONSTRUCTION.
- Skipped jobs and missing artifacts are NOT_PROVEN.
- Events describe facts; observing an event does not replay its command or notification.
- Private repository metadata stays in a private inventory; only sanitized public projections enter the public graph repository.
- No protected Helix infrastructure changes, automatic merges or historical-script replay.
- Native implementation begins after this written plan is reviewed. This plan covers registry foundation only; browser runtime and authenticated discovery expansion require subsequent linked implementation plans.

## Review Focus

- A renamed repository keeps its stable GitHub ID and goal ownership: Task 1 tests.
- A green workflow containing skipped required jobs cannot promote a goal: Task 2 tests.
- A relevant code/transport change invalidates current evidence but preserves historical proof: Task 2 tests.
- Concurrent request capture rejects a stale revision without losing a goal: Task 3 tests.
- Public rendering does not expose private repository names, paths or private evidence links: Task 4 tests.

## Task 1: Canonical registry and structural validation

**Files:** Create `goals/universal.json`, `schemas/universal-goals-v1.schema.json`, `scripts/goals_registry.py`, `tests/test_goals_registry.py`. Read existing `goals/production-backlog.yml`, `goals/system-execution-plan-2026-10-01.yml`, `omnikali/*.yml` and current graph docs before seeding. Keep historical files unchanged.

**Interfaces:** `validate_registry(registry: dict) -> list[str]` returns sorted errors and no mutations. Root fields: schema=`omnikali.universal-goals/v1`, revision=nonnegative integer, repositories, goals, evidence. Repository fields: id=GitHub repository ID string, fullName, visibility=public|private, currentBindings={codeSha,transportContractHash}. Goal fields include stable id, title, requestKey, requestedAt, requestedBy, sourceRequestRef, ownerRepositoryId, affectedRepositories, capability, targetArchitecture, dependencies, acceptanceCriteria, implementationRefs, evidenceRefs, status, blockers, nextAction, revision and supersedes. Each criterion has id, description, requiredScope. Private repos use opaque IDs in public projections.

- [ ] Write tests named `test_duplicate_ids_rejected`, `test_dangling_owner_rejected`, `test_dependency_cycle_rejected`, `test_repository_rename_preserves_owner`, `test_unknown_status_rejected`, `test_empty_acceptance_cannot_claim_proven`. Assertions: each invalid fixture returns an error; valid renamed ownership returns `[]`.
- [ ] Run `python -m unittest discover -s tests -p 'test_goals_registry.py' -v`; confirm missing-module failure before implementation.
- [ ] Implement structural validation with deterministic DFS cycle detection and strict required types/enums. Add a JSON schema documenting the same contract; runtime validation remains standard-library Python.
- [ ] Seed eight approved new goals from the companion design seed and map existing architecture goals to stable IDs with source references. Preserve current production/Broccoli blockers. Do not infer completion from closed issues or docs. Validate migration aliases and duplicate ownership manually against source.
- [ ] Rerun focused tests; commit the registry/schema/validator/tests as one bounded change.

## Task 2: Criterion-level evidence evaluation

**Files:** Extend `scripts/goals_registry.py` and `tests/test_goals_registry.py`.

**Interfaces:** `evaluate_goal(registry: dict, goal_id: str) -> dict` returns `{goalId,effectiveStatus,criteria,blockers}`. Evidence fields: id, repositoryId, codeSha, transportContractHash, criterionId, scope, timestamp, result=PASS|FAIL|NOT_PROVEN|NOT_APPLICABLE|SKIPPED, scenario, environmentId, artifactRef, artifactSha256, workflowUrl/runId/jobId when applicable, invalidatedAt. Check supplied artifact-hash format and immutable source references; this evaluator does not pretend to fetch or independently verify external artifacts. Stored evidence is an assertion until its ingestion verifier establishes provenance.

- [ ] Add tests `test_skipped_job_not_proof`, `test_missing_artifact_not_proof`, `test_stale_code_not_proof`, `test_changed_transport_not_proof`, `test_unit_scope_cannot_prove_live`, `test_regression_preserves_history`, `test_later_failure_blocks_prior_pass`, `test_foreign_criterion_rejected`.
- [ ] Run focused unittest; confirm assertions fail for unimplemented evaluation.
- [ ] Evaluate each required criterion independently. Require matching owner/current code/transport bindings, suitable scope, PASS and named artifact reference/hash. Conflicting or later failing evidence blocks promotion. Relevant invalidation with prior proof yields REGRESSED; insufficient proof retains IMPLEMENTED or earlier declared status. Never mutate or erase evidence.
- [ ] Reject stored TEST_PROVEN/LIVE_PROVEN claims exceeding evaluated scope; report explicit NOT_PROVEN criterion results. Only an independently verified artifact-ingestion path can promote future imported evidence.
- [ ] Rerun focused tests; commit.

## Task 3: Idempotent request capture and safe persistence

**Files:** Create `scripts/goals.py`, extend `scripts/goals_registry.py`, create `tests/test_goal_requests.py`.

**Interfaces:** `add_goal(registry: dict, goal: dict, expected_revision: int) -> dict` returns a new registry, leaves input unchanged, and returns unchanged content for an identical requestKey/payload; conflicting reuse raises ValueError. `save_registry(path: Path, registry: dict, expected_revision: int) -> None` uses a file lock, reads current revision under lock, validates, writes/fsyncs a same-directory temporary file, atomically replaces and fsyncs the directory. No caller-selected shell commands.

- [ ] Add tests `test_repeated_request_is_idempotent`, `test_conflicting_request_key_rejected`, `test_stale_revision_does_not_write`, `test_invalid_goal_never_replaces_file`, `test_interruption_keeps_valid_old_or_new_registry` using TemporaryDirectory.
- [ ] Run `python -m unittest discover -s tests -p 'test_goal_requests.py' -v`; confirm failing baseline.
- [ ] Implement the pure add operation and locked revision-checked save. Embed append-only audit entries in the same atomic registry document so goal/audit cannot diverge; derived standalone journals are exports, not a second authority.
- [ ] CLI: `python scripts/goals.py validate --registry PATH`, `add --registry PATH --request PATH --expected-revision N`, `status --registry PATH`. Default repository path resolves from script location; arbitrary cwd works. Invalid input exits 1 without sensitive payload echo.
- [ ] Rerun request/registry tests; commit.

## Task 4: Public graph and speech-ready views

**Files:** Create `scripts/render_goals.py`, `tests/test_goal_views.py`, `graph/universal-goals.mmd`, `docs/UNIVERSAL_GOALS.md`, `docs/UNIVERSAL_GOALS_NARRATIVE.txt`.

**Interfaces:** `public_projection(registry: dict) -> dict` excludes private names/paths/evidence URLs and represents private dependencies by opaque placeholder IDs. `render_goals(registry: dict) -> dict[str,str]` returns deterministic outputs keyed by the three generated paths. Rendering consumes validated registry and effective statuses, never reparses README claims.

- [ ] Test `test_private_metadata_redacted`, `test_transitive_private_dependency_redacted`, `test_mermaid_labels_escaped`, `test_render_deterministic`, `test_narrative_contains_owner_action_evidence_status`, `test_effective_status_matches_validator`.
- [ ] Run `python -m unittest discover -s tests -p 'test_goal_views.py' -v`; confirm missing renderer failure.
- [ ] Generate top-down Mermaid with dependency edges and short quoted labels. Generate table of owner/status/next action and speech sentences such as “Goal X depends on Goal Y. Repository Z owns Goal X. Live acceptance remains not proven.” Keep narrative alongside diagrams.
- [ ] Render only sanitized outputs in public Git/Actions. Add CLI `python scripts/render_goals.py --registry PATH --check`; --check compares outputs and exits 1 on drift without rewriting.
- [ ] Rerun view tests and regenerate outputs; commit.

## Task 5: Self-test integration, documentation and release evidence

**Files:** Create `.github/workflows/universal-goals.yml`; modify `README.md`, `docs/ci-cd.md`, `.omnikali/MASTER_GRAPH.md`. Inspect pointer documents immediately before editing; preserve dated historical evidence. Add `tests/test_goal_cli.py`.

- [ ] Add CLI integration tests for arbitrary cwd, malformed JSON, revision conflicts, missing files and generated-view drift; assert nonzero exits on invalid input and no traceback/private payload disclosure.
- [ ] Run `python -m unittest discover -s tests -v`; confirm new missing CLI cases fail before fixing.
- [ ] Add read-only Actions permissions, Python 3.12, unittest, registry validate, render --check and existing `python scripts/validate_schema.py`. Trigger on PR/push and manual dispatch. Workflow does not authorize deploy, auto-merge or private inventory uploads.
- [ ] Update README and master graph to point at one registry and generated views; document safe request capture and exact proof semantics. Record remaining goals: browser-provider implementation, private authenticated discovery, associated repositories and non-default branches.
- [ ] Run all tests, existing schema check, public projection scan, generated-output drift check and `git diff --check`. Capture exact branch/commit/test commands; do not claim Actions passed before observing exact-commit results.
- [ ] Commit; prepare a draft PR with evidence and open gates. Publication uses existing authorized GitHub connection and remains subject to its automatic review. No merge.

## Self-review and follow-on work

All five review-focus cases are assigned to tests. The registry is the single owner; audit entries share its atomic transaction. The already captured 29-repository inventory remains a private review artifact and is not bulk-committed to the public repository. Seed-goal reporting status is not treated as external artifact verification. Scope excludes browser-provider runtime implementation, new persistent services, authenticated provider login, org/collaborator enumeration and branch expansion; these remain explicit linked goals. Native execution is recommended because this unit has tightly coupled validation/evaluation/rendering interfaces and five bounded tasks.

## Review request

Review this first-unit plan and confirm native execution. Runtime code begins after plan review under the writing-plans workflow. Browser-provider runtime gets the next plan after this foundation's proof boundary is established.
