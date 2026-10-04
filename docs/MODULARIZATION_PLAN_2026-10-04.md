# OmniKali Agentic Modularization Plan

**Plan tag:** OMNIKALI-MODULARIZATION-2026-10-04
**Status:** PLANNED / NOT_PROVEN
**Companion graph:** OMNIKALI-SYSTEM-KG-2026-10-01
**Companion goals:** OMNIKALI-SYSTEM-GOALS-2026-10-01
**Program issue:** https://github.com/onnxscibroccoli/Grasshopper/issues/65
**Charter:** docs/ORCHESTRATOR_CHARTER.md

This document is a coordination plan. It is not permission to archive repositories, mutate production ingress, or promote status to PROVEN.

## Why this exists

The account already has 29 repositories. The agentic problem is not "too few repos." It is:

1. more than one owner for the same capability;
2. one repository (`broccoli-core`) that an agent cannot load, test, or change safely;
3. Grok App Builder chrome wrapping real infrastructure (Helix, grasshopper-kubernetes, kiln);
4. a recovery workspace (`GPTOmniKali-full-stack`) that looks like a second workstation implementation.

G1 already requires: one machine-readable contract per boundary and no duplicate owner for the same capability. This plan executes that rule without substituting a new architecture.

## Intended architecture (frozen)

From Grasshopper `IMPLEMENTATION_SEED.md` and Helix production evidence:

```
OmniKali
|
+-- Remote AI Computer
|   +-- Kali guest (PROVEN production path)
|   +-- future Linux / Windows / edge environments
|
+-- Agent Execution Platform (Grasshopper)
|   +-- tasks, workers, leases, execution, artifacts
|   +-- idempotency, cancellation, recovery
|
+-- Agent Infrastructure Control Plane (Helix + Grasshopper)
    +-- auth, provisioning, orchestration
    +-- durable PostgreSQL state, observability, resources
```

Android is a second executor, not a replacement desktop:

```
RDC/Termux -> broccoli-core -> lib/rish_run.sh -> Rish/Shizuku -> Android shell uid=2000
```

### Production path that must not be split or replaced

```
omnikali discovery door
  -> CloudFront
  -> nginx :80
  -> Helix :8092
  -> libvirt/QEMU
  -> helix-omnikali Kali guest
```

Separate, intentional hypervisor console:

```
CloudFront /novnc/vnc.html -> host websockify :6080 -> host VNC :5900
```

Kubernetes, FRP, Kiln native VNC, and GPT recovery snapshots must not silently become this path.

Engineering rule: freeze the proven core, extract around it, then generalize outward.

## Inventory classification (29 repos)

### Keep as-is (already correctly bounded)

| Repo | Why |
|---|---|
| omn-kali-knowledge-graph-master | Canonical contracts, graph, goals |
| omnikali | Fail-closed public discovery door |
| omnikali-link | Legacy pointer; maintenance only |
| onnxscibroccoli.github.io | Publication surface |
| lattice / lattice-audit | Independent research; out of OmniKali runtime |
| half-a-mile / newsroom-desk / dectalk-live | Published apps; out of OmniKali runtime |
| noVNC / oauth2-proxy | Upstream dependency forks |
| morphe-manager / morphe-desktop / morphe-patches* / morphe-patches-template | Vendor source registries; keep source-specific trust labels |
| ara-github-write-test* | Completed probes; archival-in-place |
| shizuku-*-mic | Empty experiments; do not activate unless explicitly requested |

### Keep, but stop treating as competing owners

| Repo | Actual role | Forbidden role |
|---|---|---|
| helix | Production gateway + hypervisor control plane | Do not become the Android executor or K8s origin |
| kali-node | Guest/workstation contract and Track B implementation | Do not become a second public origin |
| Grasshopper | Reference control plane + reconstruction | Do not copy Broccoli's script pile |
| grasshopper-kubernetes | G8 second substrate prototype | Do not bind 80/443 or replace CloudFront |
| kiln | Browser-contained v86 PC | Do not describe Tiny Core as Kali Rolling |
| GPTOmniKali-full-stack | Recovery/provenance | Do not receive new product features |
| broccoli-core | Android adjunct + historical lab | Do not remain the only place agents can edit Android code |

