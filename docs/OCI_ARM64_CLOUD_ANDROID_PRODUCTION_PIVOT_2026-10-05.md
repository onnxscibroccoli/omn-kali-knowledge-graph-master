# OCI ARM64 Cloud Android Production Pivot - 2026-10-05

## Decision

Use the existing OCI ARM64 workstation as the preferred Cloud Android host, with an ARM64 Android virtual device, instead of forcing the existing x86 Android guest onto ARM or migrating OCI to x86.

This is a production architecture decision candidate, not a claim that the VM is already live.

## Evidence

- The execution-system contract identifies `oci-grasshopper-workstation` as Oracle Linux 9.8 on aarch64 in OCI us-ashburn-1.
- The physical Android execution target is also aarch64.
- Existing Grasshopper Android transport work should be preserved rather than repeated.
- AOSP Cuttlefish officially supports ARM64 hosts and provides the `aosp_cf_arm64_only_phone-userdebug` target.
- AOSP documents ARM64 Cuttlefish interaction through ADB and its WebRTC viewer.
- Current OCI host inspection showed the required KVM device is not presently exposed, so virtualization availability is the immediate infrastructure gate.

## Corrected implementation

1. Verify OCI exposes ARM64 KVM on the existing instance.
2. If KVM is absent, determine whether the current OCI shape/image can enable the required virtualization capability without destructive changes.
3. Do not modify host keyboard/XKB/input configuration.
4. Install the ARM64 Cuttlefish host package matching the selected ARM64 image build.
5. Launch `aosp_cf_arm64_only_phone` with persistent state.
6. Prove ADB sees the device.
7. Prove Android framebuffer and touch/control transport.
8. Reuse the existing clean viewer transport layer. Diagnostics remain optional and off by default.
9. Integrate the already-proven Broccoli Core/Rish contract at the Android execution boundary. Do not copy the historical Broccoli script collection wholesale.
10. Add a production supervisor that detects VM, ADB, display transport, and viewer failures and recovers only the failed layer.
11. Keep AWS OmniKali/Helix protected and independently verified.

## Production acceptance

PASS requires:

- ARM64 Android boots persistently.
- ADB reports the same persistent device after viewer reconnect.
- Physical-phone touch reaches Android.
- Physical-phone native keyboard reaches Android without modifying the OCI host keyboard.
- Home/Back/Recents operate.
- Android apps can be launched and controlled.
- Broccoli Core proven transport can execute against the device.
- Viewer reconnect preserves Android state.
- OCI host remains healthy.
- AWS OmniKali/Helix remains healthy.

## Evidence policy

Do not mark any item PASS merely because a process is listening. Screen, input, persistence, and Broccoli execution require end-to-end evidence.

The production viewer must not contain diagnostic UI. A diagnostic flag may expose the existing proof machinery for maintenance.

## Why this avoids rebuilding

The viewer, WebSocket transport, authentication/session concepts, Broccoli Rish contract, Android human-gate model, Grasshopper orchestration, and AWS/Helix production path remain separate contracts. Only the incompatible x86 Android guest substrate is replaced.

## References

- AOSP Cuttlefish ARM64 support and launch procedure.
- Existing OmniKali execution-system identifiers.
- Existing dated live desktop evidence.
- Existing Grasshopper Android transport evidence.
