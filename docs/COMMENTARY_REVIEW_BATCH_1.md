# Commentary review batch 1

**Status: WAITING FOR OPERATOR APPROVAL. Nothing in this file has been deleted.**

Account-wide code search found **zero** classic guideline-refusal strings (`as an AI`, `I cannot assist`, `against my guidelines`, `language model`).

What exists instead is repeated agent-contract prose and a few stale architecture sentences that can confuse future agents.

## Keep unless you say otherwise

These look like project rules, not foreign safety boilerplate:

- Helix / Grasshopper / kali-node / kiln / omnikali / omnikali-link README sections titled `AI model instructions`
- Grasshopper `BASE_SYSTEM_PROTECTION.md` and incident docs
- Graph tag / restore-point paragraphs added 2026-09-28

## Batch 1 candidates (wording, not mass-delete)

Approve with `approve batch 1` to let the orchestrator apply only these edits.

1. **grasshopper-kubernetes/README.md** — architecture diagram still presents FRP/K8s as the runtime path. Should lead with “prototype / not CloudFront origin”. Risk: low. Proposed: add one warning paragraph at top; keep the intended-runtime diagram labeled TARGET.

2. **kali-node/README.md** architecture diagram starts at GitHub Pages and omits CloudFront/Helix. Risk: low. Proposed: insert CloudFront as current edge; keep Pages as discovery.

3. **helix/README.md** — already updated this pass. No further strip.

4. **Duplicated GRAPH TAG footer** on every README — useful, not guideline refuse-text. Proposed: keep.

## Not in batch 1

- Any deletion of comments inside `src/`
- Any change to `AGENTS.md` contracts
- Lane B broccoli-core milestone issue text
- Shizuku app copy

Reply `approve batch 1` or edit the list.
