# GCP Worker Gate Evidence 2026-10-01

## Scope

This document records the next reproducibility layer for the OmniKali Grasshopper + Broccoli Core architecture.

Google Cloud Compute is treated as a persistent Linux control/evidence worker. Android remains the transport and UI boundary for Termux, Shizuku/Rish, uiautomator, Android package operations, and human-gated installation/authentication.

## Evidence

### Grasshopper

- PR #121 is merged into `main`.
- PR #122 adds the executable GCP worker bootstrap and verification gate.
- PR #122 head commit: `3ae27cf20ae51747c41944f71562c1a570f70fcf`.
- OCI checkout syntax validation: PASS.
- Focused GCP worker tests: 3/3 PASS.
- Full Grasshopper test suite: 199/199 PASS.
- GitHub reports no workflow runs or combined statuses for the PR #122 head commit. Therefore the 199/199 result is local OCI evidence, not CI evidence.

### GCP deployment safeguards implemented

- Worker bootstrap rejects an external IPv4 address.
- Private VM outbound connectivity is explicitly checked before package/source acquisition.
- Cloud NAT is documented as the controlled egress path for a VM without an external IPv4 address.
- Node.js 22.23.3 is pinned and its official release checksum is verified.
- Grasshopper and Broccoli Core refs are explicit and exact commits are recorded.
- GitHub evidence ingest is API-only during bootstrap, preventing silent fallback to the Git partial-clone path.
- Existing per-repository ingest locking remains fail-closed on concurrent invocation.
- Worker source state is recorded in a machine-readable manifest.
- Worker verification checks source state, repository commits, Grasshopper tests, Python compilation, SQLite integrity, evidence-index presence, and private-network state.

## Gate status

| Gate | Status |
|---|---|
| Reproducible bootstrap source | IMPLEMENTED |
| Architecture-aware Node bootstrap | IMPLEMENTED |
| Node artifact checksum verification | IMPLEMENTED |
| Private VM external-IP fail-closed check | IMPLEMENTED |
| GitHub egress preflight | IMPLEMENTED |
| API-only GitHub evidence ingest | IMPLEMENTED |
| Source commit manifest | IMPLEMENTED |
| Worker verification script | IMPLEMENTED |
| Regression tests | PROVEN on OCI |
| Full Grasshopper suite | PROVEN 199/199 on OCI |
| Actual GCP VM | NOT_PROVEN |
| Cloud NAT live reachability | NOT_PROVEN |
| Persistent Disk mount and reboot preservation | NOT_PROVEN |
| Clean GCP bootstrap | NOT_PROVEN |
| End-to-end GCP worker verification | NOT_PROVEN |

## Important correction

A Compute Engine VM created with `--network-interface=no-address` cannot be assumed to have outbound internet connectivity. Cloud NAT or another controlled egress path is required for public internet access. The GCP deployment documentation now makes this a prerequisite rather than an implicit assumption.

The absence of a GCP project selection means no cloud resources were mutated during this gate.

## Architectural boundary

The GCP worker does not replace the proven Android Rish transport.

Canonical Android transport remains:

`broccoli-core/lib/rish_run.sh` -> Android shell -> Shizuku/Rish -> `uiautomator`

GCP is for persistent Linux control, evidence indexing, archive/provenance work, and future Linux-safe workers.

## Next gate

After a GCP project is explicitly selected, provision only the private worker path with Cloud NAT + IAP + OS Login + Persistent Disk. Then run the repository bootstrap and reboot-preservation verification. Do not label the GCP worker production-ready until those live gates pass.
