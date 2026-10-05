# OmniKali Architecture Salvage Register

**Snapshot:** 2026-10-05 EDT
**Purpose:** Preserve the goals and useful evidence of failed, broken, superseded, or incomplete implementations without allowing broken implementation details to remain architectural authority.
**Authority:** Fresh live evidence > explicit contracts/acceptance artifacts > verified source > this register > README summaries > historical material.

## Salvage rule

A broken implementation is not a lost goal.

For every implementation classified `BROKEN_NEEDS_REIMPLEMENTATION`:
- preserve the user-facing/system goal;
- preserve useful source, tests, evidence, failure analysis, and provenance;
- explicitly stop treating the broken implementation as canonical;
- assign one replacement owner;
- define the acceptance artifact that will make the replacement authoritative;
- do not create a second implementation merely because an old one is inconvenient.

Status vocabulary:
- `PROVEN`: backed by executable/live evidence.
- `ACTIVE`: current owner, not necessarily fully proven.
- `NOT_PROVEN`: implementation/evidence exists but required runtime proof is missing.
- `BROKEN_NEEDS_REIMPLEMENTATION`: goal remains valid; current implementation path is known to fail or no longer provides the required capability.
- `BLOCKED`: implementation cannot proceed until a prerequisite outside the code is resolved.
- `ARCHIVAL`: preserve provenance; do not use as a current implementation owner.
- `ADJACENT`: useful but not part of the protected OmniKali core.

## Protected architecture

The protected reference desktop remains:

`CloudFront -> nginx:80/443 -> Helix:8092 -> libvirt/QEMU -> helix-omnikali`

The intentional host-console path remains separate:

`CloudFront /novnc/vnc.html -> websockify:6080 -> host VNC:5900`

The Android transport boundary remains:

`RDC/Termux -> broccoli-core/lib/rish_run.sh -> Rish/Shizuku -> Android shell uid=2000`

Neither boundary is replaced merely because a higher layer is broken.

## Current live infrastructure observations

### Grasshopper workstation
- Desktop Commander device: `grasshopper-workstation`
- Online and reachable.
- Root filesystem: 30G total, about 29G used, about 901M available, **98% full**.
- Existing persistent `/var/oled` remains separate and must not be repurposed without ownership/rollback checks.
- Current Grasshopper checkout is on branch `feat/cloud-android-agentic-device-clean`; its upstream branch is reported as gone.
- Recent commits include cloud-Android contract work, authenticated ADB/token persistence tests, reconnect-session work, and RDC supervisor design.

### AWS/Helix host
- Desktop Commander device: `ip-172-31-8-59`
- Online and reachable.
- Root filesystem: 79G total, about 67G used, about 9G available, **89% full**.
- Helix gateway, hypervisor daemon, libvirt, nginx, Desktop Commander, and the `helix-omnikali` QEMU guest are running.
- The guest QEMU process is using KVM and the expected Kali base/overlay qcow2 layout.
- Cloud-Android QEMU is also running on this host, with local VNC :6082, tokenized websockify, ADB server, and cloudflared tunnel processes present.
- These process observations are operational evidence only. They do **not** prove authenticated browser acceptance, keyboard/input correctness, or Android app-control correctness.

## Repository inventory and disposition

### OmniKali core

| Repository | Disposition | Keep | Replace/rebuild |
|---|---|---|---|
| `Grasshopper` | ACTIVE REFERENCE / RECONSTRUCTION | domain contracts, BIST, evidence, reproducibility, agentic orchestration goals | broken/incomplete cloud-Android viewer/input path; unfinished clean-host/BIST/self-repair gates |
| `helix` | ACTIVE PROTECTED PRODUCTION LINEAGE | authentication, gateway, PostgreSQL task/state/lease contracts, libvirt/QEMU lifecycle, production evidence | only the specific failed/unfinished capabilities; do not replace the core desktop architecture |
| `kali-node` | ACTIVE WORKSTATION LINE | persistent Kali guest, connection state machine, QEMU/RFB/security/reconnect contracts | any UI/input implementation proven broken must be rebuilt behind the existing contracts |
| `grasshopper-kubernetes` | PROTOTYPE / ISOLATED | portability/substrate goal, K8s deployment research, acceptance harness | current implementation cannot become production ingress; new isolated implementation required |
| `omnikali` | ACTIVE EDGE | fail-closed endpoint discovery and external health probe | stale endpoint records/edge behavior when unverified |
| `onnxscibroccoli.github.io` | ACTIVE PUBLICATION SURFACE | stable publication/discovery role | none unless current deployment evidence fails |
| `omnikali-link` | ARCHIVAL/MAINTENANCE | public pointer lineage and phone-shell goal | do not grow into workstation/gateway |
| `GPTOmniKali-full-stack` | ARCHIVAL RECOVERY | recovered source, provenance, historical Vercel pointer, Python orchestrator lineage | do not treat recovery snapshot as deployable production implementation |
| `kiln` | ADJACENT PROTOTYPE | browser-contained VM/alternative execution goal | requires separate acceptance before being promoted |

