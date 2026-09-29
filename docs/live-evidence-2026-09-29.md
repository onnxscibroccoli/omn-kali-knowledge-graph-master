# Live evidence 2026-09-29

## Public checks from this session

Target: `https://d22bad48irrbqe.cloudfront.net`

| Path | Result |
|---|---|
| GET /health | 200 `{"ok":true,"oidcConfigured":true,"publicOrigin":"https://d22bad48irrbqe.cloudfront.net"}` |
| GET /auth/login | 200 HTML title `Sign in · OmniKali Cloud` |
| GET /novnc/vnc.html | 200 noVNC example page |
| Login start | `/auth/start?provider=COGNITO` |

Repo docs in `onnxscibroccoli/helix`:

- CloudFront gateway: `https://d22bad48irrbqe.cloudfront.net`
- OIDC callback: `/auth/callback`
- Cognito user pool: `us-east-1_40X8yJKI2`
- Validated path: CloudFront -> nginx :80 -> Helix :8092 -> libvirt/QEMU -> domain `helix-omnikali`
- K3s `omnikali-desktop` exists on the same host and is a prototype, not the public ingress

## Operator screenshots supplied in chat

Captured on Android Chrome ~00:24–00:25 EDT, 2026-09-29, host `d22bad48irrbqe.cloudfront.net`.

1. Auth wall: OmniKali CLOUD, “Sign in to your machine.”, Continue with email.
2. Authenticated dashboard: LIVE HOST `helix-omnikali`, gateway online, `systemctl status omni-kali` panel showing Kali GNU/Linux Rolling, 1 vCPU, 1.5 GiB RAM, 40 GiB encrypted disk, `STREAM RFB → WSS → noVNC`, workstation `omnikali` marked desktop running.
3. Desktop viewer: Android keyboard chrome plus XFCE lock dialog for user `kali`, clock Tuesday September 29 00:24.

Status of this evidence:

- Public HTTP edge: OBSERVED in this session.
- Authenticated dashboard + lock screen: OBSERVED from operator screenshots, not independently replayed here (no login performed).
- Task lifecycle / fencing / worker replacement: still historical, not freshly re-run here.
- Public `/novnc/vnc.html` != proven authenticated guest RFB path.


## Fresh production reconciliation 2026-09-29 ~05:25 UTC

- Current-source Grasshopper revision: 6c0aa647dd5f5d68352defa5235697343826f2b1.
- Current-source Grasshopper test suite: 140/140 passed.
- verify:live-acceptance correctly exits non-zero with all eight required scenarios OPEN; no live COMPLETE evidence was manufactured.
- AWS Core reconciliation: helix-control-plane is available, private, encrypted, Multi-AZ, and deletion-protected. Backup retention remains 1 day.
- AWS rejected an attempted 14-day retention change with FreeTierRestrictionError; this is an account limitation, not an architecture failure. The 14-day production resilience gate therefore remains BLOCKED.
- CloudFront distribution is deployed and currently targets the established EC2/nginx origin. No public ingress architecture was changed.
