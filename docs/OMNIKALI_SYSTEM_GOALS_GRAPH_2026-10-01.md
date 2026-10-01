
# OmniKali System Goals Graph

**Goals tag:** OMNIKALI-SYSTEM-GOALS-2026-10-01
**Companion graph:** OMNIKALI-SYSTEM-KG-2026-10-01

## North star

An authorized agent can reproduce, operate, recover, and extend the OmniKali system from source with no undocumented operator steps, while the existing validated production desktop remains protected.

## Goal dependency graph

G0 Protect and observe
 -> G1 Canonical contracts
 -> G2 Production acceptance
 -> G3 Reproducible reconstruction
 -> G4 Machine-readable BIST
 -> G5 Bounded self-repair
 -> G6 Terminal independence
 -> G7 Second executor
 -> G8 Second substrate
 -> G9 Autonomous operations

In parallel from G1:
G10 Android agent executor
 -> G11 APK/UI automation loop
 -> G12 Verified Morphe source ecosystem
 -> G13 Source-build reproducibility

And from G0:
G14 Persistent development substrate

## Goals

### G0 Protect and observe
**Status:** PROVEN/ONGOING

Preserve CloudFront/nginx/Helix/QEMU production and the known-good Rish transport. Maintain dated evidence and restore points.

Exit evidence: no unapproved production listener changes, current health/acceptance evidence, protected restore point.

### G1 Canonical contracts
**Status:** IN_PROGRESS

Unify task lifecycle, executor boundary, desktop session contract, BIST schema, Android MCP contract, and Morphe source trust model.

Exit evidence: one machine-readable contract per boundary and no duplicate owner for the same capability.

### G2 Production acceptance
**Status:** OPEN

Freshly prove authenticated login -> ticketed WSS -> guest desktop and the eight resilience scenarios.

Exit evidence: named acceptance IDs, user-visible browser proof, all scenarios classified.

### G3 Reproducible reconstruction
**Status:** OPEN

Reproduce the platform from source on a clean host using secret references rather than copied credentials.

Exit evidence: clean-host dry-run, deterministic artifact acquisition, source SHA/config manifest, successful authorized deployment acceptance.

### G4 Machine-readable BIST
**Status:** OPEN

Make BIST emit strict PASS|FAIL|NOT_PROVEN|NOT_APPLICABLE JSON and make merge/release gates consume it.

Exit evidence: schema validation, fail-closed behavior, no text-only PASS ambiguity.

### G5 Bounded self-repair
**Status:** OPEN

Map known failure classes to bounded, reversible repair actions and verify recovery after each action.

Exit evidence: eight-scenario mapping, repair policy, recovery evidence, loop cap and human checkpoint.

### G6 Terminal independence
**Status:** PLANNED

Use one task contract from Android/Termux and a second non-browser terminal without changing domain semantics.

### G7 Second executor
**Status:** PLANNED

Add a second executor behind the same task lifecycle without changing PENDING -> RUNNING -> COMPLETED|FAILED.

### G8 Second substrate
**Status:** PLANNED

Prove an isolated Kubernetes or portable-cloud substrate without touching production 80/443.

### G9 Autonomous operations
**Status:** PLANNED

Introduce scoped sub-bots only after ownership collisions and contract boundaries are resolved.

### G10 Android agent executor
**Status:** IN_PROGRESS

Run the custom MCP beside Broccoli/Rish on Android.

Exit evidence: supervisor recovery, local MCP initialize, phone-local Rish action, durable evidence.

### G11 APK/UI automation loop
**Status:** IN_PROGRESS

Complete observe -> understand -> locate -> act -> reobserve -> verify on real installed APKs.

Exit evidence: semantic selector proof, action proof, post-action state proof, selector recovery path.

### G12 Verified Morphe source ecosystem
**Status:** IN_PROGRESS

Maintain a trust-labeled registry. Verify source ownership, bundle metadata/signatures, supported app versions, and Morphe confirmation before classifying a source as installed.

Exit evidence: at least one source fully verified end-to-end and registry records source, target, release, signature, and runtime confirmation.

### G13 Source-build reproducibility
**Status:** BLOCKED BY GRASSHOPPER BUILD HOST

Build Morphe Manager/Desktop/patch sources from source where feasible.

Exit evidence: JDK prerequisites, persistent storage, deterministic build, artifact hash, runtime installation/acceptance.

### G14 Persistent development substrate
**Status:** BLOCKED

Provision persistent Grasshopper storage and move build caches/artifacts there without touching active runtime state.

Exit evidence: persistent mount verified after reboot, root pressure reduced, build/cache paths redirected, no production disruption.

## Cross-project sequencing

1. Protect production and update graph.
2. Close Android executor and MCP verification.
3. Provision Grasshopper persistent storage and JDK.
4. Turn Grasshopper BIST into the universal machine-readable gate.
5. Re-run production acceptance.
6. Produce clean-host reconstruction evidence.
7. Complete Morphe source verification and source builds.
8. Prove second terminal/executor/substrate.
9. Enable bounded autonomous operations.
10. Broaden into multi-cloud/self-repair swarms only after the earlier gates are proven.

## Anti-regression rule

No later goal may be marked complete because an earlier goal was skipped, renamed, simulated, or represented only by documentation.

## Broccoli-specific execution gates

The Android branch must not re-run solved transport experiments.

### B0 Transport preflight
Read `docs/BROCCOLI_ITERATION_KNOWLEDGE_2026-10-01.md`.

Exit condition:
- identify whether failure is caller, Termux, Rish, Android, or target app
- identify the existing proof that already covers the suspected layer
- define one new piece of evidence before executing

### B1 Canonical Rish transport
**Status: PROVEN**

Required invariant:
`RISH_PRESERVE_ENV=0`

Required target proof:
`uid=2000(shell)`, SDK 35, explicit artifact/marker.

Regression response:
restore the known-good transport before investigating higher layers.

### B2 Android MCP
**Status: IN_PROGRESS**

The MCP server runs phone-local beside Broccoli/Rish. Mutations are confirmation-gated and fail closed.

Exit:
local initialize + real Rish action + durable evidence.

### B3 UI automation
**Status: IN_PROGRESS**

Exit:
observe -> semantic locate -> act -> reobserve -> verify, with selector recovery and no coordinate guessing unless evidence supports it.

### B4 Supervisor lifecycle
**Status: PROVEN for bounded recovery**

Exit already demonstrated:
one supervisor, one child, lock ownership, child termination and recreation, fresh MCP initialize.

Still separate NOT_PROVEN gates:
reboot restoration, battery exemption, force-stop immunity.

### B5 Morphe
**Status: IN_PROGRESS**

A deep link or app launch is not source installation proof. Source confirmation UI and resulting runtime state must be observed.

### B6 Regression guard
**Status: REQUIRED FOR ALL BROCCOLI CHANGES**

Every transport change follows:
`.new -> syntax/self-test -> target artifact proof -> atomic promotion`

No RC=0-only PASS.
No duplicate `rish_run.sh`.
No whole-environment persistence.
No chat-only execution loop.
No historical checkout modernization without an explicit goal.
