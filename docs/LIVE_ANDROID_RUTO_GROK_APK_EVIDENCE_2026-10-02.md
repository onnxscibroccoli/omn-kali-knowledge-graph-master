# Live Android RUTO / Grok / APK Evidence 2026-10-02

## Scope

This record reconciles repository documentation with a fresh Android/Termux inspection through the canonical Broccoli Rish transport.

Device:
- RDC device: `localhost`
- device id: `566d623e-df45-4b16-b2be-4cbd08567a49`
- Android SDK: 35

## Fresh package evidence

The canonical Rish path successfully queried Android package state.

Observed installed packages:
- `com.rosan.ruto`
- `ai.x.grok`
- `ai.x.grok.bot`
- `org.solovyev.android.calculator`
- `com.sec.android.app.popupcalculator`

Ruto:
- versionCode 1
- versionName 1.0
- enabled for user 0
- activity: `com.rosan.ruto/.ui.activity.MainActivity`
- input method service: `com.rosan.ruto/.service.MyInputMethodService`

Calculator:
- `org.solovyev.android.calculator`: versionName 2.3.3, versionCode 161
- cached Samsung Calculator APK was also inspected with the repository APK inspector:
  `com.sec.android.app.popupcalculator`, versionName 12.3.05.8, versionCode 1230508000
- cached APK exposes launchable activity `com.sec.android.app.popupcalculator.Calculator`

Grok:
- `ai.x.grok` is installed with arm64, English, and xxhdpi split APKs.

## Repository lineage

Broccoli contains:
- `docs/RUTO_BRIDGE.md`
- `tools/rish_display.py`
- `drivers/overlay/virtual_display.py`
- `lib/display_lane.py`
- `broccoli_secondary_display.py`
- `tools/apk_inspector.py`
- `tools/install_a11y_apk.sh`

`docs/RUTO_BRIDGE.md` explicitly describes the RUTO + Rish wire and identifies Ruto virtual-screen support as the intended background automation path.

## Controlled display test

Current `tools/rish_display.py --create` was executed through the canonical Rish path.

Observed:
- before: no overlay display setting
- after tool invocation: no new display detected
- Android `dumpsys display`: `OverlayDisplayAdapter` with `mOverlays: size=0`
- built-in display remained display id 0
- overlay setting was restored to null

Conclusion:
- the current `overlay_display_devices` implementation is not a valid proof of Ruto virtual-screen activation on this Android 15 / SDK 35 device.
- do not substitute this path for the previously observed working Ruto virtual screen.

## Evidence classification

### PASS
- Rish transport to Android shell
- Ruto package installed and enabled
- Ruto main activity resolves
- Grok package installed
- calculator package installed
- APK inspection tooling can parse the cached calculator APK

### HISTORICAL / DOCUMENTED
- Ruto virtual-screen architecture
- Grok-on-secondary-display workflow
- previous observed calculator modification/install workflow

### NOT_PROVEN ON CURRENT BUILD
- Ruto virtual-screen creation
- a secondary display actually present
- Grok launched on that secondary display
- simultaneous primary-user display plus background Grok acceptance
- complete Playwright-through-RDC acceptance

### BLOCKER
The repository's `meta/display_policy.json` currently says `ruto_installed=false` despite live package evidence showing Ruto installed. This field must not be changed to true merely from package installation. The acceptance model should distinguish installation, configuration, virtual-display presence, and application placement.

See Broccoli issue #66 for the repair/acceptance gate.

## Safety

The controlled display test restored the global overlay setting to null. No production Helix state was touched. No Android repository reset or cleanup was performed.
