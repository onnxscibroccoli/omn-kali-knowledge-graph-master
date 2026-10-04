# Paperclip incident and migration record

Date: 2026-10-04

Status: OBSERVED recovery, PLANNED migration

## Canonical incident

The Helix production KVM host experienced resource exhaustion while running both the persistent Kali desktop and Paperclip.

The host was a c7i-flex.large with approximately 3.7 GiB RAM and approximately 1 physical core / 2 threads.

During recovery evidence:

- QEMU for helix-omnikali was approximately 93 percent CPU and approximately 1.7 GiB RSS.
- Paperclip was approximately 38 percent CPU and approximately 412 MiB RSS.
- The Kali guest process snapshot did not identify a runaway guest process.
- After Paperclip was stopped and disabled, QEMU settled near approximately 23.5 percent CPU in the captured sample and approximately 990 MiB memory was available.
- External checks returned HTTP 200 for /health, /auth/login, and /novnc/vnc.html.

The immediate production recovery is therefore PROVEN at the availability level.

## Architectural conclusion

Paperclip belongs outside the Helix workstation runtime.

Current protected path:

CloudFront -> nginx :80 -> Helix :8092 -> libvirt/QEMU -> helix-omnikali

Required future path:

Grasshopper/evidence
-> Paperclip isolated worker
-> authenticated Helix task API
-> workstation worker
-> persistent guest

Paperclip must not share unrestricted host resources with QEMU.

## Cross-repository ownership

Helix:
production KVM desktop lifecycle and guest runtime.

Grasshopper:
orchestration contracts, BIST, evidence, reconstruction, and architecture coordination.

kali-node:
Paperclip integration keeper and workstation-side boundary.

Knowledge graph:
cross-repository provenance, status, and synchronization record.

## Migration phases

1. Contain: Paperclip remains stopped and disabled on the production KVM host.
2. Inventory: record service, configuration, ports, data, credentials, dependencies, logs, and resource profile.
3. Isolate: provision a dedicated worker with explicit CPU and memory limits.
4. Integrate: use the authenticated Helix task API. Do not add a second task state machine.
5. Validate: fixture, shadow, duplicate, cancellation, timeout, and resource tests.
6. Accept: one authenticated production end-to-end run with an evidence ID.
7. Remove: delete the old host placement and install drift detection.

## Evidence vocabulary

PROVEN:
Recovery and the effectiveness of Paperclip containment.

OBSERVED:
Paperclip resource usage during the incident.

PLANNED:
Dedicated worker, resource enforcement, API contract integration, and drift detection.

NOT_PROVEN:
Final worker capacity and production cutover.

## Graph synchronization requirement

The graph must not mark Paperclip production integration as PASS merely because a service exists or a repository contains integration code.

A production PASS requires fresh live acceptance evidence.

The narrative record is complementary to machine-readable graph data and existing contracts. It does not replace them.
