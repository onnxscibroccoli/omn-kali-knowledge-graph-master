# Broccoli Transport Contract

> 2026-10-07 launcher supersession: this dated record retains historical evidence. Physical automation uses broccoli-core `lib/rish_run.sh` (or its delegating `bin/broccoli-rish` entry point); raw Rish paths and direct launch examples below are historical/internal-driver descriptions, not supported public launch instructions. See [current policy](PHYSICAL_ANDROID_TRANSPORT_2026-10-07.md). Remote Android transport remains explicitly configurable.

**Tag:** BROCCOLI-TRANSPORT-CONTRACT-2026-10-01
**Status:** code-verified against `broccoli-core` `main`
**Source inspected:** `lib/rish_run.sh`
**Blob:** `81414aa0f6a9f79db0a346fb8ab459824612cb64`
**Tree commit observed:** `4f3c84e6a02aa43ce130d99215ff6a8607dfb969`
**Device re-proof this session:** NOT_RUN

This file is the executable contract. The iteration narrative in `docs/BROCCOLI_ITERATION_KNOWLEDGE_2026-10-01.md` explains why the contract exists. If they disagree, source plus a fresh target artifact wins.

## What is already proven

Prior device evidence, not re-run here:

- Android API 35
- Rish identity `uid=2000(shell)`
- known-good invocation uses `RISH_PRESERVE_ENV=0`
- interactive Termux `rish` returning `shell` did not prove the RDC caller
- RDC `RC=0` with empty stdout was a caller-environment failure, not a broken Rish binary
- supervisor recovery on broccoli-core PR #62: kill MCP, supervisor recreates it, fresh initialize returns `omnikali-control-plane` `0.1.0`

Do not repeat those experiments unless the caller, binary, env snapshot, or Android version changed.

## Canonical boundary

```text
RDC or other non-TTY caller
  -> Termux bash
  -> broccoli-core/lib/rish_run.sh
  -> sanitized env -i
  -> allowlisted Android runtime variables
  -> /data/data/com.termux/files/usr/bin/rish -c
  -> Android shell uid=2000
```

There is one wrapper. Do not add `rish_run2.sh`, a second event bus, or a workstation impersonation of Termux.

## Source-verified behavior

`lib/rish_run.sh` currently does all of the following:

1. Requires a command. Missing command exits `2`.
2. Requires executable `RISH_BIN`, default `/data/data/com.termux/files/usr/bin/rish`. Missing binary exits `79` with `RISH_BIN_MISSING`.
3. Reads `BROCCOLI_RISH_ENV`, default `$HOME/.config/broccoli/rish/android-runtime.env`.
4. If that file is readable, replaces the process with `env -i` and only these caller variables: `HOME`, `PWD`, `PREFIX`, `TMPDIR`, `PATH`, `SHELL`, `TERM`, `RISH_APPLICATION_ID`, `RISH_PRESERVE_ENV`.
5. Defaults `RISH_PRESERVE_ENV` to `0` when unset.
6. From the env file, exports only: `BOOTCLASSPATH`, `DEX2OATBOOTCLASSPATH`, `SYSTEMSERVERCLASSPATH`, `ANDROID_*`, `LD_LIBRARY_PATH`, `LD_PRELOAD`, `CLASSPATH`, `EXTERNAL_STORAGE`.
7. Executes `rish -c` with the joined command.
8. If no env file exists but live `BOOTCLASSPATH` is set, executes `rish -c` directly.
9. Otherwise fails closed with exit `78` and `RISH_ENV_MISSING`.

The script does not detect RDC by name. It detects a missing Android runtime snapshot. Do not describe it as an RDC-specific patch.

## Environment capture rule

Capture `android-runtime.env` only from a proven interactive Termux session that already has `BOOTCLASSPATH`.

Never capture it from:

- an RDC reduced environment
- a failed `RC=0` empty-stdout run
- a workstation shell
- a dump of the entire Termux environment

A stale or reduced snapshot is preferred by the wrapper whenever the file is readable. A bad snapshot can therefore hide a good interactive shell. If transport regresses, inspect the snapshot before editing `rish` or Shizuku.

Do not persist `TERMUX_*` variables or API keys into the snapshot.

## Two homes

| Context | Identity | Owns |
|---|---|---|
| Termux | Termux app user | `broccoli-core`, MCP on `127.0.0.1:8787`, supervisor, token file |
| Rish | `uid=2000(shell)` | Android shell commands and UI automation visible to shell |

Do not assume shared `HOME`, `PATH`, or private Termux storage.

## Pass rule

A transport pass requires all of:

- expected marker in stdout, for example `BROCCOLI_RISH_OK`
- `uid=2000(shell)`
- requested `getprop ro.build.version.sdk` value when that probe is part of the command
- no reliance on `RC=0` alone

Exit `78` or `79` is a failed closed gate, not a reason to rewrite Rish.

## Promotion rule

Wrapper changes use `.new`, then syntax/self-test, then target-artifact proof, then atomic `mv`.

Do not promote because the script exited 0.

## What this session did not prove

- device reboot restoration
- battery-optimization exemption
- force-stop survival
- Grasshopper PR #115 observe/select/act/verify on a real APK
- Morphe source confirmation UI
- Morphe source build
- Grasshopper persistent build storage / JDK gate

Those remain open. Documentation does not pass them.\n## Current implementation provenance
\n\nThe canonical Android action layer was updated in `onnxscibroccoli/broccoli-core` commit `785f73315893b4917ceac23552f818ef94dd6982` (2026-10-02): `display.list` now uses `cmd display get-displays` instead of `dumpsys display`, because the latter can remain suspended when invoked through the background Rish path on Samsung Android 15. The focused Android contract/CLI/transport/action test set passed 21/21 with this implementation.\n\nThis change does **not** create a second transport and does not modify `lib/rish_run.sh`. The canonical boundary above remains authoritative.\n\nCurrent physical-device transport status remains **NOT_PROVEN** in this session: the installed Rish binary and dex are present, but the live Shizuku service is not currently producing stdout from `rish -c`. A zero exit code without the required marker is not a transport pass.\n