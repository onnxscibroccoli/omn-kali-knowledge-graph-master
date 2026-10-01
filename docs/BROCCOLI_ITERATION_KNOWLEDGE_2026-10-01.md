# Broccoli Iteration Knowledge and Transport Record

**Graph tag:** BROCCOLI-KG-2026-10-01
**Scope:** broccoli-core, Android/Termux/Rish/Shizuku/RDC execution, OmniKali MCP, and recovered Broccoli philosophy
**Purpose:** preserve the actual lessons from the iterative transport work so future agents do not repeat already-resolved experiments or regress into previously rejected designs.

## 1. Role of Broccoli

Broccoli is the Android-side execution and accessibility layer in the OmniKali system.

It is not the production cloud control plane and must not be treated as a second source of truth for Helix.

Its durable role is:

`intent -> cheapest matcher -> one schema -> dry-run -> execute -> event -> remember`

The Android phone is expected to close its own execution loop. Chat is an accessibility surface, not the execution transport.

The useful philosophy is preserved. Historical implementation debris is not automatically copied forward.

## 2. Historical versus current code

Legacy Broccoli checkouts are valuable as historical reference for philosophy and previously passing tests.

One legacy reference checkout was observed at HEAD `ed3007e`, dirty and behind six commits. It was explicitly treated as historical evidence, not a candidate for modernization or reset/pull.

Historical machinery included:
- BroccoliWorkspaceBackup/
- tools/rish_grok_once.sh
- tools/rish_grok_round.sh
- lib/broccoli_rish_ui.py
- lib/rish_run.sh
- lib/rish_cmd.sh
- rish.sh
- rish_exec.sh

Rule: do not modernize, rewrite, reset, or pull a historical checkout merely to make it fit the current architecture.

## 3. Canonical Android transport boundary

The proven execution chain is:

`RDC/Termux -> broccoli-core -> lib/rish_run.sh -> Rish/Shizuku -> Android shell uid=2000`

The Android executor must execute beside the real Termux/Rish environment.

A workstation process must not impersonate the phone's Termux environment.

Known-good invocation:

`cd ~/broccoli-core && RISH_PRESERVE_ENV=0 bash ./lib/rish_run.sh 'echo BROCCOLI_RISH_OK; id; getprop ro.build.version.sdk'`

Known proof:
- Android API 35
- target identity `uid=2000(shell)`
- SDK 35
- interactive `rish` works
- `rish -c` works

## 4. Rish transport failure history

### Initial symptom

RDC could invoke the Broccoli/Rish path but received RC=0 with no useful stdout and no target marker.

At the same time, interactive Termux:

`rish`

returned:

`shell`

This proved that Rish itself was not the original failure.

### Root cause

The failure was at the RDC -> Termux reduced execution environment boundary.

The environment used by RDC was materially different from a normal interactive Termux process.

The upstream/non-TTY Rish path also has a stdout/stderr descriptor problem, and Shizuku issue #2336 was consistent with silent success under reduced environments.

A critical lesson was therefore established:

**Do not modify or blame a known-good lower transport layer when the caller environment has not been proven equivalent.**

### Known required runtime context

The working environment included values equivalent to:
- HOME=/data/data/com.termux/files/home
- PREFIX=/data/data/com.termux/files/usr
- TMPDIR=/data/data/com.termux/files/usr/tmp
- TERM=xterm-256color
- SHELL pointing at the Termux bash

The exact environment must not be persisted wholesale.

### Final transport fix

`lib/rish_run.sh` was hardened to:
1. detect the reduced RDC environment
2. restore only the required Android/app_process runtime variables
3. invoke through a sanitized `env -i`
4. fail closed when the environment snapshot is missing
5. avoid persisting API keys and `TERMUX_*` variables
6. produce target-artifact evidence rather than trusting RC=0
7. promote changes using `.new -> test -> mv`

The final transport artifact proved:
- `uid=2000(shell)`
- SDK 35
- an explicit success marker

Therefore RDC -> Termux -> Rish is now PROVEN for the tested path.

### Regression rule

Never return to:
- accepting RC=0 with empty stdout
- copying the entire Termux environment into persistent state
- assuming an interactive TTY proves a pipe-based caller
- editing Rish/Shizuku because RDC has not reproduced the environment
- changing a known-good wrapper without first reproducing the caller boundary

## 5. Environment boundary rules

There are two distinct homes/execution contexts:

