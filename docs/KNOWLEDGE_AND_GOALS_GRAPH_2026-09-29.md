# OmniKali Knowledge and Goals Graph

**Timestamp:** 2026-09-29 13:58 EDT  
**Owner:** `onnxscibroccoli`  
**Canonical repo:** `onnxscibroccoli/omn-kali-knowledge-graph-master`  
**Graph tag:** `OMNIKALI-KG-2026-09-29-GOALS`  
**Production program issue:** https://github.com/onnxscibroccoli/Grasshopper/issues/65  
**Existing contract:** `Grasshopper/docs/TRANSCENDENTAL_ARCHITECTURE_WORKSTREAM_2026-09-29.md`

This file is an index. It does not replace live acceptance evidence.

## How to use this file

1. Treat the validated Helix production path as the protected core.
2. Use status tags exactly: `PROVEN`, `OBSERVED`, `HYPOTHESIS`, `PLANNED`.
3. Work the next-step queue in order. Do not skip a gate by renaming a prototype.
4. After any material change, update this file, `goals/production-backlog.yml`, and the owning repo `.omnikali` snapshot.

## Facts / assumptions / recommendations

### Facts

- Authenticated GitHub account is `onnxscibroccoli` (21 repos visible to this connector on 2026-09-29).
- Validated production reference remains: CloudFront -> nginx `:80` -> Helix `:8092` -> libvirt/QEMU -> `helix-omnikali`.
- Intentional hypervisor console remains: CloudFront `/novnc/vnc.html` -> host websockify `:6080` -> Debian host VNC `:5900`.
- Grasshopper already defines the architecture program and BIST script (`npm run bist`).
- Grasshopper #62 records that K3s Traefik on 80/443 broke production CloudFront. Public ingress controllers on the production host are forbidden without before/after acceptance.
- Clean-host reconstruction, fresh authenticated desktop acceptance, 14-day backup retention, and Node 24 runner upgrade remain open gates.
- AWS rejected RDS `BackupRetentionPeriod=14` with `FreeTierRestrictionError`.

### Assumptions

- Gemini market-size and acquisition-premium language is a valuation thesis, not measured revenue.
- Lambda-calculus alignment is a research metaphor until a typed intent IR exists in code.
- ContextSwitchAI / ContextWizard is a named direction, not a repo under this account.
- Kubernetes desktop path is a prototype on the same EC2 host, not the public origin.

### Recommendations

- Freeze the proven core. Build reproducibility and BIST around it. Generalize last.
- Keep identity, ingress, execution, and memory as separate contracts.
- Bind raw VNC/RFB to loopback or ClusterIP only. Terminate TLS at the edge.
- Do not claim $1B valuation readiness until Gate B and Gate C are proven and at least one design-partner workload exists.

## System map

- Intent/memory: broccoli-core, omn-kali-knowledge-graph-master
- Control plane: Grasshopper
- Execution/desktop: helix, kali-node, grasshopper-kubernetes (prototype), kiln (not Kali path)
- Public edge: omnikali, omnikali-link
- Adjacent value: lattice, lattice-audit
- Edge clients: shizuku-*

Authority order: live acceptance > Grasshopper contracts > Helix implementation > kali-node > grasshopper-kubernetes > this graph.

## Ideas 1-13 compressed to executable goals

1. Terminal-agnostic compute — PLANNED. Same signed task contract on two terminals. Next: Grasshopper `src/clients/` plus one non-browser client. Do not install Traefik on 80/443.
2. Autonomous reproducibility — PLANNED. Next: `npm run verify:clean-host-dryrun` evidence bundle. No production secrets in git.
3. Self-repair / vuln arbitrage — PLANNED. Recovery OBSERVED. Next: bind live-acceptance scenarios to BIST codes. Fuzzing isolated from production IAM.
4. Semantic alignment — HYPOTHESIS. Next: intent/evidence schema on Grasshopper export. Broccoli #49. Do not rewrite Helix for a calculus.
5. Autonomous infrastructure — PLANNED. Next: document remaining Helix manual host steps. Keep `/novnc` hypervisor access.
6. BIST — script OBSERVED, live five-phase PLANNED. Next: machine-readable JSON from `npm run bist`.
7. Grasshopper / grasshopper-kubernetes — K8s is not public origin. Next: real Guacamole/VNC on non-conflicting ingress. Issues #64 and k8s #1.
8. Multi-cloud — PLANNED after Gate B. AWS is the only OBSERVED provider. Do not drop PostgreSQL.
9. Sub-bot swarms — PLANNED after ownership collisions resolved. Helix RFB != Guacamole path.
10. Persistent ingress/identity — CloudFront path OBSERVED. Next: Helix #21 authenticated guest WSS. VNC on loopback/ClusterIP only.
11. Local memory layer — PLANNED on Lane B (broccoli-core M1-M9). Conversation index is not source of truth.
12. Containerized fuzzing — PLANNED after NetworkPolicy isolation. No CloudFront attachment.
13. IP portfolio — see README lanes A-E. Lattice remains Lane B / HYPOTHESIS for product coupling.

## Gates A-H

A Proven core OBSERVED. B Clean reconstruction OPEN. C Machine-readable BIST PARTIAL. D Bounded self-repair OPEN. E Terminal independence OPEN. F Second executor OPEN. G Second substrate OPEN. H Autonomous operations OPEN.

Work left to right. Skipping B or C is a regression.

## Immediate queue

1. Protect base system. Grasshopper #62 binding.
2. Fresh authenticated guest desktop. Helix #21.
3. Machine-readable BIST JSON. Grasshopper #65.
4. Clean-host dry-run evidence. Grasshopper reproducibility scripts.
5. Real Guacamole/VNC off production 80/443. grasshopper-kubernetes #1, Grasshopper #64.
6. Independent backup or billing capability. Grasshopper #13 / #26.
7. Node 24 runner. Helix #13.
8. Only then: second terminal, second executor, fuzz namespace, Lattice coupling.

## Agent operating rule

If two repositories appear to own the same desktop path, stop. Helix guest RFB and Kubernetes Guacamole are different products until an acceptance test says they are equivalent.
