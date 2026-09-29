# Desktop session identity 2026-09-29

Operator screenshots from authenticated CloudFront desktop viewer `d22bad48irrbqe.cloudfront.net`.

## What the GUI proves

- Past the XFCE lock screen.
- Firefox running with Kali-style bookmarks (OffSec, Kali Tools, Exploit-DB, Kali NetHunter).
- Outbound web works: Wikipedia Quantum mechanics loaded.
- Mobile viewer chrome present: Android keyboard, Paste / Ctrl-Alt-Del / Reconnect / Set Kali password / Console.

## What the shell proves

Zutty terminal in the same viewer:

```
root@ip-172-31-8-59:~# uname -a
Linux ip-172-31-8-59 6.12.107+deb13-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.107-1 (2026-08-29) x86_64 GNU/Linux
```

That identity is the AWS EC2 host from `helix/docs/ARCHITECTURE_VERIFICATION_2026-09-29.md`:

- host private IP / hostname family: `172.31.8.59` / `ip-172-31-8-59`
- host OS: Debian 13 (trixie) cloud kernel
- not hostname `kali`
- not a `kali-amd64` kernel
- not guest IP `192.168.122.78`

## Interpretation

The authenticated browser desktop is currently showing the **hypervisor/host session** (or a shell on the host), not the validated libvirt guest `helix-omnikali`.

This matches the existing warning that public/host VNC `:5900` and the Kali guest VNC are different endpoints.

Status:
- GUI + outbound Firefox: OBSERVED via operator screenshots.
- Session identity: OBSERVED as Debian cloud host `ip-172-31-8-59`.
- Authenticated RFB to guest `helix-omnikali`: still not proven by these shots.


## Fresh guest identity check 2026-09-29 ~01:13 EDT

Executed from the connected Debian EC2 hypervisor through the libvirt/QEMU guest agent for domain `helix-omnikali`.

- `virsh dominfo helix-omnikali`: domain running, UUID `c58b4df8-2138-4326-bebf-94966d423f5b`, 2 vCPU, 2 GiB maximum memory, 1.5 GiB current memory.
- Guest-agent `uname -a` returned:

```
Linux kali 7.1.5+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 7.1.5-1kali1 (2026-07-29) x86_64 GNU/Linux
```

This is fresh host-side evidence that the running `helix-omnikali` libvirt domain contains a Kali guest kernel. It is separate from the earlier browser-session shell evidence, which identified the Debian hypervisor host.

Status: OBSERVED fresh guest identity evidence. This does not by itself prove the full authenticated CloudFront RFB path or task lifecycle/fencing acceptance.
