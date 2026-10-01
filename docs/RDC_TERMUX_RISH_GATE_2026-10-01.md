# RDC to Termux to Rish gate evidence

Date: 2026-10-01
Android device: android-phone-a146u / Samsung SM-A146U
Android API: 35
Broccoli commit: d9a8d01
Broccoli PR: #63
Grasshopper PR: #123

## Gate status

PASS. A Remote Desktop Commander child can cross the previously failing caller boundary by entering Termux RunCommandService and then invoking the existing canonical Broccoli Rish wrapper.

RDC child -> /system/bin/am -> com.termux/.app.RunCommandService -> Termux bash -> broccoli-core/lib/rish_run.sh -> Shizuku/Rish -> Android shell uid=2000.

## Live evidence

- device.identity: PASS
- Rish identity: uid=2000(shell)
- Android SDK: 35
- Android device: a14xm
- package.inspect com.openai.chatgpt: PASS
- focused Broccoli transport/action regression: 21/21 PASS
- lower-level canonical Rish ui.dump: historically PASS
- fresh RDC-originated ui.dump: NOT_PROVEN because Android uiautomator can hang on this live device

## Safety invariant

The transport detects the reduced Android caller before invoking Rish. Interactive Termux keeps the direct canonical wrapper path. RDC/background callers without BOOTCLASSPATH use RunCommandService to enter a real Termux context, then the same rish_run.sh.

A direct Rish timeout is never blindly retried through the second transport, preventing duplicate mutation.

The Android action layer remains allowlisted. Arbitrary shell is not exposed as an Android action. Package names remain validated. app.stop remains confirmation-gated.

## External gates

This closes the RDC-to-Rish engineering gate. It does not close the RDC-to-uiautomator gate. It does not bypass Google 2-step verification, CAPTCHA, OAuth, biometrics, or GCP billing activation. Those remain explicit human/provider gates.

## Regression note

Full historical Broccoli unittest discovery is unhealthy on the current checkout because legacy runtime.* modules are absent and stale/placeholder tests remain. The transport/action-focused suite is green and the live caller-boundary proof is independent of those unrelated failures.
