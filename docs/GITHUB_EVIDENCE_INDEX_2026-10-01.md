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