### Android execution

| Repository | Disposition | Keep | Replace/rebuild |
|---|---|---|---|
| `broccoli-core` | ACTIVE ADJUNCT / HISTORICAL EXECUTOR | Rish transport contract, Android executor philosophy, archive/memory work, proven wrapper | incomplete higher-level MCP/UI acceptance; do not duplicate Rish |
| `broccoli-rish` | ACTIVE CANONICAL TRANSPORT EXTRACTION | canonical `rish_run.sh`, fail-closed probe, transport contract | fresh physical-device re-proof is required before promotion beyond NOT_PROVEN |
| Android RDC supervisor work | NOT_PROVEN / REBUILDABLE | supervisor design, bounded recovery contract, prerequisite checks | fresh installed crash/recovery/reboot implementation and acceptance |
| Cloud Android viewer/input path | **BROKEN_NEEDS_REIMPLEMENTATION** | goal: persistent cloud Android workstation, reconnectable screen, native keyboard/input, Home/Back/App controls, ADB/MCP control | current custom viewer/control layer that blocks/misplaces controls or fails to deliver physical keyboard input |
| Cloud Android accelerated OCI/Cuttlefish path | **BLOCKED_NEEDS_NEW_SUBSTRATE** | goal: persistent/ephemeral Android workstation with provider-neutral capability selection and always-free-first policy | OCI A1 accelerated-Cuttlefish assumption; select a substrate that actually provides required virtualization |
| Android UI automation | IN_PROGRESS / NOT_PROVEN | observe -> understand -> locate -> act -> reobserve -> verify contract, semantic selectors | complete real-app acceptance and recovery |
| Ruto virtual-display integration | NOT_PROVEN | virtual-display goal and existing display-state evidence | third-party activity placement behavior requires fresh acceptance |
| `shizuku-silent-mic` | ARCHIVAL/EMPTY | reserved experiment only | new implementation only if the capability is explicitly activated |
| `android-virtual-mic-shizuku` | ARCHIVAL/EMPTY | reserved experiment only | new implementation only if activated |
| `shizuku-virtual-mic` | ARCHIVAL/EMPTY | reserved experiment only | new implementation only if activated |

### Morphe

| Repository | Disposition | Keep | Replace/rebuild |
|---|---|---|---|
| `morphe-manager` | ACTIVE SOURCE FORK / NOT_PROVEN RUNTIME | source, build system, patch-manager goal | runtime installation/confirmation path still needs proof |
| `morphe-desktop` | ACTIVE SOURCE FORK / NOT_PROVEN RUNTIME | desktop patching/source-build goal | runtime acceptance and artifact verification |
| `morphe-patches` | SOURCE REGISTRY | source lineage and patch metadata | verify target/version/signature/runtime |
| `morphe-patches-1` | SOURCE REGISTRY | distinct source lineage | same trust gates |
| `Morphe-Patches-2` | SOURCE REGISTRY | distinct source lineage | same trust gates |
| `morphe-patches-template` | DEVELOPMENT TEMPLATE | official template lineage | build/runtime acceptance |
| Morphe source-build program | **BLOCKED** | source reproducibility goal | persistent build storage + JDK + deterministic artifact verification |

### Coordination/research/dependencies

