# OmniKali Knowledge Graph Master

**Repository:** `onnxscibroccoli/omn-kali-knowledge-graph-master`  
**Graph tag:** `OMNIKALI-KG-2026-09-28`  
**Release tag:** `omn-kali-kg-v2026-09-28`  
**Snapshot:** 2026-09-28 EDT  
**Owner account:** `onnxscibroccoli` (user, not an organization)

This is the centralized research and coordination graph for the OmniKali repository family.

It does **not** replace live acceptance evidence. It is an index: ownership, state, dependencies, candidate tools, and the agent workflow.

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

## What this repo contains

| Path | Purpose |
|---|---|
| `omnikali/` | One metadata file per OmniKali repo |
| `external/` | Candidate external OSS tools, ranked and tagged |
| `graph/` | Mermaid diagrams for hierarchy and orchestration |
| `scripts/` | Crawl, registry search, ranking, schema validation |
| `docs/` | Schema spec, search queries, CI, write-back protocol |
| `inventory/` | Point-in-time GitHub inventory snapshot |

## Source-of-truth hierarchy (current consolidation)

```text
historical experiments
      |
      v
validated production behavior
      |
      v
Grasshopper contracts + evidence
      |
      v
Helix control plane
      |
      +--> persistent real Kali workstation (kali-node)
      |
      +--> scalable Kubernetes desktop platform (grasshopper-kubernetes)
      |
      v
OmniKali public discovery / agent access
```

## Distinctions that must not be collapsed

- QEMU running != desktop usable
- Kubernetes pod Running != remote desktop working
- HTTP health != authenticated session working
- Authenticated API access != RFB/WebSocket desktop access
- Fixture/unit test passing != live infrastructure acceptance
- Historical code existing != current production capability
- A repository name != an implemented feature
- A browser emulator workstation != the persistent Kali KVM workstation

## Status tags

Every claim in this graph is one of:

- `PROVEN` - backed by named test, commit, acceptance ID, or evidence document
- `OBSERVED` - seen in the wild, not yet explained or re-verified
- `HYPOTHESIS` - plausible, unverified
- `PLANNED` - intended work, not current capability

Never promote a hypothesis to a proven fact.

## How future agents should use this repo

1. Read this README and `docs/orchestration-loop.md`
2. Identify the owning repository in `omnikali/`
3. Traverse dependencies before changing code
4. Check existing proof
5. Create a restore point
6. Apply the smallest change
7. Run static/unit tests, then authorized live acceptance
8. Verify the user-visible boundary
9. Document evidence
10. Update this graph and affected per-repo `.omnikali` files

## Local commands

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate_schema.py
python3 scripts/crawl_omnikali.py --owner onnxscibroccoli --out inventory/
```

## Write-back policy

Mass tagging every OmniKali repository is gated. This master repo is the first restore point.

See `docs/write-back.md`. Do not push tags or README markers into production repos until that protocol is explicitly approved.

## Existing per-repo graphs

- `onnxscibroccoli/helix/.omnikali/PROJECT_KNOWLEDGE_GRAPH.md`
- `onnxscibroccoli/Grasshopper/.omnikali/project-knowledge-graph.md`
- `onnxscibroccoli/omnikali/.omnikali/PROJECT_KNOWLEDGE_GRAPH.md`

## Facts vs assumptions in this snapshot

**Facts**

- Authenticated GitHub user is `onnxscibroccoli`
- 20 repositories exist under that user as of 2026-09-29T03:25Z
- No prior knowledge-graph / kg-master repository existed
- Helix and Grasshopper already carry graph tag `OMNIKALI-KG-2026-09-28`

**Assumptions**

- Candidate external tools in `external/` are domain-relevant, not proven integrations
- GitHub Dependency Graph may be unavailable or incomplete for private repos

**Out of scope for v2026-09-28**

- Automatic tagging of every sibling repo
- SBOM generation against private production hosts
- Claiming live production health without re-running acceptance
