# OmniKali Knowledge Graph Master

**Current system graph:** OMNIKALI-SYSTEM-KG-2026-10-01
**Current goals graph:** OMNIKALI-SYSTEM-GOALS-2026-10-01
**Current Broccoli transport contract:** BROCCOLI-TRANSPORT-CONTRACT-2026-10-01
**Current documentation audit:** docs/REPOSITORY_DOCUMENTATION_AUDIT_2026-10-01.md
**Current dependency narrative:** docs/OMNIKALI_SYSTEM_DEPENDENCY_NARRATIVE_2026-10-01.txt
**Historical graph:** OMNIKALI-KG-2026-09-28
**Owner account:** onnxscibroccoli

This is the centralized research and coordination graph for the OmniKali repository family.

The 2026-10-01 system graph is now the current coordination point. Historical graphs remain evidence and are not rewritten.

The dependency narrative is a companion text representation of the current system graph. It exists for human reading, text to speech, agent orientation, and narrative architecture review. It does not replace the machine readable graph, goals, contracts, or evidence documents.

## Physical Android launcher

Read [the current physical transport policy](docs/PHYSICAL_ANDROID_TRANSPORT_2026-10-07.md) before dated transport records. Use broccoli-core `lib/rish_run.sh`; `bin/broccoli-rish` delegates to it. Remote Android transports remain explicitly configurable.

## Start here

1. docs/OMNIKALI_SYSTEM_KNOWLEDGE_GRAPH_2026-10-01.md
2. docs/OMNIKALI_SYSTEM_GOALS_GRAPH_2026-10-01.md
3. docs/OMNIKALI_SYSTEM_DEPENDENCY_NARRATIVE_2026-10-01.txt
4. docs/BROCCOLI_ITERATION_KNOWLEDGE_2026-10-01.md
5. docs/BROCCOLI_TRANSPORT_CONTRACT_2026-10-01.md
6. goals/broccoli-transport-preflight-2026-10-01.yml
7. docs/REPOSITORY_DOCUMENTATION_AUDIT_2026-10-01.md
8. docs/ORCHESTRATOR_CHARTER.md
9. docs/RELEASE_READINESS_2026-09-29.md
10. goals/production-backlog.yml
11. Grasshopper program issue: https://github.com/onnxscibroccoli/Grasshopper/issues/65

## Authority order

1. Fresh live acceptance evidence and runtime behavior
2. Production contracts and acceptance artifacts
3. Verified source implementation
4. Current system graph and goals graph
5. README and generated summaries
6. Historical/recovery material

A README is never stronger evidence than an executable acceptance test.

## Operating rule

Work the goals graph in dependency order. Preserve the validated Helix production path. Keep Android execution beside the proven Rish transport. Before any new Rish experiment, answer `goals/broccoli-transport-preflight-2026-10-01.yml`. Treat Morphe source verification and source builds as separate runtime/build gates. Record missing proof as NOT_PROVEN instead of promoting it by documentation.

Mass graph markers in production repositories remain gated. Use per-repository graph updates only when the repository is materially changed.
