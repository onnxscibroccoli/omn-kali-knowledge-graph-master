# CI/CD

Workflow: `.github/workflows/refresh.yml`

## Current behavior

- Manual `workflow_dispatch`
- Weekly cron `0 2 * * 1`
- Installs `scripts/requirements.txt`
- Runs `scripts/validate_schema.py`
- Runs `scripts/crawl_omnikali.py` against `onnxscibroccoli`
- Uploads inventory artifact
- Does **not** auto-commit graph mutations
- Does **not** write back to sibling repos

Unreviewed machine edits to architectural memory create split-brain documentation.

## Universal goals self-test

`.github/workflows/universal-goals.yml` runs on PRs, main pushes and manual dispatch.
It runs unittest, structural/semantic goal validation, generated-view drift detection,
and the existing repository schema check. Permissions are read-only. It neither
imports private inventories nor performs deployment or automatic merges.
