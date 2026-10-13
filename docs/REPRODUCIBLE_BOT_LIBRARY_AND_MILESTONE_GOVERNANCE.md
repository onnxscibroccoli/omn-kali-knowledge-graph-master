# Reproducible Bot Library — Broccoli/Grasshopper Cooperative Automation

**Status:** Framework proposal, executable core and fixture tests. No historical agent runs have been automatically promoted.  
**Steward:** Central OmniKali knowledge graph. **Execution owner:** Grasshopper. **Semantic action owner:** Broccoli Core.

## The barn-raising metaphor

An Amish barn raising works because builders share **trusted patterns, measured cuts, reusable jigs, defined roles and quality checkpoints**. The community does not improvise every joist from scratch or interrupt a carpenter after every hammer stroke. The foreman verifies foundations, frames, roof structure and final safety before handing the barn over.

Successful agent workflows should become the software equivalent of a **labeled jig**: compact, repeatable, inspectable and transferable to the next team. The human operator is the inspector at **milestones**, not a person forced to approve each harmless observation. Any risky cut—financial action, authentication, host privilege, privacy breach or destructive replacement—requires explicit human authorization immediately.

This is not permission to run arbitrary code autonomously. Reusable bots are **narrow capability contracts**, not records of unrestricted agent improvisation.

## Roles, contracts and boundaries

`Observation -> Planner -> Governor -> Capability Router -> Executor -> Verifier -> Checkpoint -> Audit -> Bot Proposer`

- **Broccoli Core** defines application/device graph nodes, stable semantic selectors, intent/action schema, physical Android Accessibility Service and authorized Rish drivers.
- **Grasshopper** owns orchestration, task IDs/idempotency, recovery governor, model adapters, OCI/cloud/browser access and deployment acceptance.
- **The master library** stores sanitized bot definitions, dependencies, versioned schemas, reviewable proposals and cross-repository discovery indices; it **does not** store private actions or session data.
- **Platform adapters** (Android local/cloud, Linux desktop, browser, OCI API, GitHub Actions, self-hosted MCP or LLM providers) emit normalized events after execution. Every event carries platform, typed step, request causality, outcome and an optional private verifiable artifact.
- **Independent verifiers** attach bounded acceptance artifacts. Process existence, exit 0 or self-reported LLM confidence do not prove business success.
- **Operator** approves sensitive credentials/privileges, external purchases, destructive actions, publishing and merges. Bots remain proposals until reviewed.

## Two-zone information model

| Zone | Stores | Never stores |
| --- | --- | --- |
| **Public GitHub bot catalogue** | Typed intent templates; generalized selectors; capabilities; prerequisites; milestone descriptions; documentation; schema/tests; reviewed evidence summaries | Direct contacts; full URLs with bearer tokens; account IDs; health/payment data; auth cookies; raw transcripts; full screenshots; proprietary application data; host keys |
| **Private per-device evidence** | Append-only per-run JSONL; local proof artifacts; idempotency ledger; scoped secret references; authorized rollback checkpoints | Permanent raw passwords in bot definitions; unbounded production screen recordings; logs copied indiscriminately into public issues |

The Python `tools/bot_library.py` records **allowlisted structured event fields only**, uses restrictive `0600` journals, locks for concurrent writes, links entries by SHA-256, rejects repeated event IDs and requires real, hashed private evidence for independent milestone verification. SHA-256 chain integrity detects accidental or casual tampering; it is **not a cryptographic signature or protection from an administrator able to rewrite all files**.

Raw operational traces may contain secrets; redact or discard at the acquisition boundary. API credentials and session material belong in separately protected device keyrings or cloud IAM, never in GitHub or a bot file. Merely writing `secret_refs` is not permission to retrieve or distribute a secret.

## Bot lifecycle

