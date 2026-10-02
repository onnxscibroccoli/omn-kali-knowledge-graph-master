# Universal goals contract

The JSON schema documents structure; `scripts/goals_registry.py` validates references,
cycles, status and proof semantics. New goals must include all fields shown in
`goals/universal.json`: stable ID, request key/source, owner repository ID, affected
repositories, target architecture, dependencies, named acceptance criteria, evidence
and implementation references, status, blockers, next action and revision.

Repository identity uses stable GitHub IDs. Current bindings record exact source SHA
and transport contract hash. Initial metadata entries use SHA256 of
`no-execution-transport:goals-registry-v1`; this explicitly proves no executor identity.
A real executor capability must replace that binding with its validated contract.

Evidence result vocabulary is PASS, FAIL, NOT_PROVEN, NOT_APPLICABLE, SKIPPED.
Scope is UNIT, INTEGRATION, LIVE or RECONSTRUCTION. Evidence requires timestamp,
scenario, environment identity, criterion and repository ID, exact code/transport
binding and artifact reference/hash. `provenanceVerified=true` is a trust assertion
for a future independently authenticated artifact verifier, not a verification
performed by this registry. Do not set it from a README, issue or green badge.
Only trusted, reviewed writers may assert it. Automated evidence ingestion remains
planned. The initial registry contains no evidence asserting verified provenance.

A changed binding invalidates current proof while retaining historical evidence.
A later failing or ambiguous result prevents promotion. Historical public architecture
goals are migrated conservatively; old files remain unchanged.

Capture updates are locked, revision-checked and atomic. Audit entries share the
registry transaction. Public rendering excludes private-owned goal details and uses
opaque dependency placeholders. Keep private inventories outside this public repo.
