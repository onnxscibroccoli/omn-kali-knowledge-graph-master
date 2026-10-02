# Live Android RUTO / Grok / APK Evidence 2026-10-02

## Scope

This record reconciles repository documentation with fresh Android/Termux inspection through the canonical Broccoli Rish transport.

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
- live process observed: `com.rosan.ruto`

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

## Current live Ruto virtual-display evidence

A later live inspection changed the evidence classification from the earlier overlay-only test.

Android currently exposes three private virtual displays:
- display 27: virtual shell-owned screen
- display 28: virtual shell-owned screen
- display 29: virtual shell-owned screen

All three report:
- 1080 x 2408
- 60 Hz
- type VIRTUAL
- owner `com.android.shell` / uid 2000
- private, own-content-only flags
- layer stacks matching display IDs 27, 28, and 29

The Android activity/window state provides application placement evidence:
- Termux process `com.termux` is live and its `TermuxActivity` is focused on display 28.
- ChatGPT process `com.openai.chatgpt` is live and its `MainActivity` is focused on display 29.
- Ruto process `com.rosan.ruto` is live.
- Ruto's `MainActivity` remains associated with the primary display/controller lane rather than replacing the application placement evidence on displays 28/29.

This establishes a current live acceptance that Ruto-mediated virtual-display infrastructure is present and that both ChatGPT and Termux are currently placed on separate virtual displays.

Important ownership distinction:
- Android reports the virtual-display owner as shell uid 2000, not the Ruto package uid.
- Ruto is nevertheless live and registered as the active input method service during the inspection.
- Therefore this evidence proves the observed Ruto-mediated state, but does not by itself prove that Ruto is the direct Android VirtualDisplay owner.

## Controlled display test and reconciliation

The earlier `tools/rish_display.py --create` test used the global `overlay_display_devices` mechanism.

Observed for that test:
- before: no overlay display setting
- after tool invocation: no new overlay display detected
- Android `dumpsys display`: `OverlayDisplayAdapter` with `mOverlays: size=0`
- built-in display remained display id 0
- overlay setting was restored to null

That result is still valid for the overlay helper, but it is not a valid test of the live Ruto virtual-display substrate. The current virtual displays are supplied through Android's `VirtualDisplayAdapter`, not `OverlayDisplayAdapter`.

Conclusion:
- do not use `overlay_display_devices` as the Ruto acceptance mechanism on this device.
- the repository should distinguish the overlay helper from the Ruto-mediated virtual-display path.

## Evidence classification

### PASS

- Rish transport to Android shell
- Ruto package installed and enabled
- Ruto main activity resolves
- Ruto input method service registered and live
- Grok package installed
- calculator package installed
- APK inspection tooling can parse the cached calculator APK
- current virtual-display infrastructure present: displays 27, 28, 29
- Termux currently placed on virtual display 28
- ChatGPT currently placed on virtual display 29
- primary display remains separate from the virtual application lanes
- current live state matches the user's observed Ruto-hosted ChatGPT/Termux workflow

### HISTORICAL / DOCUMENTED

- Ruto virtual-screen architecture
- Grok-on-secondary-display workflow
- previous observed calculator modification/install workflow

### NOT_PROVEN ON CURRENT BUILD

- exact Android API call or internal Ruto mechanism that created virtual displays 27/28/29
- Grok currently launched on one of the virtual displays
- simultaneous primary-user display plus background Grok acceptance
- complete Playwright-through-RDC acceptance
- productionized recreation of the current virtual-display state after reboot

### BLOCKER / FOLLOW-UP

The repository's earlier `meta/display_policy.json` claim that Ruto is not installed is stale relative to live package evidence, but it should not simply be changed to a boolean `true`. The acceptance model should distinguish:
- `ruto_installed`
- `ruto_configured`
- `virtual_display_present`
- `display_ids`
- `application_display_placement`
- `grok_display_acceptance`

Broccoli issue #66 remains the tracking item for reconciling the live Ruto installation with the virtual-display acceptance contract.

## Safety

The live inspection was read-only with respect to Android display state. No production Helix state was touched. No Android repository reset or cleanup was performed.
