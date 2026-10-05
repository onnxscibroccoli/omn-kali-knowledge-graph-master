# OCI ARM64 Cloud Android Production Pivot - 2026-10-05

## Decision

Use the ARM64 architecture for Cloud Android, but **do not use the current OCI Ampere VM as the production Cuttlefish host**.

The OCI VM path is now **BLOCKED by infrastructure capability**: the guest does not receive hardware virtualization/KVM exposure. This is an OCI hypervisor boundary, not a guest configuration defect.

The production architecture remains valid. Only the guest compute substrate changes.

## Evidence

- The execution-system contract identifies `oci-grasshopper-workstation` as Oracle Linux 9.8 on aarch64 in OCI us-ashburn-1.
- The physical Android execution target is also aarch64.
- Existing Grasshopper Android transport work should be preserved rather than repeated.
- AOSP Cuttlefish officially supports ARM64 hosts and provides the `aosp_cf_arm64_only_phone-userdebug` target.
- AOSP documents ARM64 Cuttlefish interaction through ADB and WebRTC.
- Current OCI host inspection showed no usable `/dev/kvm`.
- Oracle's current ARM compute documentation distinguishes A1 VM and A1 bare-metal shapes.
- Oracle's nested-KVM guidance explicitly states that Ampere ARM VMs do not support nested virtualization.
- Therefore the current OCI ARM64 VM cannot be promoted to a production Cuttlefish hypervisor.

## Corrected implementation

1. Keep the ARM64 KVM gate fail-closed.
2. Do not attempt to manufacture `/dev/kvm` inside the OCI VM.
3. Do not weaken production to QEMU TCG/software emulation.
4. Do not modify OCI/Debian host keyboard, XKB, or input configuration.
5. Validate an ARM64 bare-metal substrate before installing or rewriting Cuttlefish deployment automation.
6. Preferred next substrate: AWS Graviton bare metal, with `c6g.metal` as the first candidate if available in the target account/region.
7. Secondary substrate: OCI `BM.Standard.A1.160` if AWS metal capacity/cost is unfavorable.
8. Install the ARM64 Cuttlefish host package matching the selected ARM64 image build.
9. Launch `aosp_cf_arm64_only_phone` with persistent state.
10. Prove ADB sees the device.
11. Prove Android framebuffer and touch/control transport.
12. Reuse the existing clean viewer transport layer. Diagnostics remain optional and off by default.
13. Integrate the already-proven Broccoli Core/Rish contract at the Android execution boundary. Do not copy the historical Broccoli script collection wholesale.
14. Add a production supervisor that detects VM, ADB, display transport, and viewer failures and recovers only the failed layer.
15. Keep AWS OmniKali/Helix protected and independently verified.

## Production acceptance

PASS requires:

- ARM64 Android boots persistently.
- ADB reports the same persistent device after viewer reconnect.
- Physical-phone touch reaches Android.
- Physical-phone native keyboard reaches Android without modifying the host keyboard.
- Home/Back/Recents operate.
- Android apps can be launched and controlled.
- Broccoli Core proven transport can execute against the device.
- Viewer reconnect preserves Android state.
- Host remains healthy.
- AWS OmniKali/Helix remains healthy.

## Evidence policy

Do not mark any item PASS merely because a process is listening. Screen, input, persistence, and Broccoli execution require end-to-end evidence.

The production viewer must not contain diagnostic UI. A diagnostic flag may expose the existing proof machinery for maintenance.

## Why this avoids rebuilding

The viewer, WebSocket transport, authentication/session concepts, Broccoli Rish contract, Android human-gate model, Grasshopper orchestration, and AWS/Helix production path remain separate contracts. Only the incompatible x86 Android guest substrate is replaced.

## Current status

**OCI ARM64 VM: BLOCKED / NOT_PROVEN for production Cuttlefish.**

**AWS Graviton bare metal: NEXT VALIDATION TARGET.**

No compute resource is provisioned by this documentation update.

## References

- AOSP Cuttlefish ARM64 support and launch procedure.
- Oracle ARM-based Compute documentation.
- Oracle KVM nested virtualization guidance.
- AWS EC2 nested virtualization documentation.
- Existing OmniKali execution-system identifiers.
- Existing dated live desktop evidence.
- Existing Grasshopper Android transport evidence.