### Native Termux
`$HOME = /data/data/com.termux/files/home`

Owns:
- broccoli-core
- local MCP server
- supervisor
- Termux-native processes
- private runtime state

### Rish / Android shell
Rish executes as Android `shell` and crosses the Termux private-storage boundary.

Owns:
- Android system commands
- Android UI automation
- shared/system artifacts available to uid 2000

Never assume the Rish process and Termux process have the same HOME, PATH, permissions, filesystem view, or installed binaries.

A previous failure came from assuming this equivalence.

## 6. Evidence model

Broccoli must distinguish:
- process launched
- command returned RC=0
- stdout exists
- expected artifact exists
- expected target identity exists
- expected postcondition exists

Only the complete evidence chain can become PASS.

Canonical statuses:
`PASS | FAIL | NOT_PROVEN | NOT_APPLICABLE`

An empty stdout with RC=0 is NOT success.

A UI command that times out is not evidence that the underlying Android subsystem is broken. Isolate the executor timeout from the target operation.

A direct Rish proof and an RDC-mediated proof are separate gates.

## 7. Boot and supervisor lessons

Relevant paths:
- `~/.termux/boot/broccoli-supervisor`
- `~/bin/broccoli-supervisor`
- MCP supervisor on `127.0.0.1:8787`

The supervisor architecture includes:
- separate supervisor PID and MCP server PID
- lock directory to prevent duplicate supervisors
- bounded polling
- MCP token in `~/.config/omnikali/mcp.token`
- MCP log in `~/.config/omnikali/mcp.log`
- MCP launched with `BROCCOLI_ROOT=$HOME/broccoli-core`
- Termux:Boot integration
- wake-lock request

A duplicate-supervisor bug occurred when supervisor and server PID ownership was initially conflated. It was fixed by separate PID files and a lock.

A stale MCP process from an earlier supervisor epoch also occupied the port during testing. The clean recovery gate then passed:
1. one real supervisor
2. one real MCP server
3. duplicate supervisor launch does not create another watcher
4. intentionally terminate MCP
5. supervisor recreates MCP
6. fresh MCP initialize succeeds
7. Broccoli main runtime is not restarted

This proves bounded supervisor recovery, not Android process immortality.

Still NOT_PROVEN:
- actual device reboot restoring the complete stack
- exemption from Android battery optimization
- immunity to Android force-stop/process termination

Never claim Android cannot terminate Termux.

## 8. Android-native OmniKali MCP

The custom MCP belongs on the phone beside Broccoli/Rish.

Transport:
`http://127.0.0.1:8787/mcp`

Authentication:
private bearer token in `~/.config/omnikali/mcp.token`

Fail-closed mutation policy:
mutating tools require explicit confirmation.

Core tools include:
- device.identity
- device.list
- fs.read
- fs.list
- fs.search
- fs.write
- fs.move
- process.list
- process.exec
- process.kill
- android.rish
- android.input
- android.screenshot
- app.inspect
- app.launch
- app.stop
- model.status
- model.ask
- human.status

UI tools:
- android.ui.snapshot
- android.ui.find
- android.ui.tap
- android.ui.text
- android.ui.back

Application intelligence:
- app.catalog
- app.optimization.plan

Morphe intelligence:
- morphe.sources.manifest
- morphe.source.prepare
- morphe.batch.prepare

The model is replaceable. The deterministic executor owns actual actions.

Remote model APIs are optional. The core Android agent must be able to operate through MCP against installed APK UIs without requiring a paid vendor API.

## 9. UI automation contract

Canonical loop:

`observe -> understand -> locate -> act -> reobserve -> verify -> remember`

Selector priority:
1. exact resource-id
2. exact content-desc
3. exact text
4. stable semantic text
5. class/package plus spatial relation
6. coordinates only as last resort

On selector failure:
1. reobserve
2. replan
3. try an alternate semantic selector
4. use visual fallback only when evidence supports it
5. stop at a human boundary rather than guessing

A prior uiautomator dump through an RDC process timed out. That was NOT_PROVEN for that executor path, not proof that Rish or Android UI automation was broken.

The app-inspection approach is APK-first:
package discovery -> installed APK path -> copy APK -> manifest/resources/layout/resource-id extraction -> normalized app map -> runtime UI snapshot -> revalidate current state.

Useful tools when present:
- apkanalyzer
- aapt2
- JADX
- apktool

The normalized app map may be cached by package/version, but runtime state must always be revalidated.

