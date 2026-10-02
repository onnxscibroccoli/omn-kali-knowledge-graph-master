# Repository Tool Discovery Architecture

Date: 2026-10-01

## Purpose

GitHub Actions provides the repeatable evidence pipeline for repository tool discovery. The pipeline recursively scans the repositories declared in `tools/discovery/discovery_scope.json`, classifies candidate scripts and command line interfaces, validates each manifest against the adjacent JSON Schema, and renders deterministic plain text narrative output.

## Pipeline stages

First, GitHub Actions checks out the knowledge graph repository and establishes a pinned Python major and minor version.

Second, the workflow reads the declared repository scope. Public repositories are cloned with the workflow read token. Private repositories are recorded as NOT_SCANNED unless a separately authorized credential integration is added.

Third, the read-only discovery engine recursively walks each checked out repository. It identifies executable files, shebangs, Python CLI frameworks, Node CLI and MCP patterns, shell CLI patterns, Ansible playbook patterns, and workflow YAML.

Fourth, each discovered candidate receives provenance containing the repository, source reference, exact source commit, and Git path history. History is descriptive and does not prove capability.

Fifth, the validator checks every generated manifest against `tools/discovery/tool_manifest.schema.json`. A validation failure fails the workflow.

Sixth, the narrative renderer translates registry metadata into plain text. The narrative uses descriptive verbs and avoids diagrams and symbolic architecture notation so it can be read by text to speech systems.

Seventh, the generated registry, historical registry, qualified registry, narrative, and private-scope report are uploaded as workflow evidence. Repository writeback is deliberately not enabled because the workflow has contents read permission only.

Eighth, the qualification layer applies explicit retest evidence. A live PASS can promote a candidate to HIGH. Historical proof without a current retest becomes HISTORICAL_RETEST_REQUIRED. Weak, archived, mirrored, legacy, and template candidates receive an intended-purpose classification and a conservative improvement strategy. A replacement link is created only when meaningful semantic overlap with a HIGH implementation is established.

## Safety boundary

Discovery is descriptive and read-only. It does not execute discovered scripts, invoke MCP tools, install discovered dependencies, or grant execution authority.

Grasshopper remains the reference control plane. Helix remains the production desktop lifecycle owner. Broccoli Core remains the Android and Termux execution lineage. Discovery metadata cannot override those ownership boundaries.

## Private repositories

Cross-repository private access is deliberately separated from the default GitHub Actions token. The current workflow records private repositories as NOT_SCANNED. A future private-access adapter must use an explicitly authorized GitHub App or equivalent credential, least privilege, auditability, and fail-closed behavior.

Credentials must never be stored in the discovery registry, manifest, generated narrative, or repository source.

## Generated narrative

The narrative is a projection of the registry, not a second source of truth. Machine-readable discovery metadata remains authoritative for catalog structure. Runtime acceptance evidence remains authoritative for capability claims.

## Future extensions

Temporal may consume validated discovery metadata only through a separate workflow architecture decision.

Nushell may be evaluated for individual operator scripts without changing the discovery contract or Broccoli Rish boundary.

Ansible may be introduced for explicit host convergence when repeated configuration responsibility justifies it. Discovery itself does not require Ansible.

## Verification status

GitHub Actions run `36953078467` completed successfully on 2026-10-02 against head `e72c15f736db3fafbc2d40e2b5c50f6b4e4ef374`. It discovered 3,224 candidates across 21 public repositories, recorded 8 private repositories as NOT_SCANNED, indexed Git history, validated the registry, validated 4 explicit retest records, qualified the catalog, rendered the narrative, and uploaded artifact `omnikali-tool-discovery-e72c15f736db3fafbc2d40e2b5c50f6b4e4ef374`.

The qualification result contains 3 HIGH candidates, 1 HISTORICAL_RETEST_REQUIRED candidate, 804 MEDIUM candidates, and 2,416 LOW candidates. The three HIGH candidates are the Grasshopper control-plane CLI, the Grasshopper reference verifier, and the Helix public-health verifier. Broccoli Core's canonical `lib/rish_run.sh` has strong historical proof but remains HISTORICAL_RETEST_REQUIRED because the connected retest device is not the Android/Termux execution device.

The CI execution path is therefore PASS for this snapshot. Local container runtime validation remains NOT_PROVEN, and private repository discovery remains NOT_SCANNED by design.

