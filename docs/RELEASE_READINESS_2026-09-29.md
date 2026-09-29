# OmniKali release readiness 2026-09-29

## Current baseline

The validated production reference remains:

CloudFront -> nginx :80 -> Helix :8092 -> libvirt/QEMU -> helix-omnikali

The intentional hypervisor console remains:

CloudFront /novnc/vnc.html -> host websockify :6080 -> Debian host VNC :5900

These paths are not interchangeable.

## Fresh verification

- CloudFront /health: HTTP 200.
- CloudFront /auth/login: HTTP 200.
- CloudFront /novnc/vnc.html: HTTP 200.
- helix-omnikali: running, persistent, autostarted.
- QEMU guest-agent: hostname kali; Kali 7.1.5+kali-amd64 kernel.
- RDS helix-control-plane: available, PostgreSQL 18.3, private, encrypted, Multi-AZ, deletion protection enabled.
- Current Grasshopper main HEAD: 6c0aa647dd5f5d68352defa5235697343826f2b1.
- Current Grasshopper test suite: 140/140 passed.
- Production readiness endpoint against CloudFront /health: HTTP 200.

## Gates that remain OPEN

1. Fresh authenticated end-to-end acceptance of the real /auth/login -> ticketed WSS -> guest desktop/task path.
2. Eight required live-acceptance scenarios: normal execution, worker termination, stale lease reclaim, replacement completion, duplicate fencing, gateway restart, database failure, and network interruption.
3. Clean-host reconstruction.
4. Fresh live Secrets Manager cutover verification.
5. Self-hosted GitHub Actions runner Node 24 verification.
6. Independent backup retention: only one verified restore point exists and RDS PITR remains at one day.
7. Optional Grok client artifact on current main is still open.

## Account-level blocker

AWS rejected an attempted RDS BackupRetentionPeriod=14 modification with FreeTierRestrictionError. The request did not modify the database.

The 14-day gate therefore requires an account/billing capability change or another explicitly authorized recovery arrangement. No architecture substitution should be made to evade the gate.

## Explicit operator intervention required

The remaining blockers cannot be honestly closed by repository edits alone:

- an authenticated browser/operator session is required for fresh production acceptance;
- AWS account capability must permit the required 14-day retention;
- GitHub self-hosted-runner administration is required to verify/upgrade the Node 24 runner if necessary.

Until those gates are satisfied, the project is not marked production-ready or PROVEN. The existing production system remains the protected reference.
