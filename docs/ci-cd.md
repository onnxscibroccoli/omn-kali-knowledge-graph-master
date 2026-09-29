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