## Capability ownership map (target)

One capability, one owner. Other repos may consume the contract; they may not reimplement it.

| Capability | Owner | Consumers | Split? |
|---|---|---|---|
| Task lifecycle PENDING->RUNNING->COMPLETED\|FAILED | Grasshopper | Helix, Android MCP, K8s | No. Internal packages only. |
| Authenticated desktop session / RFB tickets | helix | kali-node, omnikali | No. Frozen production. |
| Kali guest persistence / QEMU | kali-node + helix `production/` | Grasshopper reconstruction | No until G2/G3 pass. |
| Public discovery / health door | omnikali | none | No. |
| BIST / merge gate schema | knowledge-graph-master `schemas/` | all Lane A | No new repo. Expand contracts here. |
| Android Rish transport | **extract** `broccoli-rish` | broccoli-mcp, Grasshopper MCP client | **Yes. First physical split.** |
| Android MCP + supervisor | **extract** `broccoli-mcp` after rish extract is proven | Grasshopper | Yes, gated. |
| APK/UI observe-act-verify | stay in broccoli-core until MCP extract is proven | Morphe verification | Later. |
| Isolated K8s desktops | grasshopper-kubernetes Helm chart | Grasshopper G8 | Internal extract from Grok scaffold; not a new GitHub repo yet. |
| In-browser v86 PC | kiln `src/lib/linux` | none | Freeze native XFCE/noVNC path as non-owner. |
| Morphe source trust | knowledge-graph-master + morphe-* forks | broccoli UI loop | No first-party rewrite. |

## What actually needs to be broken out

### 1. broccoli-core — the only mandatory repo split

Evidence: ~5,900 entries, ~58k, committed logs, Word docs, workspace backups, `_quarantine`, nested `broccoli-core/`, `Agent/Broccoli/mirror/`, historical `runs/`, root-level `advance_step*.sh`.

An agent cannot complete a one-line transport change without loading unrelated history. That is the modularization failure.

**Do not clean in place.** Broccoli README already forbids indiscriminate cleanup because the history is evidence.

Extract, leaving broccoli-core as the archive:

```
broccoli-rish          PROVEN transport only
  lib/rish_run.sh
  tools.android_transport.RishTransport
  lib/rish_transport_probe.sh
  fail-closed evidence contract (no RC=0-empty PASS)
  AGENTS.md + tests that prove uid=2000 and SDK 35

broccoli-mcp           G10, after broccoli-rish is consumed
  phone-local MCP server
  supervisor lock/PID recovery
  confirmation-gated mutations

broccoli-core          ARCHIVAL owner of everything else
  kernel, Agent/, mirrors, chat loops, AutoJS adapters, docs
  no new features except pointing consumers at the extracts
```

Non-negotiable extract rules:

- `RISH_PRESERVE_ENV=0` remains the invocation invariant.
- Do not create a second `rish_run.sh`.
- Do not persist the whole Termux environment.
- Do not treat RC=0 with empty output as PASS.
- The executor stays on the phone. A workstation process must not impersonate it.

### 2. Helix / kali-node / GPTOmniKali-full-stack — ownership, not a three-way split

These three currently all contain workstation/gateway/QEMU/RFB material.

Target:

- helix owns live gateway, auth, hypervisor, AWS/OCI IaC, production contracts.
- kali-node owns the guest/workstation behavior contract and Track B tests.
- GPTOmniKali-full-stack owns recovered lineage only. Prefix any remaining notes with GPT. No feature work.

Do **not** carve Helix into `helix-app`, `helix-infra`, `helix-hypervisor` until G2 (fresh production acceptance) and G3 (clean-host reconstruction) pass. Splitting the proven core is an architecture substitution.

