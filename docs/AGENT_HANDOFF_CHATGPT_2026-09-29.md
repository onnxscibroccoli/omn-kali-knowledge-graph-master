# Agent handoff for ChatGPT — 2026-09-29 18:31 UTC

Copy everything below the line into a new ChatGPT session. Work agentically. Do not invent production proof.

---

## Role

You are a senior software engineer continuing OmniKali work. Prefer correctness over speed. Separate facts, assumptions, and recommendations. Preserve existing production behavior unless an authorized live-acceptance change is explicitly requested.

Owner account: `onnxscibroccoli`.
Canonical graph: `onnxscibroccoli/omn-kali-knowledge-graph-master`.
Implementation owner for BIST: `onnxscibroccoli/Grasshopper`.

## Mission now

1. Keep BIST machine-readable and schema-valid after the merged schema contract.
2. Keep local BIST execution explicitly controllable and non-recursive.
3. Do **not** mark production desktop, database write-path, worker recovery, or executor side-effects PROVEN.
4. Next implementation gate: produce a clean-host dry-run evidence bundle, then continue toward helix #21 for live desktop acceptance. Guest-desktop live acceptance remains helix #21.

## Hard constraints

- Do not bind new ingress to host `:80`/`:443` (Grasshopper #62).
- Do not replace production PostgreSQL / RDS.
- Do not expose, copy, or print production credentials, cookies, or agent secrets.
- Do not treat Kubernetes as the current public origin.
- Do not treat process/pod/HTTP liveness as `PASS`.
- Do not mutate production from BIST. Public probe is GET `/health` only, and only when `OMNIKALI_BIST_PUBLIC=1`.
- Do not push directly to Grasshopper `main` if `BASE_SYSTEM_PROTECTION.md` requires a branch/PR. Use a feature branch.
- Knowledge-graph `main` may receive documentation/index updates.
- Historical acceptance IDs may be cited in `detail`. They do not promote a gate to PROVEN by themselves.

## Current facts (verified 2026-09-29)

### Production path that remains authoritative

CloudFront → nginx → Helix → libvirt/QEMU → Kali guest `helix-omnikali`.

Public health URL used by BIST when opted in:
`https://d22bad48irrbqe.cloudfront.net/health`

### BIST emitter already on Grasshopper main

File: `scripts/bist.mjs`
Command: `npm run bist`
Schema id already emitted: `omnikali-bist/v1`
Statuses: `PASS | FAIL | NOT_PROVEN | NOT_APPLICABLE`
Overall today: `FAIL` or `PASS_WITH_NOT_PROVEN` only.
Exit code: `1` if overall `FAIL`, else `0`.

Skip-local control is now implemented on Grasshopper main: `runBist({ includeLocal: false })` and `OMNIKALI_BIST_SKIP_LOCAL=1` both skip local unit/reference checks. Skipped checks are `NOT_APPLICABLE` and non-blocking. This prevents BIST contract tests from recursively launching `npm test`.

Production checks default to `NOT_PROVEN` unless `evidence/bist-production.json` or `OMNIKALI_BIST_EVIDENCE` supplies both `acceptanceId` and a valid status.

`production.kubernetes` is `NOT_APPLICABLE`.

### Schema work merged on Grasshopper main

PR: https://github.com/onnxscibroccoli/Grasshopper/pull/71
Merged commit: `afb6086d73b34afe40a431b0ddba77d2057c2bcc`.
Schema branch HEAD before merge: `33b3e499dac78b1b0bfd8d820a4cc7721d4f75a7`.


Files on that branch:

- `schemas/omnikali-bist-v1.schema.json`
- `schemas/omnikali-bist-evidence-v1.schema.json`
- `schemas/examples/bist-report.valid.json`
- `schemas/examples/bist-evidence.valid.json`
- `scripts/validate-bist-schema.mjs`
- `test/bist-schema.test.mjs`
- `docs/BIST_JSON_SCHEMA.md`
- `package.json` scripts `validate:bist-schema` and `test:bist-schema`

Graph copies already on KG main:

- `schemas/omnikali-bist-v1.schema.json`
- `docs/BIST_JSON_SCHEMA.md`
- this handoff file

PR #71's GitHub Actions were inspected and successful for the BIST and Reference tests workflows. PR #72 then added skip-local behavior and a dedicated environment-control test; its BIST, Reference tests, Agentic Reference Control Plane, and Agentic MVP Reproducibility workflows all completed successfully before merge.

### Tracking issues

- Grasshopper #65 architecture program: https://github.com/onnxscibroccoli/Grasshopper/issues/65
- KG #2 goals graph: https://github.com/onnxscibroccoli/omn-kali-knowledge-graph-master/issues/2
- helix #21 authenticated guest desktop acceptance (blocker for production desktop PASS)
- Grasshopper #62 do not bind new ingress to 80/443
- Grasshopper #64 / grasshopper-kubernetes #1 non-production Guacamole/VNC only

### Existing parallel BIST branch

`feat/bist-c0-contract` exists and has `docs/BIST_CONTRACT.md` plus `test:bist` on that branch. Do not fork a third BIST design. Prefer PR #71 schema + current main `scripts/bist.mjs`. Reconcile CLI flags from the C0 doc (`--skip-local`, `--allow-dirty`, `--public`) with env vars already implemented:

- `OMNIKALI_BIST_PUBLIC=1`
- `OMNIKALI_BIST_REQUIRE_CLEAN=1`
- `OMNIKALI_BIST_OUTPUT=<path>`
- `OMNIKALI_BIST_EVIDENCE=<path>`
- `OMNIKALI_BIST_PUBLIC_URL` optional override

## Recommended next actions (in order)

### Gate C.1 — merge hygiene for PR #71 (complete)

1. Checkout `feat/bist-json-schema-v1`.
2. Run:
   ```bash
   npm run test:bist-schema
   npm run validate:bist-schema
   node --test test/bist-contract.test.mjs
   ```
   If `bist-contract.test.mjs` invokes `runBist()` and therefore `npm test`, set a skip-local env once you implement it, or run only the schema tests.
3. Review `scripts/bist.mjs` output against the schema. If live emitter output has extra fields, either add them to the schema or stop emitting them. Schema currently `additionalProperties: false` on the report object. Current emitter fields are exactly: `schema`, `timestamp`, `checks`, `summary`, `overall`. Checks have `id`, `status`, `detail`, `blocking`.
4. Merge PR #71 only after tests you actually ran are green. Do not claim CI is green unless you inspected checks.

### Gate C.2 — make BIST non-recursive (complete)

In `scripts/bist.mjs`:

- Honor `includeLocal === false`.
- Add `OMNIKALI_BIST_SKIP_LOCAL=1` as the env equivalent.
- When skipped, mark `local.unit-tests` and `local.reference-verification` `NOT_APPLICABLE` or omit them consistently. Prefer `NOT_APPLICABLE` with `blocking: false` so summaries stay honest.
- Update `test/bist-contract.test.mjs` so it no longer accidentally launches the full suite.

Do not change production check defaults.

### Gate C.3 — optional phase field

If you emit `phase`, use only:
`auth | provisioning | connectivity | interactive | recreation | runtime | source | local | reconstruction | production`

Map the five-phase live suite later; do not invent PASS for those phases.

### Gate B — clean-host reconstruction evidence

`npm run verify:clean-host-dryrun` is fail-closed. BIST already maps explicit `FAIL_CLOSED` / `clean_host_reconstruction: blocked` to `NOT_PROVEN` rather than `FAIL`. Preserve that.

Produce a dated evidence note, not a fake PASS.

### Gate A — live desktop

Only helix #21 plus authorized acceptance credentials. Browser path must be CloudFront `/auth/login` → ticketed WSS → intended guest. Direct `wss://helix.omnikali.io:8444/...` is not the public contract.

## Commands

```bash
# schema branch
git clone https://github.com/onnxscibroccoli/Grasshopper.git
cd Grasshopper
git fetch origin feat/bist-json-schema-v1
git checkout feat/bist-json-schema-v1
npm run test:bist-schema
npm run validate:bist-schema

# emitter on this branch still works
OMNIKALI_BIST_OUTPUT=/tmp/bist-report.json npm run bist
node scripts/validate-bist-schema.mjs report /tmp/bist-report.json
```

After skip-local is implemented:

```bash
OMNIKALI_BIST_SKIP_LOCAL=1 npm run bist
```

## Definition of done for this handoff thread

The schema/skip-local gates are complete. The next agent should continue at Gate B.

- PR #71 is merged.
- PR #72 (`fix(bist): honor skip-local execution controls`) is merged as `8ef386fb349da7874500109bce037c4e5f9b3456`.
- Schema and skip-local tests passed in GitHub Actions.
- No document claims production guest desktop is PROVEN.
- Next gate: clean-host reconstruction evidence, then helix #21 live desktop acceptance.

## Out of scope unless the user asks again

- Binding new public ingress
- Replacing Helix with Kubernetes
- Changing RDS
- Enabling authenticated BIST against production
- Multi-agent orchestration
- Claiming transcendental/self-repair capabilities are live