| Repository | Disposition |
|---|---|
| `omn-kali-knowledge-graph-master` | **CANONICAL COORDINATION INDEX**. Preserve historical graphs; this register becomes the current salvage/rebuild layer. |
| `lattice` | ADJACENT RESEARCH. Preserve independently; not a production dependency. |
| `lattice-audit` | ADJACENT AUDIT SURFACE. Preserve independently. |
| `noVNC` | DEPENDENCY MIRROR. Keep as dependency provenance, not custom desktop authority. |
| `oauth2-proxy` | DEPENDENCY MIRROR. Keep as dependency provenance, not auth architecture authority. |

### Published/adjacent applications

| Repository | Disposition |
|---|---|
| `half-a-mile` | ACTIVE SEPARATE PRODUCT |
| `newsroom-desk` | ACTIVE SEPARATE PRODUCT |
| `dectalk-live` | PUBLISHED SEPARATE PRODUCT |
| `ara-github-write-test` | ARCHIVAL CAPABILITY PROOF |
| `ara-github-write-test-2` | ARCHIVAL CAPABILITY PROOF |

## Clearly broken or invalid implementation paths

### 1. Custom cloud-Android viewer/input implementation
**Status:** `BROKEN_NEEDS_REIMPLEMENTATION`

Goal retained:
- a persistent cloud Android device that a physical Android can access;
- usable screen/viewer;
- physical keyboard input delivered to Android;
- reliable Home/Back/Recents controls;
- reconnect without destroying the guest;
- ADB/MCP control;
- human gates surfaced on the physical device.

Why the implementation is rejected:
- recent live testing showed the display could render while physical keyboard input did not reach Android;
- custom overlay controls became misplaced/hidden and interfered with the Android display;
- disconnected viewer links were not reliably reconnecting to a real VM.

Replacement rule:
- do not keep patching the broken UI layer indefinitely;
- first prove the underlying QEMU -> VNC/RFB -> websockify -> viewer transport independently;
- then add controls as a thin client contract;
- then prove keyboard/input with an observable Android-side artifact;
- then prove reconnect/persistence.

### 2. OCI A1 accelerated-Cuttlefish assumption
**Status:** `BLOCKED_NEEDS_NEW_SUBSTRATE`

Goal retained:
- provider-neutral, always-free-first capability selection for Android/cloud desktops.

The OCI A1 KVM limitation is evidence against that substrate for accelerated Cuttlefish. It is not evidence against the product goal.

Replacement:
- capability matrix -> substrate selection -> isolated deployment -> end-to-end acceptance.
- Paid metal remains optional and must never become an implicit mandatory dependency.

### 3. Grasshopper clean-host/source-build path
**Status:** `BLOCKED_NEEDS_NEW_IMPLEMENTATION/INFRA`

Goal retained:
- an authorized agent can reproduce the system from source without undocumented operator steps.

Current blockers:
- root disk pressure;
- missing persistent build workspace permissions;
- missing JDK prerequisites documented by the graph.

Replacement:
- provision/attach authorized persistent storage;
- relocate only cold/regenerable caches after byte/ownership checks;
- install JDK prerequisites;
- run deterministic clean-host dry-run;
- capture source SHA/config/artifact manifest.

### 4. Universal exactly-once claim
**Status:** `INVALID_ARCHITECTURAL_CLAIM`

Retain:
- fenced task ownership;
- stale lease recovery;
- duplicate control-plane fencing.

Reject:
- universal exactly-once external side effects.

Replacement:
- command-type-specific idempotency, cancellation acknowledgement, reconciliation, and explicit side-effect semantics.

### 5. Prototype ingress on the protected Helix host
**Status:** `INVALID/PROHIBITED`

Retain:
- isolated second-substrate goal.

Reject:
- any implementation that claims host 80/443, DNATs the protected path, or silently replaces CloudFront/nginx/Helix.

The previous K3s/Traefik collision remains a permanent regression lesson.

## Goals preserved from broken work

1. Remote AI computer with a real persistent desktop/Android environment.
2. Agent execution platform with durable tasks, leases, recovery, fencing, idempotency, cancellation.
3. Agent infrastructure/control plane independent of any one cloud provider.
4. Always-free-first capability selection with optional paid accelerators.
5. Physical Android as a human-intervention/control plane.
6. Human gates for OAuth/CAPTCHA/device approvals with pause/resume.
7. APK-first inspection and semantic UI automation.
8. Morphe source trust, patching, signing, installation, and runtime verification.
9. Searchable protected cross-provider chat archive with crash-safe Android paging.
10. Clean-host agentic reconstruction.
11. Machine-readable BIST with strict PASS/FAIL/NOT_PROVEN/NOT_APPLICABLE.
12. Bounded self-repair with restore points and loop limits.
13. Second executor and second substrate behind the same domain contracts.
14. Durable knowledge graph and provenance across all implementation lanes.
15. Persistent/reconnectable remote sessions independent of chat/token lifetime.

