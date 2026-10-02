# Grasshopper browser providers and universal goals

Date: 2026-10-02. Status: written design for review; runtime not implemented.

## Approved intent

Grasshopper owns a durable, provider-neutral automation loop on remote workstations. It can communicate with supported AI providers through browser interfaces without requiring OpenClaw. Android remains an execution edge through Broccoli's canonical Rish boundary. A universal goals registry covers the accessible account repository tree and exposes both proven capabilities and intended architecture through the existing knowledge graph.

## Ownership and alternatives

Extend Grasshopper's existing task/control-plane and application-observation modules. Store cross-repository coordination in omn-kali-knowledge-graph-master, the existing canonical graph owner. Preserve PR #115's agent-loop/provider/human-gate work by reviewing and reusing its contracts before implementation. Do not create another orchestrator or copy the Android executor.

Recommended: Grasshopper runtime plus browser-provider adapters and a central goals registry. OpenClaw remains an optional client. Keeping OpenClaw as the mandatory governor conflicts with the user's goal. A separate orchestrator would duplicate ownership. API adapters may coexist but cannot be a requirement for browser operation.

## Browser-provider contract

Each adapter implements inspectSession, observeConversation, submitPrompt, awaitResponse and reconcileSubmission. Provider identity and account identity are opaque local IDs. A private persistent browser profile belongs to one provider/account and has an exclusive lease. Use semantic locators and explicit supported-page/version contracts. Never share profile cookies or credentials through Git, prompts, or evidence bundles.

The governor owns operation IDs, task state, deadlines, cancellation and checkpoints. Before submission it persists PREPARED with request hash and conversation identity; after observing submission it records SUBMITTED with the provider message identity where available. A crash between those steps yields SUBMISSION_UNKNOWN. Recovery inspects the conversation before any decision to resubmit. Inability to disambiguate preserves unknown state and requests review; switching providers never silently resends an uncertain request.

Accept only a newly observed assistant turn belonging to the current request and conversation. Reject composer text, user messages, navigation chrome, stale answers and incomplete streaming output. Completion requires observed streaming termination and bounded stable response observations. Model responses are untrusted proposals; validate structured action schemas and authorization before passing actions to the existing executor.

Human input takes precedence. Authentication, consent, MFA, CAPTCHA, biometric and payment gates pause mutation, persist a checkpoint, and expose the current browser to the user. Resume only after explicit user completion plus two valid gate-free observations, with conversation/session identity unchanged. Timeout while waiting preserves the checkpoint. No challenge bypass or undocumented provider endpoint is introduced. A provider is supported only after its adapter and live acceptance pass; unsupported pages degrade explicitly.

Observe -> classify -> plan -> validate -> act -> reobserve -> verify -> record is the runtime loop. Events describe facts; observing an event does not replay its command or notification. Recovery restores a route without marking an uncertain task complete. Every successful task needs independent named artifact or application-state evidence.

## Universal goals contract

Use one canonical registry in the graph-master repository, with generated Markdown, Mermaid and speech-ready narratives. Repository-local files reference stable goal IDs rather than duplicate goal definitions. Schema fields: id, title, requestedAt, requestedBy, sourceRequestRef, ownerRepositoryId, affectedRepositories, capability, targetArchitecture, dependencies, acceptanceCriteria, implementationRefs, evidenceRefs, status, blockers, nextAction, revision and supersedes.

Status vocabulary: PLANNED, IN_PROGRESS, BLOCKED, IMPLEMENTED, TEST_PROVEN, LIVE_PROVEN, REGRESSED, RETIRED. Evidence scope is separately UNIT, INTEGRATION, LIVE or RECONSTRUCTION. IMPLEMENTED does not mean TEST_PROVEN. TEST_PROVEN does not mean LIVE_PROVEN. Each evidence record contains repository ID, exact commit SHA, criterion ID, command or scenario, workflow/run/job URL where applicable, environment identity, timestamp, result and artifact hash/reference. A failed required criterion prevents promotion. Skipped jobs and missing artifacts are NOT_PROVEN. Relevant source/transport changes invalidate evidence bindings until retest; old proof remains historical.

