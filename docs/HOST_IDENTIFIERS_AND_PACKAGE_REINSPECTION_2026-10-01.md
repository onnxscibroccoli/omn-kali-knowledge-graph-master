# Host identifiers and package reinspection - 2026-10-01

> 2026-10-07 launcher supersession: this dated record retains historical evidence. Physical automation uses broccoli-core `lib/rish_run.sh` (or its delegating `bin/broccoli-rish` entry point); raw Rish paths and direct launch examples below are historical/internal-driver descriptions, not supported public launch instructions. See [current policy](PHYSICAL_ANDROID_TRANSPORT_2026-10-07.md). Remote Android transport remains explicitly configurable.

Snapshot time: 2026-10-01T17:12Z to 2026-10-01T17:20Z.
Status vocabulary: PROVEN, OBSERVED, NOT_PROVEN, PLANNED.

Use these IDs in every handoff. Do not call every Linux host "the Oracle box" or "Kali".

## HOST-PHONE-A146U

Role: Android executor. Canonical Rish lives here.

| Field | Value | Status |
|---|---|---|
| Model | Samsung SM-A146U | PROVEN 2026-10-01 earlier Rish pass |
| OS | Android 15, API 35, aarch64 | PROVEN earlier pass |
| Packages | 460 total, 91 third-party, 369 system | count PROVEN; system names NOT dumped |
| Termux | 0.118.3; API 0.53.0; GUI 0.1.6; Window 0.17.0; Boot 0.8.1 | PROVEN earlier pass |
| Not installed then | Termux:Float, Termux:X11, Termux:Styling, Termux:Widget, Termux:Tasker | OBSERVED absent, not ruled out |
| This session | no Rish/ADB transport from the connected tool set | NOT re-probed |

Third-party list: `docs/ANDROID_THIRD_PARTY_PACKAGES_2026-10-01.txt`.
System packages were counted and then treated as stock. That assumption is withdrawn. A system dump is still required before any "stock Samsung" claim.

Next phone command, via the known-good wrapper only:

`RISH_PRESERVE_ENV=0 bash ./lib/rish_run.sh pm list packages -s -f`

Also capture `-3` again in the same pass so the two sets can be diffed. Do not modify `lib/rish_run.sh`.

## HOST-KALI-GUEST-25d9daa1

Role: OmniKali MCP shell target. This is the machine reached by `omnikali___run_command`.

| Field | Value | Status |
|---|---|---|
| hostname | kali | PROVEN |
| machine-id | 25d9daa1260340d88610ada1d4f328d5 | PROVEN |
| OS | Kali GNU/Linux Rolling 2026.3 | PROVEN |
| kernel | 7.1.5+kali-amd64 | PROVEN |
| firmware | QEMU / SeaBIOS / Standard PC i440FX + PIIX | PROVEN |
| NIC | eth0 192.168.122.78/24 | PROVEN; libvirt NAT range, not a public NIC |
| egress | 32.199.143.170 | PROVEN as NAT egress only |
| cloud provider | unknown | NOT_PROVEN; cloud-init is not installed |
| disk | /dev/vda1 37G, 23G used, 13G free, 65% | PROVEN |
| uptime at probe | 1 day 20 hours | PROVEN |
| dpkg records | 3336 | PROVEN |
| apt-mark manual | 193 | PROVEN |
| apt-mark auto | 3143 | PROVEN |
| holds | 0 | PROVEN |

This guest is not a stock Kali image.

Manually selected packages beyond a normal desktop seed:

- awscli
- gh
- grok-bot
- nodejs
- npm
- qemu-guest-agent
- spice-vdagent
- sqv

Installed outside apt, in `/usr/local/bin`:

- grok 1.0.41
- gemini 0.61.0
- codex-cli 0.157.1
- GitHub Copilot CLI 1.0.88
- openclaw 2026.9.6 (eb377ac)

Config directories present, contents not read:

- `/root/.grok`
- `/root/.gemini`
- `/root/.codex`
- `/root/.openclaw`

Absent: `/root/.copilot`, `/root/.config/gh`.
Login validity was not tested. Do not treat a config directory as an authenticated session.

Also present: OpenJDK 25.0.4, Firefox 140.15.0esr, Chromium 150.0.7871.181, Node v24.19.0.
Absent: apktool, aapt, adb, docker. Listeners observed: ssh 22 only.

## HOST-HYPERVISOR-UNSEEN

Role: parent of HOST-KALI-GUEST-25d9daa1.

The guest DMI and 192.168.122.78 address show a QEMU guest behind libvirt NAT. This session did not shell into the hypervisor. Do not equate this guest with the Grasshopper root disk, the Helix production path, or an Oracle/AWS account until a hypervisor probe records its own machine-id.

Knowledge-graph names that must stay distinct until proven equal:

- Grasshopper workstation
- helix-omnikali production guest
- HOST-KALI-GUEST-25d9daa1

## Decisions from this pass

Apktool stays off the phone. HOST-KALI-GUEST-25d9daa1 has Java and 13G free, so it can hold a persistent apktool tree, but OpenJDK 25 may be too new for current apktool. Pin a JDK 21 runtime beside it rather than replacing the system JDK.

Morphe patch distribution stays on the existing source-manifest path (`morphe-patches` and sibling forks already exist). Custom patches get their own source repo and signed bundle. They are not silent edits on the Hoodles upstream fork. License-bypass and premium-unlock patches are out of scope.

Remote build, then deliver the APK to HOST-PHONE-A146U. On-device apktool remains optional, not the default.

Termux:Float, Termux:X11, and Termux:Styling stay in the human-interaction plane design even though they were absent on the last phone inventory. Float is the overlay intervention terminal. X11 is the graphical session. Styling is the readability layer. Termux:API notifications remain the current handoff mechanism. None of the three add-ons are required to keep the Rish transport.

Web automation is provider-agnostic and remote-first. OpenClaw is one installed runtime on HOST-KALI-GUEST-25d9daa1, not the only path. Grok, Gemini, and Codex CLIs are already on that guest, with browser substrates beside them. The phone is the human-gate surface, not the default browser farm.
