# GitHub evidence index

## Evidence status

IMPLEMENTED in Grasshopper.

Historical precedent also exists in broccoli-core:
- \`Agent/Broccoli/meta/github_repo\`
- \`Agent/Broccoli/pull/*/broccoli/meta/github_repo\`
- repository inventories and manifests
- \`BroccoliWorkspaceBackup\` containing harvested data and archive indexes

The old implementation was operationally useful but mixed evidence, backups, and runtime artifacts. The new tool deliberately separates:
1. remote source;
2. local evidence index;
3. knowledge-graph conclusions.

## Why this matters

The knowledge graph must answer "where did we learn this?" without loading an entire repository into context.

For a repository, the minimum provenance chain is:

\`GitHub -> repository -> commit -> path -> blob SHA -> indexed excerpt -> graph fact\`

For a conversation:

\`provider -> account -> conversation -> message -> source page -> graph fact\`

The two chains can converge at a graph fact while retaining independent provenance.

## Multi-gigabyte rule

Do not use a full clone merely to search architecture.

Use partial clone, tree listing, path classification, and bounded blob retrieval first. Full materialization is reserved for a task that actually requires the complete working tree.

## Protected-data rule

Repository metadata and path names may themselves reveal sensitive information. Secret-looking files are excluded from text indexing by default. Credentials must never be copied into the graph.

## Current live corpus

The OCI \`oci-grasshopper-workstation\` is the preferred persistent development-side workspace for building this index. It is not production state.

## Live validation: 2026-10-01

Grasshopper PR #120 makes the ingest path API-first and concurrency-safe.

Observed on OCI workstation `oci-grasshopper-workstation`:

- source: GitHub Trees API
- repository: `onnxscibroccoli/broccoli-core`
- historical commit: `e8eff124000e8bfb0a9419281d065a493d880cc5`
- tree entries indexed: 5,481
- bounded text files indexed: 20
- protected paths excluded: 3
- recursive tree truncated: false
- selected raw file bytes verified against exact Git blob SHA before indexing
- SQLite status persisted with `status=OK`
- FTS query `chat` returned exact repository/path evidence
- a second worker attempting the same repository lock was rejected with `repository ingest already running`
- clean rerun completed successfully in about 3 seconds

### Learned failure boundary

The earlier Git partial-clone implementation was tested against the same historical repository. It exposed repeated promisor fetches while `git ls-tree` and lazy blob access were operating on the partial clone. That behavior is now treated as a documented fallback limitation, not as proof that the original path is bounded.

The API-first path avoids that observed behavior for public repositories by obtaining commit/tree metadata directly and retrieving only selected high-signal files. Git remains an explicit fallback. `OMNIKALI_GITHUB_API_ONLY=1` provides fail-closed validation when fallback must not occur.

### Concurrency contract

One index root permits one active ingest worker per repository. The lock is an OS-level advisory file lock under `<index-root>/locks/`. Lock ownership is released automatically when the process exits, including abnormal process termination.

