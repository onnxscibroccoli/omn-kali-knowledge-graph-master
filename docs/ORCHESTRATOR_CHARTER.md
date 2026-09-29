# OmniKali orchestrator charter

Accepted 2026-09-29 by operator. Orchestrator works from this graph first.

## Standing facts

- Product Kali path: `https://d22bad48irrbqe.cloudfront.net/auth/login`
- Intentional hypervisor console: `https://d22bad48irrbqe.cloudfront.net/novnc/vnc.html` → Debian host `:5900`
- Validated guest path: CloudFront → nginx → Helix :8092 → libvirt/QEMU → `helix-omnikali`
- K3s `omnikali-desktop` is a prototype on the same EC2 host, not public ingress
- Grasshopper #62: Traefik on 80/443 broke production. Do not install a public ingress controller without a before/after acceptance test

## What the orchestrator will do

1. Clean repos by lane (runtime first, satellites later).
2. Test for production readiness against the live path above, not against planned FRP/K8s ingress.
3. Continue co-development in small reviewable commits.
4. Inventory guideline-generated commentary. Do not delete it until the operator explicitly approves a listed batch.

## What the orchestrator will not do without approval

- Remove comments, disclaimers, or safety prose from code or docs
- Change the public production path (ports 80/443, CloudFront origin, Traefik, FRP)
- Archive or delete repositories
- Promote statusTag to PROVEN without a fresh acceptance ID

## Lanes

### Lane A — live runtime (first)
helix, Grasshopper, kali-node, grasshopper-kubernetes, kiln, omnikali, omnikali-link, GPTOmniKali-full-stack

### Lane B — adjacent product
broccoli-core, lattice, lattice-audit

### Lane C — content / demos
half-a-mile, newsroom-desk, dectalk-live, onnxscibroccoli.github.io

### Lane D — experiments / access tests (do not treat as production)
shizuku-virtual-mic, android-virtual-mic-shizuku, shizuku-silent-mic, ara-github-write-test, ara-github-write-test-2

### Lane E — graph itself
omn-kali-knowledge-graph-master

## Production-readiness bar (Lane A)

A repo is production-ready only if:
- README states the live path vs prototype path correctly
- CI exists and is green or explicitly waived
- Secrets are not in git
- Host vs guest desktop paths are not collapsed
- Restore/tag pointer exists (`.omnikali/MASTER_GRAPH.md`)
- Critical issues are either closed or accepted as known debt

## Commentary scrub protocol

1. Orchestrator lists candidate hunks with file, line range, why it looks guideline-generated, and risk.
2. Operator replies `approve batch N` or edits the list.
3. Only then does the orchestrator commit removals.

Until that approval, commentary stays.
