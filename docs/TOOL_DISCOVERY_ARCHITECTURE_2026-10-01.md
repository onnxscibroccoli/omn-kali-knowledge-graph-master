# Repository Tool Discovery Architecture Note

Date: 2026-10-01

## Decision

The repository-wide tool discovery system begins as a read-only catalog.

It discovers candidate tools and records provenance, interface signals, ownership, and evidence state. It does not execute tools, grant capability, become a scheduler, or replace an existing control plane.

## Ownership boundary

Grasshopper remains the reference control plane and domain contract authority.

Helix remains the protected production desktop lifecycle owner.

Kali Node remains the workstation-side implementation.

Broccoli Core remains the Android and Termux automation lineage and keeps the proven Rish transport as its execution boundary.

Provider-specific infrastructure code remains responsible for provider resources.

Ansible can own host convergence when an explicit adapter assigns that responsibility. It must not own desired state for Grasshopper resources, Helix desktop lifecycle, or Android execution.

## Current Ansible evaluation

The 2026-10-01 kali-node repository tree was inspected at commit 39b1cd6e77a751ab7d23471ff00f64da99744047.

No Ansible playbook, inventory, or Ansible-specific path was found in that snapshot.

The current Grasshopper tree was inspected at commit a0423ee40287506843faff9b24989a1a37217441.

Grasshopper already contains provider-specific Terraform infrastructure and multiple explicit bootstrap and verification scripts. This means Ansible is not required to establish the current infrastructure boundary.

The appropriate next evaluation is comparative rather than invasive: determine whether repeated host-convergence logic has become large enough to justify Ansible roles. Do not introduce Ansible merely to wrap existing shell scripts.

## Temporal evaluation

Temporal is an integration candidate for durable long-running workflows. It is not part of the discovery layer.

The discovery system should expose workflow entrypoints as metadata when they already exist. It must not create a second workflow engine or silently replace Grasshopper's durable task and recovery contracts.

Any Temporal adoption requires a separate architecture decision covering ownership, state authority, deployment topology, failure recovery, and migration evidence.

## Nushell evaluation

Nushell is an optional operator and scripting tool candidate. It is not a prerequisite for discovery.

The discovery engine deliberately uses Python standard-library parsing and does not require a new shell runtime. Existing Broccoli and Android execution contracts remain unchanged.

A future Nushell adoption must be evaluated at individual script boundaries and cannot replace the proven Rish transport.

## Discovery contract

A discovered tool is a description, not an authorization.

Every manifest records a source reference and source SHA. Runtime evidence defaults to NOT_PROVEN.

The registry is generated data and must never outrank executable acceptance evidence or the owning control-plane contract. Qualification adds a second evidence layer: explicit live retests can promote a candidate to HIGH, while historical proof without retest remains HISTORICAL_RETEST_REQUIRED.

## First implementation

The first implementation consists of:

- tools/discovery/tool_manifest.schema.json
- tools/discovery/discovery_engine.py
- tools/discovery/tool_registry.json
- tools/discovery/discovery_scope.json
- tools/discovery/validate_registry.py
- tools/discovery/render_narrative.py
- tools/discovery/README.md
- .github/workflows/tool-discovery.yml

The scanner is intentionally read-only and conservative. False negatives are preferable to inventing executable capabilities.

## Verification status

GitHub Actions run `36953078467` completed successfully on 2026-10-02 against the final branch head. It discovered 3,224 candidates across 21 public repositories, recorded 8 private repositories as NOT_SCANNED, indexed Git history, passed both registry and retest-evidence schema validation, qualified the catalog, rendered the plain-text narrative, and uploaded the generated evidence artifact.

The repository-wide discovery and qualification gate is PASS for this snapshot. Three tools have HIGH quality based on explicit live retests. One historically proven Broccoli transport tool remains HISTORICAL_RETEST_REQUIRED because an Android/Termux retest device is not currently connected. Local container runtime validation remains NOT_PROVEN. Private repository discovery remains NOT_SCANNED until a separately authorized credential boundary exists.

## Next gate

Review the generated catalog for false positives and sensitive-path noise before any downstream consumer is allowed to treat a discovered candidate as operationally useful.

No production routing should consume the registry until that review and an explicit ownership decision are complete.
