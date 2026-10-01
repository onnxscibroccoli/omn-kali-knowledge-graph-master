# Android System Package Audit - 2026-10-01

## Evidence identity

- Device: Samsung SM-A146U
- Android: 15
- API: 35
- Architecture: aarch64
- Build fingerprint: `samsung/a14xmsq/a14xm:15/AP3A.240905.015.A2/A146USQSJEZH3:user/release-keys`
- Remote Desktop Commander device name: `localhost`
- RDC device ID: `566d623e-df45-4b16-b2be-4cbd08567a49`
- Audit capture directory: `/sdcard/OmniKali/android-package-audit-20261001-130941`

## Package inventory

Live PackageManager inventory returned:

- 460 total packages
- 91 third-party packages
- 369 packages reported by PackageManager as system packages
- 26 APEX package paths
- 220 `/system`
- 12 `/system_ext`
- 47 `/product`
- 16 `/vendor`
- 76 `/data/app`
- 63 `/mnt/asec`

The path classification is evidence about where the installed package currently resolves from. It is **not** by itself proof that a package is stock, vendor-signed, unmodified, or safe.

## Important system-package finding

The 369 system-tagged packages are not all immutable base-image packages.

A second pass intersected the system-package list with package code paths:

- 321 system-tagged packages resolve from base partitions/APEX paths.
- 48 system-tagged packages resolve from `/data/app`.

Those 48 include updated Google, Samsung, carrier, and Android framework components. Examples observed include:

- `com.android.chrome`
- `com.android.vending`
- `com.google.android.gms`
- `com.google.android.webview`
- `com.google.android.networkstack`
- `com.google.android.youtube`
- `com.google.android.captiveportallogin`
- `com.samsung.android.themestore`
- `com.samsung.android.scs`
- `com.sec.android.sbrowser`

This means future integrity checks must distinguish:

1. immutable/base partition package
2. updated system package
3. ordinary third-party package
4. legacy/external `/mnt/asec` package
5. APEX package

Do not label the 369 system packages as "stock" without signature/hash/firmware-baseline evidence.

## Morphe and execution-relevant packages

The live inventory contains:

- `app.morphe.manager`
- `app.morphe.android.youtube`
- `app.morphe.android.apps.youtube.music`
- `anddea.youtube.music`
- `app.revanced.android.gms`
- `app.revanced.manager.plugin.downloader.apkcombo`
- `moe.shizuku.privileged.api`
- `com.rosan.ruto`
- `org.autojs.autojs.modify`
- `com.agatamessina.webinspector`
- `com.northmendo.Appzuku`
- `io.github.muntashirakon.AppManager`
- `io.github.samolego.canta`

These are inventory observations only. They are not an endorsement of any package.

## Termux add-on state

Present:

- `com.termux`
- `com.termux.api`
- `com.termux.gui`
- `com.termux.window`
- `com.termux.boot`
- `com.gardockt.termuxterminalwidget`
- `io.github.swiftstagrime.termuxrunner`

Absent from the live PackageManager inventory:

- `com.termux.float`
- `com.termux.styling`
- `com.termux.tasker`
- `com.termux.widget`
- `com.termux.x11`

The absent packages are therefore **NOT_INSTALLED**, not **NOT_RELEVANT**.

## Interaction-plane implication

Termux:Float, Termux:X11, and Termux:Styling remain candidate components.

- Termux:Float provides a floating terminal window.
- Termux:X11 provides a full X server and requires both an Android app and a Termux companion package.
- Termux:Styling provides terminal font/color customization and integrates with the Termux long-press menu.

They should remain in the architecture candidate set for the human interaction plane. Installation and integration should be a separate gated experiment, not silently bundled into the current transport path.

## Rish boundary

Direct PackageManager access through the unprivileged RDC child was sufficient for package inventory.

A later attempt to invoke the canonical Rish wrapper from the RDC child timed out. This does not invalidate the earlier canonical Rish proof. It demonstrates that **RDC child -> Rish** remains a distinct caller boundary and must not be conflated with **interactive Termux -> Rish**.

The canonical wrapper was not modified during this audit.

## Evidence labels

PROVEN:
- live PackageManager inventory
- 460-package count
- 91 third-party count
- 369 system-package count
- system package code-path classification
- 48 system-tagged packages resolving from `/data/app`
- Termux add-on presence/absence listed above

NOT_PROVEN:
- stock/firmware integrity of every system package
- package signing identity for every package
- APK hash comparison against Samsung firmware
- RDC-child Rish end-to-end transport
- real MCP observe -> act -> verify

## Durable artifact

The raw audit was captured on-device under:

`/sdcard/OmniKali/android-package-audit-20261001-130941/`

with package path/UID/installer data and normalized classification files.
