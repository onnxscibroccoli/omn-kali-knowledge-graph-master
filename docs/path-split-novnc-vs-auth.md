# Two public URLs, two machines

Operator confirmation 2026-09-29 plus public HTTP checks and helix repo config.

## Path A — host Debian noVNC

URL: `https://d22bad48irrbqe.cloudfront.net/novnc/vnc.html`

Lands on the EC2 host desktop, not the Kali guest.

Evidence:
- Public GET returns 200 noVNC page.
- Operator: this URL opens Debian.
- `uname` in that session: `root@ip-172-31-8-59` / `6.12.107+deb13-cloud-amd64`.
- Unit `production/desktop/helix-novnc.service`:
  `websockify --web=/usr/share/novnc 127.0.0.1:6080 127.0.0.1:5900`
- Repo nginx serves `/novnc/` from `/usr/share/novnc/` and does not send it through the Helix ticket path.

Status: OBSERVED host console. Do not document this URL as the Kali workstation.

## Path B — authenticated Kali control plane

URL: `https://d22bad48irrbqe.cloudfront.net/auth/login`

This is the product path.

Flow:
1. OmniKali Cloud login
2. Cognito (`/auth/start?provider=COGNITO`)
3. Helix session
4. Portal / Launch desktop for workspace `omnikali` / host `helix-omnikali`
5. Short-lived WS ticket
6. Gateway tunnels RFB to the workspace VNC (libvirt guest), not host `:5900`

Evidence:
- Public GET `/auth/login` 200.
- Public GET `/health` `oidcConfigured: true`.
- Operator: login + control plane opens Kali.
- Dashboard copy: LIVE HOST `helix-omnikali`, `STREAM RFB → WSS → noVNC`.
- `production/gateway/README.md`: gateway is the only public desktop entry; VNC stays localhost; ticketed WS is the tunnel.

Status: OBSERVED authenticated guest path by operator. Guest `uname`/`hostname` screenshot not yet attached.

## Rule

```
/novnc/vnc.html  = Debian host :5900
/auth/login      = control plane → Kali guest helix-omnikali
```

Agents must not collapse these into one desktop.