## 10. Morphe integration lessons

Morphe source installation is a separate acceptance gate.

The existence of a source repository, a prepared deep link, or a successful launch is not installation proof.

Official Morphe source behavior requires user confirmation. Therefore:
- deep-link opened: OBSERVED
- source confirmation UI observed: required
- source added: only after confirmation evidence
- patch completed: separate proof
- resulting app runtime: separate proof

The attempted source handoff opened Morphe but the actual source-confirmation UI was not observable. Therefore source installation remains NOT_PROVEN.

Do not repeat the same deep-link attempt while calling it installed.

## 11. Broccoli philosophy that must survive

Preserve these concepts:
- one phrase fires one schema
- cheapest matcher before expensive model/provider
- schema index -> Markov -> ONNX -> provider cascade where useful
- Echo proves the loop without consuming model tokens
- confirmation is a notification, not a code review
- Grok is an accessibility surface, not the product
- the phone closes its own loop
- changes use .new -> self_test.sh -> mv only on PASS
- sensors should point back to the user or not be collected

Do not preserve historical implementation debris merely because it exists.

## 12. Historical degradation lessons

These failures are architecture requirements now:

1. Contracts were replaced with `# see chat ENGINEERING.md`.
   Rule: executable/local contracts must live in the repository.

2. Milestones were claimed shipped while files were placeholders.
   Rule: shipped means artifact exists, test passes, and acceptance evidence exists.

3. Duplicate root scripts/logs/backups accumulated.
   Rule: one canonical owner per capability.

4. Atom forked, including duplicate `rish_run.sh` and event buses.
   Rule: do not create a second implementation when one canonical transport exists.

5. RC=0 / empty stdout was treated as success.
   Rule: require target artifact/postcondition evidence.

6. A known-good wrapper was blamed for a caller environment problem.
   Rule: isolate execution boundaries before editing working lower layers.

7. The phone-closes-own-loop rule was inverted into paste-back chat.
   Rule: the Android executor closes the action loop locally.

8. An installation ended by stopping the daemon even though it was supposed to remain running.
   Rule: preserve requested runtime state after installation and verify it.

9. An earlier supervisor implementation shared PID ownership.
   Rule: supervisor and child process identity must be independently tracked.

10. Duplicate supervisors accumulated during testing.
    Rule: lock the supervisor ownership boundary.

11. Heavy source builds were considered before persistent build storage was available.
    Rule: storage/JDK readiness precedes expensive build work.

## 13. Current Broccoli status

PROVEN:
- Android API 35
- direct interactive Rish
- noninteractive Rish with `RISH_PRESERVE_ENV=0`
- RDC -> Termux -> Rish target identity/artifact proof
- custom authenticated MCP
- MCP supervisor bounded recovery
- APK catalog
- runtime UI snapshot
- semantic UI automation contract
- Morphe application intelligence contract

NOT_PROVEN:
- Android reboot restoring full stack
- battery optimization exemption
- force-stop immunity
- complete real-app observe/select/act/verify acceptance through every MCP UI action
- Morphe source confirmation/install
- source-built Morphe artifact on Grasshopper

BLOCKED:
- heavy Grasshopper source builds until persistent storage and JDK are provisioned

## 14. Mandatory future-agent preflight

Before changing Broccoli/Rish/MCP transport, read this file and answer:

1. Is the failure direct Termux, Rish, RDC, or target-application?
2. Does direct interactive Rish still pass?
3. Does `RISH_PRESERVE_ENV=0` still apply?
4. Is the caller using the same environment as the proven path?
5. What target artifact/postcondition will prove success?
6. Am I about to create a duplicate transport or script?
7. Is the requested mutation confirmed and fail-closed?
8. Is this actually an Android problem, or an executor timeout/environment problem?
9. Does the existing proof already answer this experiment?
10. What exact new evidence would change the graph status?

If the answer to #10 is "none", do not run another iteration.

## 15. Canonical command and evidence references

Known-good transport command:

`cd ~/broccoli-core && RISH_PRESERVE_ENV=0 bash ./lib/rish_run.sh 'echo BROCCOLI_RISH_OK; id; getprop ro.build.version.sdk'`

Expected identity:
`uid=2000(shell)`

Expected API:
`35`

Successful transport changes follow:
`file.new -> syntax/self-test -> artifact proof -> atomic promotion`

Never promote merely because the shell exited zero.
