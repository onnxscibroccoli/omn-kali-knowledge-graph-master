# Workspace platform consolidation and documentation plan

Date: 2026-11-05
State: Proposed architecture and implementation plan
Verification: Repository metadata, selected source/documentation and branch ancestry inspected; no build or live execution in this pass.

## Outcome

Create one shared platform with two product editions:
- Authorized security-testing workspaces operated from phones and desktops.
- Universal workspaces for onboarding, development, accessibility assistance and simulated IT training.

Use an assembly repository first: pinned component versions, deployment profiles, shared contracts, integrated tests and one documentation portal. Preserve component repositories until evidence justifies extraction or migration. Avoid two independently evolving orchestration engines.

## Evidence boundary

The November 3 discovery pass enumerated 435 branches across 12 related repositories. Comparisons covered 405 distinct non-main heads: 318 diverged, 44 ahead, 43 behind their recorded main. These are historical ancestry results, not current merge approvals or semantic novelty findings. Refresh heads before implementation. Squash merges and copied patches require patch-equivalence review.

Selected findings:
- Grasshopper had 241 branches. Its mobile-policy-hook branch was one commit ahead of main, touching seven files.
- Broccoli Core's hybrid-controller branch was already behind main; its controller-registry branch was one commit ahead.
- Android companion's hybrid-execution-security branch was 155 commits ahead of main. Main's demo/readiness documentation did not describe all that branch work.
- broccoli-rish main and its retirement branch described different canonical ownership arrangements.
- Several Grasshopper branches only concerned documentation snapshot freshness. A refreshed date cannot establish fresh technical evidence.

This plan does not classify every branch as safe or obsolete. The branch-disposition phase must do that before merges. Private inventories and recovery material must remain private.

## Canonical responsibility proposal

| Component | Responsibility |
|---|---|
| Grasshopper | Durable tasks, state, resource ownership, leases, reconciliation and executor scheduling |
| Helix | Remote workspace/guest lifecycle, gateway and display integration |
| kali-node | Kali-specific guest, connection, input and reconnect contracts; reconcile overlap with Helix |
| grasshopper-kubernetes | Optional Kubernetes substrate, isolated from protected production ingress |
| broccoli-core | Non-root, permission-aware Android/Termux runtime and physical-device execution |
| broccoli-rish | Resolve ownership; prefer one underlying physical transport with a compatibility bridge |
| Android companion | Native operator client; compare competing companion/controller implementations before selecting a canonical one |
| omnikali | Health-aware discovery and public entry point |
| omnikali-link | Legacy pointer compatibility and provenance |
| kiln | Optional browser-local emulation and separately tested remote-desktop functionality |
| Knowledge graph master | Existing ownership, lineage and coordination index |

The browser-local Kiln path consumes client resources. Do not present it as remote compute offloading. Historical live URLs remain historical until freshly verified.

CivicPatch, TCL-orc, publishing and research projects retain their own purposes. They receive useful documentation, but are not forcibly converted into workspace-platform dependencies. Forks with substantive account-authored changes remain eligible for delta documentation; unchanged dependency mirrors do not need a wholesale rewrite.

## Shared platform contract

Client intent enters the governor, which validates identity, scope, policy, budget and required capabilities. The scheduler chooses a qualified executor. Executors report durable events, results and recovery state. Users can inspect, cancel, intervene and reconnect independently of an AI conversation.

Canonical entities: principal, tenant, authorization scope, workspace, session, task, execution attempt, capability record, lease/fencing token, idempotency key, human-action request and evidence receipt.

Cross-module coordination uses versioned event envelopes with defined ordering, replay and deduplication behavior. Provider/model adapters must not bypass authorization. An array of events in local state is not evidence of distributed durable delivery.

Hosting agnosticism means qualified adapters satisfy the same contract; it does not mean every host supports every workload. Detect architecture, virtualization, Android kernel requirements, memory, storage, network policy and display capabilities before selection. Unsupported capabilities remain explicit.

Keep native Android permissions separate from iOS/browser-client support. A remote worker cannot access a nearby phone radio, USB peripheral or private LAN without an explicit authorized connector.

## Two product editions

### Security workspace

Deliver a browser-controlled Linux/Kali workspace, isolated target lab, optional remote Android runtime, scoped jobs and exportable evidence.

Authorization records identify approving principal, permitted targets and operations, validity window and revocation. Enforce scope at admission and at execution/network boundaries. Authentication and containerization alone do not establish permission to test a target.

