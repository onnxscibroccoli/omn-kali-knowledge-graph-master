# Evidence: 2026-10-06/07 Kali OOM storm

Observed on Helix host `i-03b6a82d46271d9cd`.

Facts:
- Host RAM: 3.7 GiB.
- Swap: 2 GiB; it reached effectively 100% utilization during the incident.
- Persistent Kali libvirt guest: `helix-omnikali`, configured for 2 GiB.
- Concurrent Android QEMU workers: `omnikali-cloud-android`, `omnikali-adb-control`, `omnikali-adb-e1000`.
- Kernel OOM logs repeatedly killed `qemu-system-x86` processes.
- After the duplicate Android workers were terminated, Kali was started successfully with libvirt and remained running.
- A host memory guard is now enabled every 30 seconds.

Interpretation:
This is a host capacity/admission-control failure, not evidence of corruption in the persistent Kali disk. Future agents must check host memory, swap, QEMU count/RSS, and kernel OOM evidence before treating a Kali restart as a guest-level failure.