## Live gate update 2026-10-05

### R1 Persistent development storage
**Status: PASS / OPERATIONAL**
- Grasshopper has a persistent `/srv/grasshopper` filesystem backed by `/dev/sdb`, approximately 112G.
- The mount is present in `/etc/fstab` with `nofail` and device timeout settings.
- Root pressure was reduced from 98% to 86% by quarantining disposable container-image storage with matching SHA-256 hashes before deletion and removing an unreferenced DNF temporary cache.
- A durable agent workspace/cache/artifact/log area exists under the user-owned `/srv/grasshopper/backups/` subtree because the mount root itself is root-owned.

### R2 Cloud Android
**Screen transport status: PASS / PROVEN**
- QEMU Android guest boots.
- VNC/RFB handshake succeeds on loopback.
- token-gated websockify serves noVNC.
- VNC keyboard input can switch from the stale SeaBIOS framebuffer to the Android graphical surface.
- VNC pointer input reaches the Android graphical surface.
- websockify restart preserves the QEMU guest and bearer token.

**ADB agent status: BROKEN_NEEDS_REIMPLEMENTATION**
- The Android guest remains `offline` to host ADB on `127.0.0.1:5555`.
- Multiple standard Android-x86/AOSP adbd init triggers and the required `qemu=1` boot property were tested without producing an online ADB transport.
- Do not change the proven screen transport to compensate for this failure.
- Next implementation must establish a guest-side adbd lifecycle proof or deliberately replace ADB with a formally equivalent agent transport while preserving the MCP control goal.

## Rebuild queue

### R0 Protect
- Freeze the validated Helix production chain.
- Freeze canonical Rish transport.
- Do not perform destructive storage/network changes while root disks are critically full.

### R1 Storage
- Resolve Grasshopper persistent build storage.
- Reduce root pressure safely.
- Record post-change evidence.

### R2 Cloud Android transport
- Prove QEMU is reachable through a single canonical RFB path.
- Prove keyboard, pointer, and control events independently.
- Remove/replace broken overlay behavior rather than layering more controls on it.
- Prove reconnect after viewer restart without guest restart.

### R3 Android executor
- Re-prove physical Rish/Shizuku transport.
- Complete real-app observe/select/act/verify.
- Keep supervisor recovery bounded and explicitly separate reboot/force-stop gates.

### R4 BIST
- Emit strict machine-readable statuses.
- Make release/merge gates consume BIST.
- Never promote a process-only health check to capability proof.

### R5 Production acceptance
- Fresh authenticated browser acceptance.
- Eight resilience scenarios.
- Capture user-visible evidence and acceptance IDs.

### R6 Reproducibility
- Clean-host reconstruction.
- Deterministic source/artifact/config manifest.
- Recovery/rollback evidence.

### R7 Morphe
- Verify at least one patch source end-to-end.
- Build from source after storage/JDK prerequisites.
- Hash/sign/verify artifacts and observe runtime confirmation.

### R8 Generalization
- Second terminal.
- Second executor.
- Isolated second substrate.
- Bounded autonomous operations.

## Non-negotiable failure lessons

- RC=0 with empty output is not PASS.
- A running process is not an end-to-end capability.
- A screenshot is not authentication or input proof.
- Do not edit a proven lower transport layer to compensate for a caller-boundary failure.
- Do not create duplicate transports.
- Do not copy entire Termux environments.
- Do not install prototype ingress on the protected production host.
- Do not promote documentation claims over executable evidence.
- Do not spend scarce disk space on heavy builds before persistent storage is ready.
- Preserve source lineage even when the implementation is rejected.

## Durable continuation

The repository graph remains the source of architectural ownership. This register is the salvage layer. Future agents should start here, then follow the owning repository's contract and evidence files.

**Next authoritative update:** after the first R1/R2/R3 gate changes, create a new dated register rather than mutating this historical snapshot.
