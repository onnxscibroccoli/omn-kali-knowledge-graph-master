
# OmniKali System Knowledge Graph

**Graph tag:** OMNIKALI-SYSTEM-KG-2026-10-01
**Snapshot:** 2026-10-01 EDT
**Canonical index:** onnxscibroccoli/omn-kali-knowledge-graph-master

This graph is the current cross-repository coordination map. Historical graph tags remain immutable evidence.

## Authority

1. Fresh live acceptance and runtime evidence
2. Explicit production contracts and acceptance artifacts
3. Source implementation verified against those contracts
4. This system graph and machine-readable goals
5. README and generated summaries
6. Historical repositories and screenshots

Status vocabulary: PROVEN, OBSERVED, NOT_PROVEN, HYPOTHESIS, PLANNED, BLOCKED, ARCHIVAL.

## System hierarchy

OmniKali
- Public discovery: omnikali, onnxscibroccoli.github.io, omnikali-link
- Production control / desktop: helix, kali-node, RDS PostgreSQL
- Reference control plane / reconstruction: Grasshopper
- Android execution / accessibility: broccoli-core, Termux, Rish, Shizuku, custom OmniKali MCP
- Kubernetes execution substrate: grasshopper-kubernetes
- Recovery / historical implementation: GPTOmniKali-full-stack
- Browser-contained alternative: kiln
- Morphe ecosystem: morphe-manager, morphe-desktop, morphe-patches, morphe-patches-1, Morphe-Patches-2, morphe-patches-template
- Research: lattice, lattice-audit
- Published applications: newsroom-desk, half-a-mile, dectalk-live
- Android experiments: shizuku-silent-mic, android-virtual-mic-shizuku, shizuku-virtual-mic
- Completed probes: ara-github-write-test, ara-github-write-test-2
- Coordination: omn-kali-knowledge-graph-master
- Direct dependency forks: noVNC, oauth2-proxy

## Repository ownership map

| Repository | Lane | Role | Current truth |
|---|---|---|---|
| Grasshopper | A | reference control plane | ACTIVE reconstruction/reference |
| helix | A | cloud/KVM control plane | ACTIVE production lineage |
| kali-node | A | persistent Kali workstation | ACTIVE integration |
| grasshopper-kubernetes | A | isolated K8s desktops | PROTOTYPE |
| omnikali | A | fail-closed public door | ACTIVE edge |
| onnxscibroccoli.github.io | A | publication/deployment surface | ACTIVE artifact |
| omnikali-link | A | legacy pointer | MAINTENANCE |
| broccoli-core | B | Android executor + historical philosophy | ACTIVE adjunct |
| GPTOmniKali-full-stack | B | recovery/provenance workspace | RECOVERY |
| kiln | B | browser-contained VM alternative | FUNCTIONAL PROTOTYPE |
| lattice | C | independent research/rules engine | INDEPENDENT |
| lattice-audit | C | public audit boundary | MAINTENANCE |
| omn-kali-knowledge-graph-master | META | coordination graph | CANONICAL INDEX |
| morphe-manager | D | Android patch manager fork | ACTIVE fork |
| morphe-desktop | D | desktop patching tool fork | ACTIVE fork |
| morphe-patches | D | Hoodle patch source fork | SOURCE REGISTRY |
| morphe-patches-1 | D | Kareem patch source fork | SOURCE REGISTRY |
| Morphe-Patches-2 | D | Alastor patch source fork | SOURCE REGISTRY |
| morphe-patches-template | D | official template fork | DEVELOPMENT TEMPLATE |
| noVNC | E | upstream dependency fork | DEPENDENCY MIRROR |
| oauth2-proxy | E | upstream auth dependency fork | DEPENDENCY MIRROR |
| shizuku-silent-mic | F | reserved Android experiment | EMPTY |
| android-virtual-mic-shizuku | F | reserved Android experiment | EMPTY |
| shizuku-virtual-mic | F | reserved Android experiment | EMPTY |
| ara-github-write-test | G | completed capability proof | ARCHIVAL |
| ara-github-write-test-2 | G | completed capability proof | ARCHIVAL |
| half-a-mile | H | published editorial application | ACTIVE |
| newsroom-desk | H | published editorial platform | ACTIVE |
| dectalk-live | H | browser/WASM speech demo | PUBLISHED |