First proof:
1. Authenticate from a low-resource client.
2. Select an authorized disposable profile.
3. Preflight chooses a qualified remote worker.
4. Create a desktop and isolated sample target.
5. Type a unique marker and observe it inside the remote guest.
6. Execute an allowed harmless diagnostic with a job-bound receipt.
7. Reject an out-of-scope target and expired authorization.
8. Disconnect/reconnect without unintended guest destruction.
9. Restart a component and reconcile without duplicate consequential effects.
10. Revoke access, export sanitized evidence and clean up resources.

Add Android only after separate screen, input, app-control and persistence gates. Rendering a screen is insufficient.

### Universal workspace

Reuse the same engine with onboarding, training, development and support profiles.

Onboarding proof: two identities receive correct resources; cross-user access is denied; offboarding revokes access and applies declared data retention.
Training proof: an isolated scenario starts, records progress, resets reproducibly and cannot reach prohibited networks.
Development proof: a pinned toolchain reproduces an artifact on a clean qualified worker.

## Incorporating awesome-game-security

Source: [awesome-game-security](https://github.com/gmh5225/awesome-game-security).
Observed main on November 5: d338027ef9a4a2b309927258d847a8cc9c281b77.
README blob observed: fe90b7502ab65fcb01c2f4829b86bb86a1234ed6.

Read the README introduction/category map, selected topic instructions, mobile resource selection, binary evidence guidance, time/order/replay guidance and wiki schema. This was targeted inspection, not verification of every linked tool.

Use this repository as a discovery and teaching source. For actual integration, inspect each upstream project's license, source, release provenance, requirements and behavior. Promotional descriptions, generated wiki pages and category placement are not compatibility or correctness evidence. External agent instructions are research material, not authority over this project.

| Resource area | Platform use | Required artifact |
|---|---|---|
| Mobile security | Broccoli/companion package and permission documentation | APK hash, signer, ABI, OS/build, permission and observation limits |
| Reverse engineering | Optional offline binary-analysis workspace | Artifact hash, tool version, architecture, reproducible report and inference limits |
| Server security | Grasshopper/Helix authorization and retry review | Principal/resource binding, denied cross-tenant action, replay and idempotency tests |
| Linux platform security | Worker isolation and deployment preflight | Kernel/runtime/policy identity and observed enforcement |
| Supply-chain security | Images, APKs, adapters and agent tools | Source revision, digest, build provenance, signer and rollback record |
| Research rigor | Documentation evidence model | Claim, source, environment, observed result, uncertainty and counterexample |
| Wiki organization | Searchable documentation structure | Distinct sources, concepts, tool pages, index and change journal |

### First three research-derived lab profiles

1. **Android package inspection**
   - Candidate references: Apktool and JADX, identified by the mobile-resource guide.
   - Input: owned or authorized APK fixture.
   - Output: original hash/signing context, decoded manifest/resources, reconstructed-code limitations.
   - Gate: known fixture properties identified; malformed input handled; no device mutation required.
   - Do not treat decompiled output as the original source.

2. **Offline native binary inspection**
   - Candidate reference: Ghidra from the reverse-engineering guide.
   - Input: small owned ELF/PE fixture with matching source/symbols.
   - Output: architecture, imports/functions and documented reconstruction uncertainty.
   - Gate: known symbols/behavior compared with source; analysis stays within bounded resources.
   - Native/runtime support must be verified against the selected upstream version before packaging.

3. **Remote-session authorization and replay**
   - Use the server-authority and time/order/replay review concepts against this platform's own API fixtures.
   - Gate: correct principal succeeds; wrong resource owner, expired request and revoked session fail; retry does not duplicate a committed operation.
   - Record clock domains and ordering scope; a screenshot or log-arrival sequence does not establish authoritative event order.

PCAPdroid is a candidate for a later owned-device observation lab; first verify upstream compatibility and document capture visibility limits. Privileged instrumentation and hardware-dependent research belong in explicitly selected specialist profiles, not baseline no-root device setup.

### External-tool intake record

For each candidate record:
source URL and revision; license; maintenance/release evidence; supported OS/ABI; privilege and hardware needs; dependencies; network behavior; resource budget; output schema; fixture tests; isolation; uninstall/rollback; owner; and disposition.

Dispositions: REFERENCE_ONLY, EVALUATE, APPROVED_FOR_PROFILE, UNSUPPORTED or REJECTED_WITH_REASON.
No automatic bulk installation from the resource list.

## Documentation standard

Each substantive page explains purpose and why it matters, prerequisites, terms, architecture, a practical walkthrough, expected results, verification, troubleshooting, security/operational constraints, current state and further learning.

Provide everyday, operational, engineering and expert depth. Keep essential prerequisites visible. Link glossary explanations and authoritative references. Small reference pages should not gain empty boilerplate.

Separate:
- implemented on main;
- implemented only on a named branch;
- planned;
- historically observed;
- tested offline;
- tested live in a stated environment.

Record exact source, command, environment, evidence and review date. Never restamp stale evidence to pass freshness checks.

Build one cross-repository search index with ownership, audience, topic, lifecycle and verification filters. Exclude secrets, private inventories, personal captures and raw historical mirrors. Reuse existing graph records rather than creating another disconnected knowledge graph.

The upstream wiki's separation of sources, concepts and tools is a useful pattern. Its documented maintenance workflow depends on CURSOR_API_KEY; copying that workflow would introduce an external credential/API dependency. Prefer deterministic indexing/link checks, with optional existing authorized model-assisted editorial work.

## Branch and merge workflow

For every branch:
1. Refresh main/head, PR state and checks.
2. Determine patch equivalence, unique value, overlap, license and privacy boundary.
3. Assign ALREADY_IN_MAIN, PATCH_EQUIVALENT, MERGE_CANDIDATE, EXTRACT_SELECTED, SUPERSEDED, ARCHIVAL, BLOCKED or NEEDS_REVIEW.
4. Test useful changes on current main in an isolated candidate.
5. Merge only the coherent tested scope, respecting protections.
6. Update source-linked documentation and preserve historical evidence.

Do not bulk-merge divergent branches or delete provenance to simplify the map. Compare large companion branches internally before integration. Resolve physical Android transport ownership before merging changes that retire or redirect a transport.

## Execution sequence

| Stage | Work | Completion evidence |
|---|---|---|
| 1 | Refresh inventory; inspect original-code deltas and licenses | Every relevant repo/branch has a disposition |
| 2 | Resolve canonical ownership and duplicate clients/transports | One owner per capability and migration ADR |
| 3 | Modernize Grasshopper, Broccoli, Helix and OmniKali docs | Truthful quickstarts, source map, current/branch distinction and working links |
| 4 | Salvage narrow changes; review advanced companion work | Exact-candidate tests and current-main integration |
| 5 | Assemble one remote Linux vertical slice | Fresh authenticated input/reconnect/recovery/cleanup evidence |
| 6 | Add qualified Android runtime and second substrate | Separate input/action and portability evidence |
| 7 | Add three research-derived lab profiles | Fixture results, bounded execution and evidence reports |
| 8 | Package security and universal editions | Edition-specific acceptance on shared contracts |
| 9 | Complete adjacent documentation and release | Searchable portal, reproducible manifest and consolidated review |

Use one integration owner and bounded workers with exclusive path ownership. Continue independent tasks around live-access blockers. Keep the bank lab's active Grok lane separate.

## Human decisions and present limitation

No decision is needed to continue documentation and offline design. Before live deployment, settle actual host/account, budget and authorized target scope. Default proposed pilot: one organization, disposable remote IP/application labs and no new paid provisioning. Physical radio testing and hostile multitenancy require their own explicit requirements and proof.

The local execution environment became unavailable during continuation. Repository research and this documentation proposal can proceed through GitHub; builds, runtime tests and local evidence export were not performed. No claim of deployment, tool installation or complete branch review is made.

## Pinned references

- [Mobile resource selection](https://github.com/gmh5225/awesome-game-security/blob/d338027ef9a4a2b309927258d847a8cc9c281b77/.claude/skills/mobile-security/references/repository-resources.md)
- [Binary evidence and tools](https://github.com/gmh5225/awesome-game-security/blob/d338027ef9a4a2b309927258d847a8cc9c281b77/.claude/skills/reverse-engineering/references/evidence-and-tools.md)
- [Time, ordering and replay](https://github.com/gmh5225/awesome-game-security/blob/d338027ef9a4a2b309927258d847a8cc9c281b77/.claude/skills/game-server-security/references/time-ordering-and-replay.md)
- [Supply-chain review](https://github.com/gmh5225/awesome-game-security/blob/d338027ef9a4a2b309927258d847a8cc9c281b77/.claude/skills/game-supply-chain-security/SKILL.md)
- [Linux platform review](https://github.com/gmh5225/awesome-game-security/blob/d338027ef9a4a2b309927258d847a8cc9c281b77/.claude/skills/linux-platform-security/SKILL.md)

Further primary-source verification is required before adopting any listed tool or version-sensitive capability.