Helix internal module boundaries (packages, same repo) are allowed:

- `src/` web/auth/session
- `production/` live contracts
- `infra/` Terraform/Ansible
- `hypervisor/` QEMU utilities
- `test-suite/` live vs declarative tests stay explicit

### 3. grasshopper-kubernetes — strip the Grok scaffold, keep one repo

The Helm chart under `grasshopper-kubernetes/` is the real substrate. The surrounding Vite/TanStack/Grok App Builder tree is chrome. Agents confuse the chrome with the cluster.

Action: make the chart the default agent surface (`AGENTS.md` points at Helm + acceptance scripts first). Do not create `grasshopper-k8s-chart` until the chart has its own test command and the web-console is optional.

### 4. kiln — two products, one freeze

Keep kiln as the v86 browser PC. Mark native XFCE/TigerVNC/KasmVNC scripts as a non-owner prototype so agents cannot treat them as a third desktop path. No new repo unless v86 and native paths both become production, which they are not.

### 5. Grasshopper — do not split the control plane

Grasshopper is the right size (~1k). The large docs/evidence tree is intentional protection, not bloat. Internal packages only:

- `src/model.mjs` + `src/store.mjs` + `src/control-plane.mjs` + `src/executor.mjs`
- `src/mcp/`
- `src/clients/`
- `src/android/` consumes broccoli-rish/mcp; does not own Rish

Copying Broccoli historical scripts into Grasshopper remains forbidden.

## Agentic operating contract (how a future agent uses this)

An authorized agent gets **one repo, one capability, one test command, one restore point**.

```
inspect graph -> confirm owner -> restore point -> smallest change
  -> narrow test -> acceptance artifact -> graph update
```

If ownership is ambiguous, stop. Do not create a second copy.

Agent-sized slices this plan makes legal:

1. broccoli-rish extract (this plan's first physical change)
2. BIST schema expansion in knowledge-graph-master (G4)
3. Grasshopper executor idempotency/cancellation (already G1/G5, same repo)
4. grasshopper-kubernetes Helm-only acceptance (G8, no 80/443)
5. Helix production acceptance evidence (G2, no architecture change)

Agent-sized slices this plan forbids until earlier gates pass:

- splitting Helix
- new public ingress
- new Rish wrapper
- promoting kiln or K8s to production origin
- rewriting Morphe as first-party
- deleting broccoli-core history

## Implementation sequence

M0 Graph and ownership freeze (this document). **IN_PROGRESS.**
M1 Extract `broccoli-rish` from proven files only. broccoli-core remains the archive. **PLANNED / HUMAN GATE before repo creation.**
M2 Point Grasshopper Android client and broccoli MCP at broccoli-rish. No transport rewrite.
M3 Extract `broccoli-mcp` only after M2 has live uid=2000 evidence.
M4 Helix/kali-node/GPT ownership README + AGENTS.md alignment. No code move.
M5 grasshopper-kubernetes AGENTS.md defaults to Helm/acceptance.
M6 kiln native path labeled non-owner.
M7 Only then consider additional repos.

M1 requires explicit operator approval because it creates a repository. M4-M6 are documentation/ownership changes and may proceed after this plan is merged.

## Human gates (from orchestrator charter)

Do not do these without a named approval:

- create or delete repositories
- archive repositories
- change CloudFront / nginx / ports 80/443
- promote any item to PROVEN
- mass-delete Broccoli commentary, mirrors, or logs

## Success criteria

This plan is done when:

1. every OmniKali capability has exactly one owner in this document and in each repo `AGENTS.md`;
2. an agent can change the Rish transport without opening the Broccoli mirror;
3. an agent can change Grasshopper task lifecycle without opening Helix hypervisor code;
4. an agent can change the K8s chart without treating Grok scaffold files as the product;
5. Helix production path is unchanged and still the only public origin.

Missing evidence stays NOT_PROVEN.