## Critical dependencies

Production desktop:
omnikali -> CloudFront -> nginx :80 -> Helix :8092 -> libvirt/QEMU -> helix-omnikali

Separate host console:
CloudFront /novnc/vnc.html -> host websockify :6080 -> host VNC :5900

No Kubernetes ingress, FRP listener, or alternative desktop path may silently replace this chain.

Control plane:
Grasshopper -> task contracts/BIST/reproducibility -> Helix

Android:
Grasshopper MCP contract -> Android/Termux MCP -> Rish -> Android shell/UI -> installed APK

The Android executor must live where the proven Rish environment exists. A workstation process must not impersonate the phone.

Morphe:
Morphe Manager -> patch source manifest -> signed .mpp bundle -> local patching -> Android install

A source is not verified merely because its repository exists. Verification requires source metadata, release/signature evidence where applicable, compatible target evidence, and runtime confirmation in Morphe.

## Current proven knowledge

- Android API 35 and Rish shell access are proven.
- Rish returned uid=2000(shell) and SDK 35.
- The known-good Rish wrapper works with RISH_PRESERVE_ENV=0.
- Android-native OmniKali MCP exists with authenticated, fail-closed control tools.
- MCP supervisor recovery on Android was live-tested: MCP termination -> supervisor recreation -> fresh MCP initialize, while the Broccoli runtime remained alive.
- APK-first application inspection and semantic UI automation contracts are implemented.
- Morphe app catalog and UI snapshot have been observed.
- Morphe source confirmation/installation remains NOT_PROVEN.
- Grasshopper has the control-plane, BIST, reconstruction, and provider-neutral substrate work.
- The live Helix production path remains the protected reference.
- The Grasshopper workstation is storage constrained at roughly 87% root usage and persistent build storage has not yet been attached.
- Grasshopper source builds are NOT_READY because Java was absent during the last check.
- Direct dependency forks now exist for Morphe Manager, Morphe Desktop, Morphe patch sources/template, noVNC, and oauth2-proxy.

## Known failure lessons

1. Do not treat README text or issue titles as proof.
2. Do not treat RC=0 with empty output as execution success.
3. Do not repair a proven lower transport layer to compensate for a caller-boundary failure.
4. Do not collapse host-console VNC and guest desktop RFB into one path.
5. Do not bind prototype ingress to production 80/443.
6. Do not call a Morphe source installed until the confirmation UI is observed.
7. Do not start heavy source builds on the 87%-full Grasshopper root disk.
8. Do not weaken permissions merely to make an automation path convenient.
9. Do not copy Broccoli's historical script pile into Grasshopper.
10. Do not claim Android process survival as guaranteed; supervisor recovery is bounded best-effort.

## Missing edges

- Fresh authenticated production browser acceptance
- Full eight-scenario live acceptance
- Clean-host reconstruction proof
- Machine-readable BIST merge gate
- Android MCP end-to-end observe/select/act/verify on a real installed app
- Morphe source confirmation and post-install verification
- Grasshopper persistent storage provisioning
- JDK 21 and Android build prerequisites on Grasshopper
- Source-build acceptance for Morphe where feasible
- Off-host recovery / backup retention gate
- Node 24 self-hosted runner verification
- Second executor and second substrate after earlier gates

## Agent rule

Every material change moves through:
inspect -> establish provenance -> choose owner -> smallest change -> narrow test -> acceptance -> evidence -> graph update

When ownership is ambiguous, resolve ownership before implementing a second copy.

When evidence is missing, record NOT_PROVEN; never promote by optimism.
