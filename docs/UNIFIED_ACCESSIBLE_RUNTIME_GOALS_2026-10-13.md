# Unified Accessible Runtime — Persistent Cross-Repository Goals

**Graph extension:** `OMNIKALI-UNIFIED-ACCESSIBILITY-GOALS-2026-10-13`
**Parent coordination graphs:** `OMNIKALI-SYSTEM-KG-2026-10-01`, `OMNIKALI-SYSTEM-GOALS-2026-10-01` (preserved as historical/provenance snapshots).
**Status:** Architectural contract; not a claim that every target is implemented.
**Canonical reads:** Only files on each owned repository's `main` branch, never raw commit-SHA refs or unmerged branches. Development proposals go through reviewable feature branches. All public artifacts must be deidentified.

## Standing, non-expiring user requirements

1. **Accessibility before convenience.** All device interactions must work for users who cannot reliably perform complex manual gestures. Support chat, voice, semantic control, assisted visual input, permission-aware Android APIs and graceful degradation. The foundational accessibility tooling stays free.
2. **Three interoperable device classes.** Personal non-root Android phone (physical input, native apps and biometric approval); persistent cloud Android (isolated user apps and authenticated sessions); secure Linux/Kali development/access desktop (browser-windowed applications remotely controllable from Android).
3. **Provider-agnostic model/tool federation.** Common SDK abstractions for local/remote AI models, GitHub, cloud APIs, MCP servers and sanctioned app control. A device or agent may request an authorized capability on another device but must never directly copy passwords, biometric data or unrestricted OAuth tokens.
4. **Universal app understanding.** Maintain a versioned semantic UI graph and reusable action schema for Android accessibility trees, Linux AT-SPI, browsers/ARIA and authorized remote display transports. LLMs propose typed intents; the governor verifies capabilities and executes through a target-specific driver.
5. **Dynamic application engineering.** Implement accessible chat/voice-driven code editing, windowed Linux apps on the Android display, safe application patch/build/install workflows, and remote source-built Android APK customization. Preserve signing identities privately and require approval for sensitive installs.
6. **Resilient autonomous operation.** Event-bus decoupling, resource admission, supervisor/governor, guarded self-repair, checkpointing, deduplication, structured logs, privacy filters, stable semantic IDs, metrics and proof-based regression tests. **Observation must never trigger replay of its originating action.**
7. **Human authentication gateway.** OAuth/SSO, CAPTCHA and account verification challenges, payment confirmations and biometric checks are handed off to a trusted companion phone UI over secure channels, then the agent receives only a short-lived, purpose-bound approval or capability. No CAPTCHA bypass or biometric spoofing.
8. **Privacy and financial safety.** Default to local/self-hosted open source and verified zero-billable cloud entitlements. Never expose ADB/MCP, passwords, personal contact/medical data, or account sessions in public GitHub. No automatic merge or destructive shared-host changes without explicit operator approval.
9. **Continuity of architectural intent.** Preserve these goals as standing requirements, not just a one-session work request. Future agents must discover them from this graph without requiring the operator to restate the overall product vision. Statuses distinguish feasible-now vs blocked, not deleted aspirations.

## Typed control schema — minimal shared vocabulary

```json
{
  "schema": "broccoli.intent/v1",
  "request_id": "<unique-id>",
  "idempotency_key": "<unique-dedup-key>",
  "origin_device_id": "<registered-device>",
  "target_device_id": "<authorized-target>",
  "application_id": "<package-or-app>",
  "semantic_node_id": "<stable-selector>",
  "intent": "activate",
  "arguments": {},
  "required_capabilities": ["ui.interact"],
  "approval_policy": "user_if_sensitive",
  "expected_postcondition": "<verifiable-state>",
  "expires_at": "<timestamp>"
}
```

For an observation, record `event_id`, `caused_by_request_id`, `semantic_diff`, `confidence`, `privacy_classification` and `timestamp` separately. Event consumers must never transform `caused_by_request_id` into a second execution request. Each executor implements `observe/capabilities/authorize/execute/verify/checkpoint/recover`; transports are replaceable and may run on different machines.

## Dependency-ordered additions to the system goals

| ID | Goal | Depends on | Initial status | Exit evidence |
| --- | --- | --- | --- | --- |
| G15 | Shared semantic UI graph and action schema | G1, G11 | PLANNED | JSON schema, stable IDs, Android/browser/Linux conformance fixtures, replay/idempotency tests |
| G16 | Secure phone-mediated human interaction gateway | G10, G15 | IN_PROGRESS | User-approved OAuth/biometric handoff, scoped expiring grants, device-bound verification, audit test |
| G17 | One persistent OCI cloud Android worker (Redroid preferred) | G14, G15 | BLOCKED | Kernel Binder support, secure local-only ADB, boot and home screen, persistence/reboot and IME tests |
| G18 | Cross-device application window streaming | G15, G17 | PLANNED | Android screen-fit, keyboard/IME, zoom, Linux/Kali window rendering and reconnect acceptance |
| G19 | Provider-neutral AI/API/MCP capability federation | G1, G16 | PLANNED | At least two independent model/tool providers, no shared raw secrets, permission and failure tests |
| G20 | Safe remote Android app adaptation/build/install | G11, G16, G19 | PLANNED | Signed APK provenance, explicit operator approval, build reproducibility, device install/rollback |
| G21 | Fully accessible agentic development from voice/chat | G16, G18, G19, G20 | PLANNED | Spoken/typed request -> approval -> code edit -> test -> visible result on another device |
| G22 | Sustainability and reproducible free-tier self-hosting | G0, G3, G14 | ONGOING | Zero-billable preflight, explicit cloud capacity, backups, clean host reconstruction, no hidden paid dependencies |

This supplements rather than renames existing G0–G14. Dependencies represent an implementation plan, not automatic promotion to success.

## Live evidence and current constraints — 2026-10-13

The existing OCI Grasshopper host is Oracle Linux 9.8, ARM64 with kernel `6.12.0-206.104.4.4.el9uek.aarch64`, 2 OCPU and 12 GiB configured. It contains Kali/Grasshopper desktop services and an active separate Android QEMU container (not Kali). That QEMU Android exposes a loopback ADB port responding to the ADB handshake but has no full user-visible acceptance proof. Redroid is **not deployed**; Binder devices and matching development headers are missing, and rootless Podman currently writes layers onto the constrained boot disk. Do not use another operating system's kernel-module compile result as acceptance.

A controlled cleanup of three *inactive* Android QEMU experiment directories recovered **29,021,933,568 bytes** of attached-data-volume storage, while local desktop/noVNC HTTP responses and active Android TCP transport remained available. Non-secret findings were staged in Grasshopper's privacy-safe feature work; original small test/source archives remain private on the host. The active guest and Kali/remote access were not removed. Full device UX and reboot acceptance remain pending.

The architectural source owner for implementation is Grasshopper (`docs/architecture/UNIFIED_ACCESSIBLE_DEVICE_RUNTIME.md`, proposed under review) and Broccoli Core for its Android/A11y SDK; this master graph owns program-wide goal/dependency continuity.

## Agent delivery discipline

`inspect main -> identify goal -> inventory authority -> smallest isolated proposal -> privacy gate -> unit test -> live acceptance -> evidence -> update master graph -> operator-approved merge`

No unverified claim may substitute for a live accepted artifact. Do not commit names, direct personal contacts, private medical data, SSH/private keys, browser tokens, payment information, or authenticated Android images. Do not use raw commit SHAs to retrieve source content. This file is durable product intent: lack of current resources changes `status` to BLOCKED, not the goal.
