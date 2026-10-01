# Android System Package Audit 2026-10-01

Canonical device identity:

- Samsung SM-A146U
- Android 15 / API 35
- RDC device: `localhost`
- RDC ID: `566d623e-df45-4b16-b2be-4cbd08567a49`

The live package audit found 91 third-party packages. APK path classes were 220 `/system`, 12 `/system_ext`, 47 `/product`, 16 `/vendor`, 26 `/apex`, 76 `/data/app`, and 63 `/mnt/asec`.

48 packages carrying the Android system-package classification were installed from `/data/app`. This must not be treated as proof that they are aftermarket. Android system designation and APK storage path are separate facts. Provenance requires installer/source, signing certificate, version, and firmware comparison.

Morphe packages are present:

- `app.morphe.manager`
- `app.morphe.android.youtube`
- `app.morphe.android.apps.youtube.music`

The Termux execution family currently includes Termux, API, Boot, GUI, Window, a third-party widget, a third-party runner, and Shizuku. Official Float, Styling, Tasker, Widget, and X11 packages were not present in the audit inventory. They remain future candidates, especially for the human interaction plane.

Architecture direction: APK inspection and patch/build work should be movable to persistent Oracle Cloud or AWS workers. Android should remain the execution/UI edge, not the mandatory heavy build host.

Evidence: package inventory PASS; package provenance NOT_PROVEN; remote patch worker DESIGN_ONLY.