New requested features are saved as PLANNED goals before execution, with an idempotent request key. Autonomous discovery records candidate goals with provenance instead of inventing approved user intent. A validator rejects duplicate IDs, dangling repository/goal references, dependency cycles, and unsupported completion claims. Goal changes are atomic and revision-checked; the audit journal is append-only. Merge/release gates consume criterion-level evidence, not a green workflow badge.

Account discovery paginates authenticated accessible repositories, including private repos and forks. Associate by stable repository IDs; preserve source ownership and upstream dependency roles. Index each default-branch tree at its returned tree SHA. Optional branch expansion is a separately tracked coverage goal. Record inaccessible, empty and truncated trees explicitly; never equate omitted repositories with deleted repositories. Preserve private repository metadata in a private inventory; publish only sanitized public projections to the public graph repository. Do not bulk-copy private contents into public documentation.

The inventory links repositories to paths; the architecture graph links components through action verbs such as observes, submits, validates, executes, verifies, records, depends_on and recovers. The goals graph links target capabilities to owners, dependencies and criteria. Speech-ready text accompanies rendered diagrams and retains evidence labels.

## Grounded baseline

29 accessible account repositories were indexed at their default branches on 2026-10-02; all returned trees were untruncated. The companion inventory contains paths and Git object SHAs, not file contents or universal behavior claims. Associated organization/collaborator repositories and non-default branches are not yet covered.

Grasshopper main a0423ee40287506843faff9b24989a1a37217441: BIST run 37034730965, job 110929994187, reported 9 PASS, 0 FAIL, 6 NOT_PROVEN, 2 NOT_APPLICABLE and PASS_WITH_NOT_PROVEN. Authenticated remote desktop, gateway health, database, worker recovery, executor side effects and clean-host reconstruction remain unproven in that run. Development run 37034734341 verified source; autonomous improvement and resulting-state jobs were skipped. Draft PR #115 head aa4d7b63f72a45dd78c64ac170844e916a4f8a5e contains reusable agent-loop/providers/human-gate work; it is not merged-main proof. Ten focused application/BIST tests passed on workstation branch feat/gcp-reproducible-worker-gate at 3ae27cf, a different source identity. The prior OpenClaw consultation timed out without a recommendation.

## Acceptance and delivery sequence

1. Universal registry foundation: schema, seeded user goals, dependency/evidence validator and generated graph/narrative. Prove duplicate-request idempotency, reference integrity, cycle rejection, stale evidence rejection, skipped-job handling, regression preservation and private projection isolation.
2. Browser session/adapter foundation: isolated profiles, exclusive ownership and submission reconciliation. Use local deterministic browser fixtures for normal response, streaming, stale text, selector drift, crash before/after submit, ambiguous submission, rate limit, human gate and human takeover. No paid provider calls are required for CI.
3. One real provider vertical: authorized browser profile -> benign prompt -> new assistant response -> validated action proposal -> isolated workstation action -> independent artifact proof. No OpenClaw process or API key is required by this acceptance scenario.
4. Second provider vertical: repeat the same task contract through a second adapter and prove governor semantics unchanged. Provider switching occurs only before submission or after a resolved terminal outcome.
5. Durable recovery: interrupt browser/worker, restore checkpoint and verify outcome without replay. Preserve uncertain side effects and prove human-gate pause/resume.
6. Account reconciliation: goal/evidence import from source, issues and Actions with provenance; repository association expansion and branch coverage; README and knowledge graph pointer updates. Automated import never promotes closed issues directly to proof.

The first implementation unit is the registry validator and generated goals view in graph-master; the browser-provider contract becomes a linked Grasshopper goal. Each unit receives narrow tests, complete relevant CI checks, a draft PR and dated evidence. No protected Helix infrastructure changes, automatic merges or historical-script replay are part of this design.

## Review status

Written specification and implementation plan reviewed and approved by the user on 2026-10-02. Registry foundation is the first execution unit. Browser runtime remains linked follow-on work.
