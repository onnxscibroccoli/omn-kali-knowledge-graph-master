# Write-back and tagging protocol

Mass write-back is gated because it mutates every sibling repository.

Proposed first write-back set (not executed in this snapshot):

1. helix
2. Grasshopper
3. omnikali

Disallowed without explicit approval: tagging empty Shizuku repos, tagging write-test repos as production components, force-pushing tags, auto-committing into runtime repos.

This master repository is the restore point for graph research.
