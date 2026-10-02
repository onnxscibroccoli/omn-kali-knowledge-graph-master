# Implementation ledger — universal-goals-implementation-plan.md

Baseline: fd5cca1d4fed96cd552e08711885e5c9617c3fde; existing schema check passed.
Isolation: fresh clone on feat/universal-goals-registry, no user's worktree modified.
Preflight: validation feeds evaluation; both feed atomic capture and public renderer.
Ruling: Tasks 1 and 2 share one test module and were verified together (19 tests RED import failure -> GREEN); separate proof criteria remain explicit.
Ruling: evidence requires provenanceVerified=true; supplied URLs/hashes alone cannot establish independent artifact verification. A future ingestion verifier owns that assertion.
Ruling: native branch review will use a fresh reviewer as required by executing-plans; no implementation subagents.
Tasks 1/2: validation and evidence evaluator implemented, 19 tests pass; seed/schema pending before completion.
Task 3: request tests RED missing interface -> GREEN; five tests pass.
Tasks 1/2: complete. Public source SHA inventory and 23 conservative seed goals validate.
Task 3: complete. Request capture and CLI tests pass, including stale revisions and interrupted replacement.
Task 4: complete. Six public rendering tests pass; deterministic outputs regenerated and checked.
Task 5: CLI RED -> GREEN. All 36 tests and legacy schema check pass; GitHub Actions execution awaits publication.
Ruling: initial GH-BIST goal is IMPLEMENTED, not TEST_PROVEN, because independent artifact provenance has not been ingested; avoids promoting a historical green badge.
Ruling: default-branch metadata uses explicit no-execution transport hash; it cannot establish executor health. Private account inventory is excluded from public Git.
Final review: fresh reviewer confirmed six important findings; each reproduced before fixes.
Final: fixed malformed enum/ID types, unmet dependency promotion, mutable artifact references,
public reference redaction, unaudited persistence, migration ownership/blockers.
Review regression tests RED -> GREEN; later lower-scope failure also blocks old proof.
Ruling: bounded save API supports goal additions only; metadata/evidence edits require a future separately audited writer. Wrong decision cost: callers needing updates must wait for that writer.
Ruling: public views redact URLs and absolute paths from free text. Wrong decision cost: useful public links must be read from canonical reviewed metadata instead of rendered prose.
Ruling: migration ownership is mapped from existing execution lanes; affected repositories preserve public implementation roles. Private executor association stays in the private inventory. Wrong decision cost: owner corrections require a reviewed registry migration.