1. **Observe** a bounded human-authorized task and label each action by executor, semantic intent, risk, origin and target platform.
2. **Reconcile** observed UI events with originating action IDs; **never replay the originating command on observation**.
3. **Classify** successful/failed cases; do not promote an isolated process PASS or cache hit from a different code/transport.
4. **Reproduce** in a clean isolated environment with mocked credentials or scoped test identities.
5. **Independently verify** the task's required milestones and stored artifacts, including UX/input/reconnect for remote desktops.
6. **Generalize** parameter inputs, stable selectors, capability lists, approval points and recovery path. Remove personal state, raw output and vendor lock-in.
7. **Propose** a bot manifest with `source_ref: main` and a hashed proof chain. The tool produces a **REVIEW_REQUIRED** proposal, not an automatic publication.
8. **Review** privacy, scope, costs, rollback, provenance and tests via draft PR. An operator explicitly approves any publication or production deployment.
9. **Index** approved manifests in the master graph under bot ID, version, platforms, dependencies, owner, acceptance revision, and capabilities. Workers discover bots through a registry API or MCP resource with read-only access, never Git history scraping.
10. **Evolve** with semver, canaries, acceptance and rollback; keep failed cases as sanitized lessons rather than retraining fragile success assumptions into the library.

## Milestone supervision instead of step-by-step micromanagement

A task has explicit gates: `PLAN_ACCEPTED` → `ENVIRONMENT_READY` → `MILESTONE_VERIFIED` → `RECOVERY_READY` → `OPERATOR_ACCEPTED`.

Routine reversible actions may proceed within bounded quotas without chat interruptions. Human check-ins occur only at a named milestone, sensitive capability request, non-idempotent/destructive mutation, exhausted repair budget, missing evidence, OAuth/CAPTCHA/biometric step or failed invariant. The governor cancels or pauses rather than repeatedly correcting partially observed successes.

This makes operators scalable: parallel specialists may build different components, but they must pass contracts at handoff boundaries. One agent's observation must never cause another agent to replay the initial mutation.

## CLI operations (private, safe examples)

```bash
python3 tools/bot_library.py validate bots/oci-admission-preflight.json

# A platform adapter writes a PRIVATELY SCRUBBED event JSON with the exact
# schema documented in the Python implementation and a synthetic or real
# acceptance artifact within the PRIVATE store.
python3 tools/bot_library.py record bots/oci-admission-preflight.json \
  /private/path/to/event.json --store /private/bot-evidence

python3 tools/bot_library.py propose bots/oci-admission-preflight.json \
  --run-id run_example --store /private/bot-evidence
```

Do **not** run these CLI examples against real private account data until private-path permissions and event filters have been reviewed. A manifest whose `acceptance.status` is `NOT_PROVEN` is a template, not a claimed successful bot.

## Remote access and just-in-time privilege

The operator may personally execute a reviewed local script through an already authenticated remote desktop and enter a sudo password in the workstation's **own interactive terminal**. Remote Desktop Commander **does not receive or persist that password**. Systemd service enablement and user linger are configured in a bounded root-only installer; the remote device process remains an unprivileged user service.

Never set unrestricted `NOPASSWD: ALL`, store `SUDO_ASKPASS` passwords, forward credential prompts through MCP or grant persistent root to a general-purpose model. For future approved privileged workflows, use a separately audited root-owned capability helper allowing precisely defined commands, with expiry and evidence, rather than disclosing sudo credentials.

## Production test gates

- Event schema and privacy allowlist validation.
- Hash chain, deduplication, no replay and evidence integrity checks.
- Simulator for independent milestone proof, failure/pause and incomplete acceptance.
- Cross-platform contract tests for browser, Android/Termux, OCI and Linux.
- Human-visible remote desktop reconnection after reboot, not just active systemd units.
- Approval and merge controls for reviewed bot promotion, kernel changes and privileged scripts.
- No credential dumps, historical raw Git SHA reads, cloud billing changes or accidental public services.

## Next integration steps

Convert the library into a minimal read-only MCP catalogue and an event-ingestion API with per-device mTLS or short-lived OAuth capability grants; connect Broccoli semantic actions and Grasshopper governor events. Add a private evidence exporter that derives scrubbed public summaries. Implement independent human-visible acceptance on two distinct execution targets before promoting the first real bot.

**Canonical source reads: `main` only.** Development stays on reviewable feature branches. Historical Git SHA values may be opaque provenance metadata but must not be used to fetch source.
