# Terminal progress/status convention (Android Termux and cloud operations)

**Adopted 2026-10-12 at operator request:** all future long-running scripts should have an **npm-style live status indicator**, not appear stalled while querying services.

## Required output

- Clear initial objective, environment, authentication profile **name only** (never print credentials), and read-only vs mutating status.
- Interactive terminal: one updating line with **spinner + bar + completed/total stages + % + current operation + elapsed time**, for example:
  `OCI / [##########..........] 50% 6/12 19s API:5 OK:4 EMPTY:1 WARN:0 Inspect volumes`.
- Non-TTY output/CI: stable newline-delimited `STATUS [n/total] task`, followed by `PASS`, `EMPTY`, `WARN`, `FAIL` for reliable logs and screen readers.
- **Percent is measured stages completed**, not guessed time remaining or resource discovery percentage; stage names should communicate active work.
- Print counts of actual API attempts, results, confirmed-empty responses, unverified silent responses, warnings/failures.
- Provide **final summary and private report path**, with explicit `COMPLETE`, `PARTIAL`, or `BLOCKED`, and whether changes occurred.
- For live OCI list CLI: `exit=0 + empty stdout` can mean an empty `[]` result because the CLI's `render()` skips falsey data. Show this as `POSSIBLY_EMPTY` until independently checked. Do not label it a service error or a guaranteed verified empty list.
- Process and command timeouts, interrupt handling, no silent long-running tasks. Print statuses without token contents, secrets, or full private OCI resource IDs.
- Persistent logs should be scrubbed of access tokens, OAuth callbacks, private keys, and personal data before any public GitHub commit.

## Current model

`termux_oci_reconcile_progress.sh`: 12 tracked steps, live spinner and progress bar, API counters, and SDK spot-checks of empty tenancy-root compute/VCN and Grasshopper compute/volumes. Reads the original v2 inventory and writes a separate 0600 v3 report. Bash and embedded Python syntax checks passed in isolated execution; real Android runtime acceptance is pending.

**Scope caution:** An SDK spot check of selected services corroborates the silent-list behavior but does not prove every unqueried service/resource family is empty. Do not delete OCI instances, volumes, or networks based on this progress meter or the partial inventory.
