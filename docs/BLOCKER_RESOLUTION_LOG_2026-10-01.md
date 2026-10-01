# Blocker Resolution Log — 2026-10-01

**Session evidence source:** GitHub contents of `omn-kali-knowledge-graph-master` `main` at `3c47517a1e0e096be07ef7a7444407c375198b9f`, `broccoli-core` `lib/rish_run.sh`, open PRs.
**Device:** not attached. No live Android command was run.

## Resolved in this session

1. Documentation could identify the Rish lesson but did not bind it to the wrapper that is actually on `main`.
   Resolution: `docs/BROCCOLI_TRANSPORT_CONTRACT_2026-10-01.md` records blob `81414aa0f6a9f79db0a346fb8ab459824612cb64`, exit codes `2/78/79`, the `env -i` allowlist, and the stale-snapshot hazard.
2. Agents could still "test Rish again" without a stop condition.
   Resolution: `goals/broccoli-transport-preflight-2026-10-01.yml` is mandatory before a new transport experiment.
3. Confirmed the prior iteration record and system graphs exist. They are not rewritten.

## Not resolved, and why

| Gate | Status | Why it stays open |
|---|---|---|
| Grasshopper #115 Android MCP acceptance | draft, NOT_PROVEN | Needs phone observe -> select -> act -> verify. Repo existence is not the gate. |
| broccoli-core #62 supervisor recovery | OBSERVED in PR text | Bounded kill/recreate only. Reboot and force-stop remain NOT_PROVEN. |
| Morphe source confirmation | NOT_PROVEN | Deep link is not install confirmation. |
| Morphe source build | BLOCKED | Downstream of Grasshopper storage/JDK. Do not fill root disk to bypass the gate. |
| Production eight-scenario desktop acceptance | OPEN | Not run this session. |
| Clean-host reconstruction | OPEN | Not run this session. |

## Logical next action

On the phone, do not retest Rish unless the preflight says the caller or snapshot changed.

Next new evidence is one real APK loop through the existing phone-local MCP:

1. initialize `127.0.0.1:8787`
2. `android.ui.snapshot`
3. semantic locate
4. one confirmed mutating action
5. reobserve
6. verify postcondition
7. store the artifact

If that fails, classify the failed boundary before changing transport.
