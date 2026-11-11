# Portfolio reviewer readiness — omn-kali-knowledge-graph-master

**Focus:** Cross-repository source ownership and dependency knowledge graph  
**Current evidence status:** `GRAPH_REFRESH_CI_EXECUTED` (2026-11-11 snapshot; **not** production approval).  
**Tracking:** [repository issue](https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/issues/15) · [portfolio master ledger](https://github.com/onnxscibroccoli/broccoli-core/issues/102)  


## Inspect actual source
- [docs/OMNIKALI_SYSTEM_KNOWLEDGE_GRAPH_2026-10-01.md](https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/blob/main/docs/OMNIKALI_SYSTEM_KNOWLEDGE_GRAPH_2026-10-01.md)
- [goals/production-backlog.yml](https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/blob/main/goals/production-backlog.yml)
- [README.md](https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/blob/main/README.md)

**Scoped reference workflow run:** [Inspect the historical GitHub Actions result](https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/actions/runs/43029344795). Verify its SHA/branch before attributing it to current source; CI success is not live/production evidence.
Recorded 2026-11-11: run 43029344795 is `refresh-graph` (`workflow_dispatch`) at `main` `ded4da9decb92fde91180515c484f3cc4faa8a67`, which is the current `main` head; conclusion success. It covers schema validation, candidate ranking and a public-inventory crawl, with permissions `contents: read`. It has no `pull_request` trigger, so readiness PRs carry no CI check.

## First reviewer command (check prerequisites before executing)

```sh
python3 -m compileall -q scripts
```

This is a proposed reproduction command, **not a claim of executed testing**. Confirm the command exists in the current repository; record missing scripts/dependencies as NOT_VERIFIED rather than masking failures.

## Ordered implementation queue

1. [ ] Publish dated source-of-truth dependency map and practical reviewer navigation.
2. [ ] Validate every linked public repository and canonical capability owner.
3. [ ] Make PRIVATE/NOT_PROVEN markers first-class rather than inferred success.
4. [ ] Add an automated freshness check that preserves historical graph records.

## Evidence promotion gate

A project is not ready for a public professional demonstration merely because it has a README, an Actions schedule, or a test result unrelated to its claimed behavior. Provide exact source SHA, real test scope, negative controls, and meaningful limitations. Production or hardware assertions require an authorized real environment and appropriately scoped acceptance.

## Safe resumption

Inspect this issue and the master ledger, refresh the repo's `main` head and relevant PRs, implement the first unchecked item on a draft PR, attach exact test evidence and update the tracker. Avoid mass merging, secret exposure, false human review, and speculative employment claims.
