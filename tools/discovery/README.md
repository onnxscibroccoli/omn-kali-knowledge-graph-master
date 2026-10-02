# Repository Tool Discovery

This directory defines the first read-only slice of repository-wide tool discovery.

The discovery layer catalogs likely scripts, command-line tools, Ansible playbooks, workflows, and MCP implementations. It does not execute discovered tools, authorize them, or replace Grasshopper, Helix, Broccoli Core, or provider ownership.

## Files

- `tool_manifest.schema.json` defines evidence-aware metadata for one discovered tool.
- `discovery_engine.py` scans a local repository snapshot using conservative source signals.
- `tool_registry.json` is the generated-registry target and remains NOT_GENERATED until a real repository snapshot is scanned.

## Safety boundary

Discovery is descriptive. A discovered path is not automatically runnable.

A manifest defaults runtime evidence to `NOT_PROVEN`. Execution authority must continue to come from the owning control plane and its existing capability contracts.

The engine is intentionally read-only. It does not run shell commands, import discovered modules, invoke MCP tools, parse credentials, or mutate the scanned repository.

## Initial signals

The prototype recognizes:

- Python CLI patterns from argparse, Click, and Typer.
- Python MCP patterns.
- Shell scripts and executable files identified by shebang or executable bit.
- Ansible playbook patterns.
- GitHub Actions-style workflow YAML.

The scanner is deliberately conservative. False negatives are preferable to inventing capabilities.

## Ownership

Grasshopper remains the reference control plane and contract authority.

Helix remains the production desktop lifecycle owner.

Kali Node remains workstation lineage.

Broccoli Core remains the Android and Termux execution lineage, including the proven Rish transport.

Ansible may converge hosts where an adapter explicitly assigns that responsibility. It does not become a second control plane.

Temporal and Nushell are integration candidates, not dependencies of this discovery slice. They must not be introduced merely because discovery exists.

## Verification

Run:

`python3 tools/discovery/discovery_engine.py <repository> --repository owner/name --ref main --source-sha <commit>`

Then validate the emitted JSON against `tool_manifest.schema.json` using the repository's available JSON Schema tooling. The scanner itself remains dependency-light and does not require third-party packages.

## Qualification and self-testing

Discovery is followed by a separate qualification layer.

Historical source history is indexed without treating history as proof of capability. Explicit retest evidence is the only mechanism that can promote a candidate to `HIGH`.

A candidate with strong historical proof but no available current retest is marked `HISTORICAL_RETEST_REQUIRED`. Weak, archived, mirrored, legacy, or template candidates are marked `LOW` and receive an inferred intended purpose. When a semantically related `HIGH` implementation exists, the candidate receives a lineage link to that validated implementation. Otherwise the qualification layer records `NEW_IMPLEMENTATION` rather than silently inventing an executable replacement.

The qualification layer never executes arbitrary discovered candidates. Retests are explicit, separately recorded evidence.

Files:

- `tool_retest_evidence.schema.json` defines explicit retest evidence.
- `retest_evidence.json` records approved retests and historical proof references.
- `history_index.py` records Git path history without promoting it to capability proof.
- `qualify_registry.py` assigns quality, intended purpose, and validated lineage.
