# Repository Tool Discovery Architecture

Date: 2026-10-01

## Purpose

GitHub Actions provides the repeatable evidence pipeline for repository tool discovery. The pipeline recursively scans the repositories declared in `tools/discovery/discovery_scope.json`, classifies candidate scripts and command line interfaces, validates each manifest against the adjacent JSON Schema, and renders deterministic plain text narrative output.

## Pipeline stages

First, GitHub Actions checks out the knowledge graph repository and establishes a pinned Python major and minor version.

Second, the workflow reads the declared repository scope. Public repositories are cloned with the workflow read token. Private repositories are recorded as NOT_SCANNED unless a separately authorized credential integration is added.

Third, the read-only discovery engine recursively walks each checked out repository. It identifies executable files, shebangs, Python CLI frameworks, MCP patterns, shell CLI patterns, Ansible playbook patterns, and workflow YAML.

Fourth, each discovered candidate receives provenance containing the repository, source reference, and exact source commit. Runtime evidence defaults to NOT_PROVEN.

Fifth, the validator checks every generated manifest against `tools/discovery/tool_manifest.schema.json`. A validation failure fails the workflow.

Sixth, the narrative renderer translates registry metadata into plain text. The narrative uses descriptive verbs and avoids diagrams and symbolic architecture notation so it can be read by text to speech systems.

Seventh, the generated registry, narrative, and private-scope report are uploaded as workflow evidence. On pushes to main, changed registry and narrative files are committed by the workflow bot.

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

The GitHub workflow definition and repository-side source changes are present on the feature branch. CI execution has not yet been observed from this environment, so end to end workflow execution remains NOT_PROVEN until GitHub Actions produces a successful run artifact.

