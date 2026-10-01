
# Repository Documentation Audit

**Date:** 2026-10-01 EDT
**Scope:** all 29 repositories visible to the linked onnxscibroccoli GitHub account.

## Findings

The repositories divide into five operational groups.

### OmniKali execution system

Grasshopper, helix, kali-node, grasshopper-kubernetes, omnikali, onnxscibroccoli.github.io, omnikali-link, broccoli-core, GPTOmniKali-full-stack, omn-kali-knowledge-graph-master.

### Morphe and direct dependencies

morphe-manager, morphe-desktop, morphe-patches, morphe-patches-1, Morphe-Patches-2, morphe-patches-template, noVNC, oauth2-proxy.

### Adjacent products

kiln, lattice, lattice-audit.

### Published applications

half-a-mile, newsroom-desk, dectalk-live, onnxscibroccoli.github.io.

### Reserved experiments and completed probes

shizuku-silent-mic, android-virtual-mic-shizuku, shizuku-virtual-mic, ara-github-write-test, ara-github-write-test-2.

## Documentation drift

1. The old master graph is a useful historical snapshot but its repository inventory is stale.
2. Several repositories still point at the older OMNIKALI-KG-2026-09-28 marker.
3. Grasshopper contains the most current cross-project implementation philosophy, while the master graph remains the better coordination index.
4. Some expected documentation paths are missing from current branches. This is evidence of documentation drift, not permission to invent replacement content.
5. README claims are generally careful about prototype versus production boundaries and should remain so.
6. Morphe forks contain source/build instructions, but source verification is a runtime problem.
7. Empty Shizuku repositories are correctly documented as empty and should remain low priority unless explicitly activated.
8. Duplicate Morphe patch repositories are distinct source lineages and must keep source-specific trust labels.

## Active implementation clusters

### Android agent execution
Grasshopper PR #115 and broccoli-core PR #62 form one capability. The executor belongs beside proven Rish on Android. The next gate is real observe/select/act/verify against an installed APK.

### Production reconstruction
Grasshopper PR #61 and the Helix production lineage form one capability. The production architecture remains frozen until fresh browser acceptance proves a replacement.

### Portable infrastructure
Helix PR #55 and #56 establish provider-neutral OCI sandbox boundaries. They are development infrastructure, not production migration.

### Morphe source/build
The account now contains Morphe Manager/Desktop and multiple patch-source forks. The Grasshopper host lacks JDK/storage prerequisites for source builds.

### Documentation
The new 2026-10-01 graph is the coordination point. Old graph tags remain historical.

## Current high-value open work

- Grasshopper #115: Android MCP
- Grasshopper #61: full AWS remote desktop reproducibility
- Grasshopper #89: verifier handling of install artifacts
- Helix #56: OCI sandbox IaC
- Helix #55: provider-neutral sandbox
- Helix #53/#52: agent authority isolation
- Helix #41/#39: workspace lifecycle and chat-independent session launch
- Helix #33: graduated self-healing
- broccoli-core #62: Android MCP supervisor
- broccoli-core #55/#54/#53: offline memory/vector work

## Agent execution decision

The account does not need another parallel architecture. It needs dependency-ordered execution with continuous evidence updates.

The next work should therefore follow the new goals graph, with small verified changes and explicit NOT_PROVEN states.
