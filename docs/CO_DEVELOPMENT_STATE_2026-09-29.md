# OmniKali co-development state

The graph remains the orchestration authority for Lane A.

Current protected reference:

CloudFront -> nginx :80 -> Helix :8092 -> libvirt/QEMU -> helix-omnikali

Lane A development branches created for this pass:

- helix: codex/co-dev-20260929
- Grasshopper: codex/co-dev-20260929
- kali-node: codex/co-dev-20260929
- grasshopper-kubernetes: codex/co-dev-20260929
- kiln: codex/co-dev-20260929
- omnikali: codex/co-dev-20260929
- omnikali-link: codex/co-dev-20260929
- GPTOmniKali-full-stack: codex/co-dev-20260929
- graph: codex/co-dev-20260929

This pass is non-production. No 80/443 changes, CloudFront cutover, production credential changes, RDS retention changes, or backup-runner changes are authorized by the branch set.

## Current implementation lanes

- Grasshopper: C0 BIST contract.
- Helix: read-only public health verification.
- kali-node: AWS/CloudFront, Paperclip, and Go dispatcher keepers.
- grasshopper-kubernetes: isolated real-browser Guacamole acceptance remains the target; existing PR #2 is the implementation candidate.
- kiln: emulator/native remote-desktop boundary.
- omnikali: fail-closed endpoint-record validation.
- omnikali-link: legacy pointer boundary.
- GPTOmniKali-full-stack: recovery/reconstruction boundary.

Every live claim still requires fresh evidence.
