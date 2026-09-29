# OmniKali Knowledge Graph Master

**Repository:** `onnxscibroccoli/omn-kali-knowledge-graph-master`  
**Graph tag:** `OMNIKALI-KG-2026-09-28`  
**Goals tag:** `OMNIKALI-KG-2026-09-29-GOALS`  
**Release tag:** `omn-kali-kg-v2026-09-28`  
**Owner account:** `onnxscibroccoli` (user, not an organization)

This is the centralized research and coordination graph for the OmniKali repository family.

It does **not** replace live acceptance evidence. It is an index: ownership, state, dependencies, candidate tools, goals, and the agent workflow.

## Authority order

1. Live acceptance evidence and production runtime behavior
2. Grasshopper production contracts and evidence documents
3. Helix production implementation and infrastructure
4. kali-node validated workstation implementation
5. grasshopper-kubernetes validated Kubernetes implementation
6. This master graph and per-repo `.omnikali` snapshots
7. Historical / recovery repositories
8. README descriptions and generated summaries

A README is never stronger evidence than an executable acceptance test.

## Start here for production work

1. `docs/ORCHESTRATOR_CHARTER.md` — what an agent may and may not touch
2. `docs/RELEASE_READINESS_2026-09-29.md` — open production gates
3. `docs/KNOWLEDGE_AND_GOALS_GRAPH_2026-09-29.md` — transcendental ideas mapped to repos
4. `goals/production-backlog.yml` — machine-readable next steps
5. `graph/knowledge.mmd` and `graph/goals.mmd`
6. Grasshopper program issue: https://github.com/onnxscibroccoli/Grasshopper/issues/65

Sequence is fixed: **validated core → hardening → reproducibility → BIST → bounded self-repair → terminal independence → controlled generalization**.

## What this repo contains

| Path | Purpose |
|---|---|
| `omnikali/` | One metadata file per OmniKali repo |
| `external/` | Candidate external OSS tools, ranked and tagged |
| `graph/` | Mermaid diagrams for hierarchy, orchestration, knowledge, goals |
| `goals/` | Production backlog and gate status |
| `scripts/` | Crawl, registry search, ranking, schema validation |
| `docs/` | Schema spec, search queries, CI, write-back protocol, goals graph |
| `inventory/` | Point-in-time GitHub inventory snapshot |

## Distinctions that must not be collapsed

- QEMU running != desktop usable
- Kubernetes pod Running != remote desktop working
- HTTP health != authenticated session working
- Authenticated API access != RFB/WebSocket desktop access
- Fixture/unit test passing != live infrastructure acceptance
- Historical code existing != current production capability
- A repository name != an implemented feature
- A browser emulator workstation != the persistent Kali KVM workstation
- Helix guest RFB path != Kubernetes Guacamole path

## Status tags

Every claim in this graph is one of:

- `PROVEN` - backed by named test, commit, acceptance ID, or evidence document
- `OBSERVED` - seen in the wild, not yet explained or re-verified
- `HYPOTHESIS` - plausible, unverified
- `PLANNED` - intended work, not current capability

Never promote a hypothesis to a proven fact.

## Write-back policy

Mass tagging every OmniKali repository is gated. This master repo is the first restore point.

See `docs/write-back.md`. Do not push tags or README markers into production repos until that protocol is explicitly approved.
